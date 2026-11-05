"""Prepare art assets for the sample pages (Option B: artwork integrated, no frames).

- cutout: 'unmultiply' the paper away -> RGBA, the ink stays exactly as painted
- lens: circular crop of a plate (crop = allowed; drawing untouched)
- silhouette: solid shape derived from a cutout (for 'find the shadow')
Writes art/*.png and art/manifest.json (crop positions -> used by the answer key).
"""
import cv2, numpy as np, json, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATES = os.environ.get("PLATES", os.path.join(os.path.dirname(R), "robert", "plates"))
OUT = f"{R}/art"
os.makedirs(OUT, exist_ok=True)
man = {}


LENS_MAX = int(os.environ.get("LENS_MAX", 760))
CUT_MAX = int(os.environ.get("CUT_MAX", 2300))


def cap(im, mx):
    h, w = im.shape[:2]
    if max(h, w) <= mx:
        return im
    s = mx / max(h, w)
    return cv2.resize(im, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)


def load(k):
    return cv2.imread(f"{PLATES}/{k}.jpg")


def ink_map(img):
    d = 255 - img.astype(np.float32).min(2)
    paper = np.median(d)
    return d, paper


def cutout(k, name, lo=10, hi=60, pad=12):
    img = load(k).astype(np.float32)
    d, paper = ink_map(img)                     # distance from paper white
    a = np.clip((d - paper - lo) / (hi - lo), 0, 1)
    a = cv2.GaussianBlur(a, (0, 0), 0.6)
    am = np.maximum(a, 1e-3)[..., None]
    col = 255 - (255 - img) / am               # unmultiply from white
    col = np.clip(col, 0, 255)
    rgba = np.dstack([col, a * 255]).astype(np.uint8)
    big = cv2.dilate((a > 0.3).astype(np.uint8), np.ones((25, 25), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(big)
    keep = np.argsort(st[1:, cv2.CC_STAT_AREA])[::-1][:6] + 1
    keep = [i for i in keep if st[i, cv2.CC_STAT_AREA] > 0.01 * st[1:, cv2.CC_STAT_AREA].max()]
    mask = np.isin(lab, keep)
    a = a * mask
    rgba[..., 3] = (a * 255).astype(np.uint8)
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = max(ys.min() - pad, 0), ys.max() + pad, max(xs.min() - pad, 0), xs.max() + pad
    rgba = rgba[y0:y1, x0:x1]
    cw_, ch_ = rgba.shape[1], rgba.shape[0]
    cv2.imwrite(f"{OUT}/{name}.png", cap(rgba, CUT_MAX))
    man[name] = {"src": k, "w": cw_, "h": ch_, "x0": int(x0), "y0": int(y0), "W": int(img.shape[1]), "H": int(img.shape[0])}
    return rgba


def silhouette(rgba, name, close=25, color=(58, 44, 36), flip=False):
    a = (rgba[..., 3] > 60).astype(np.uint8) * 255
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close, close))
    a = cv2.morphologyEx(a, cv2.MORPH_CLOSE, k)
    cs, _ = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m = np.zeros_like(a)
    big = [c for c in cs if cv2.contourArea(c) > 0.002 * a.size]
    cv2.drawContours(m, big, -1, 255, -1)
    m = cv2.GaussianBlur(m, (0, 0), 1.2)
    out = np.zeros((*m.shape, 4), np.uint8)
    out[..., :3] = color
    out[..., 3] = m
    if flip:
        out = out[:, ::-1]
    ys, xs = np.where(m > 40)
    out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    cv2.imwrite(f"{OUT}/{name}.png", out)
    man[name] = {"w": out.shape[1], "h": out.shape[0]}


def lens(k, name, cx, cy, r, search=0.12, mx=None):
    """Circular crop; cx, cy, r normalized (r to width). Snaps to the inkiest spot near (cx, cy)."""
    img = load(k)
    h, w = img.shape[:2]
    R_ = int(r * w)
    d, paper = ink_map(img)
    ink = (d > paper + 35).astype(np.float32)
    ii = cv2.integral(ink)
    best, bx, by = -1, int(cx * w), int(cy * h)
    for yy in range(int((cy - search) * h), int((cy + search) * h), 12):
        for xx in range(int((cx - search) * w), int((cx + search) * w), 12):
            if xx - R_ < 0 or yy - R_ < 0 or xx + R_ >= w or yy + R_ >= h: continue
            sc = ii[yy + R_, xx + R_] - ii[yy - R_, xx + R_] - ii[yy + R_, xx - R_] + ii[yy - R_, xx - R_]
            sc -= 0.15 * ((xx - cx * w) ** 2 + (yy - cy * h) ** 2) ** .5 * R_ / w * 4
            if sc > best: best, bx, by = sc, xx, yy
    X, Y = bx, by
    cx, cy = X / w, Y / h
    crop = img[Y - R_:Y + R_, X - R_:X + R_]
    mx = mx or LENS_MAX
    if crop.shape[0] > mx:
        crop = cv2.resize(crop, (mx, mx), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"{OUT}/{name}.jpg", crop, [cv2.IMWRITE_JPEG_QUALITY, 90])
    man[name] = {"src": k, "cx": cx, "cy": cy, "r": r}


# ---- p.10 Odd one out: 3 lenses of one work + 1 of another (different colour family)
ROWS = [
    ("06", "07", 2, [(.25, .30), (.62, .62), (.80, .30), (.40, .62)]),   # sepia lines vs black lines
    ("15", "01", 0, [(.30, .45), (.25, .30), (.60, .55), (.80, .40)]),   # blue network vs red script
    ("02", "04", 3, [(.25, .35), (.55, .55), (.80, .65), (.45, .45)]),   # honey strokes vs red/blue strokes
    ("09", "10", 1, [(.40, .40), (.50, .45), (.75, .45), (.30, .75)]),   # black blocks vs brown maze
]
for ri, (main, odd, pos, pts) in enumerate(ROWS):
    for ci, (x, y) in enumerate(pts):
        lens(odd if ci == pos else main, f"odd_r{ri}_c{ci}", x, y, 0.085)
man["odd_answer"] = [p for *_, p, _ in [(r[0], r[1], r[2], r[3]) for r in ROWS]]

# ---- p.14 Find the shadow: bird cut out + 3 silhouettes (bird, red creature, fish)
bird = cutout("13", "bird")
silhouette(bird, "sh_bird", close=9)
sh = cv2.imread(f"{OUT}/sh_bird.png", cv2.IMREAD_UNCHANGED)
cv2.imwrite(f"{OUT}/sh_bird_flip.png", sh[::-1])        # upside-down decoy
man["sh_bird_flip"] = man["sh_bird"]
silhouette(cutout("01", "creature"), "sh_creature", close=41)

# ---- p.64 Where is this piece? big plate + 3 lenses (1 true, 2 from look-alike works)
cutout("12", "painting12")
lens("12", "piece_true", .66, .30, .07)
lens("03", "piece_d1", .30, .40, .07)
lens("08", "piece_d2", .70, .70, .07)

json.dump(man, open(f"{OUT}/manifest.json", "w"), indent=1)
print("ok", len(man))

# ---- set 2: memory pair (p.17/18) and pattern page (p.30) — one fixed tile per colour family
TILES = {"blue": ("15", .45, .45), "red": ("01", .35, .30), "honey": ("02", .40, .45), "black": ("07", .45, .40),
         "sepia": ("06", .35, .55), "green": ("08", .75, .72), "multi": ("12", .30, .30)}
for name, (k, x, y) in TILES.items():
    lens(k, f"tile_{name}", x, y, 0.09)
json.dump(man, open(f"{OUT}/manifest.json", "w"), indent=1)


# ---- V1 art map extras: whole works as pictures (sheet kept) for p.36 / p.37
for k in ["02", "15", "07", "12", "13", "01", "04"]:
    im = load(k)
    name = f"work{k}" if k not in ("02", "15") else f"painting{k}"
    cv2.imwrite(f"{OUT}/{name}.jpg", cap(im, 1500), [cv2.IMWRITE_JPEG_QUALITY, 90])
    man[name] = {"src": k, "w": im.shape[1], "h": im.shape[0]}
    if k in ("02", "15"):
        cv2.imwrite(f"{OUT}/work{k}.jpg", cap(im, 1500), [cv2.IMWRITE_JPEG_QUALITY, 90]); man[f"work{k}"] = man[name]
json.dump(man, open(f"{OUT}/manifest.json", "w"), indent=1)

# ---- V2 extras
cutout("14", "face14"); cutout("11", "face11")
for k in ["14", "11", "05", "09", "08", "03", "10"]:
    im = load(k)
    cv2.imwrite(f"{OUT}/work{k}.jpg", cap(im, 1500), [cv2.IMWRITE_JPEG_QUALITY, 90]); man[f"work{k}"] = {"src": k, "w": im.shape[1], "h": im.shape[0]}
# detail detective (p.8): 3 pieces of the geometric face + 1 look-alike from the black blocks
for i, (x, y) in enumerate([(.25, .35), (.55, .30), (.40, .70)]):
    lens("14", f"det_{i}", x, y, 0.075)
lens("09", "det_x", .45, .40, 0.075)
# odd one out PRO (p.12): look-alike pairs
for name, (k, x, y) in {"a06": ("06", .3, .4), "b06": ("06", .7, .6), "c06": ("06", .5, .3), "d06": ("06", .2, .7),
                        "x10": ("10", .5, .5), "a07": ("07", .3, .4), "b07": ("07", .6, .6), "c07": ("07", .7, .3),
                        "d07": ("07", .4, .7), "x09": ("09", .4, .4), "a15": ("15", .3, .3), "b15": ("15", .6, .6),
                        "c15": ("15", .7, .3), "d15": ("15", .3, .7), "x03": ("03", .2, .8), "a08": ("08", .7, .7),
                        "b08": ("08", .5, .8), "c08": ("08", .8, .5), "d08": ("08", .6, .55), "x12": ("12", .55, .6)}.items():
    lens(k, f"pro_{name}", x, y, 0.08)
lens("09", "turn_target", .40, .40, 0.08); lens("09", "turn_other", .75, .65, 0.08); lens("07", "turn_x", .5, .5, 0.08)
img = cv2.imread(f"{OUT}/turn_target.jpg")
cv2.imwrite(f"{OUT}/turn_rot.jpg", cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)); man["turn_rot"] = man["turn_target"]
img = cv2.imread(f"{OUT}/turn_other.jpg")
cv2.imwrite(f"{OUT}/turn_other_rot.jpg", cv2.rotate(img, cv2.ROTATE_180)); man["turn_other_rot"] = man["turn_other"]
lens("07", "griddraw", .5, .45, 0.16, mx=1500)
json.dump(man, open(f"{OUT}/manifest.json", "w"), indent=1)

# ---- covers: larger crops (more pixels for print)
for name, (k, x, y) in {"red": ("01", .35, .30), "honey": ("02", .40, .45), "blue": ("15", .45, .45), "green": ("08", .72, .70),
                        "black": ("07", .45, .40), "multi": ("12", .30, .30), "sepia": ("06", .35, .55)}.items():
    lens(k, f"cov_{name}", x, y, 0.13, mx=900)
json.dump(man, open(f"{OUT}/manifest.json", "w"), indent=1)
