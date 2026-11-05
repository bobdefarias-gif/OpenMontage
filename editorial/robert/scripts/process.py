"""Digitize photographed artworks into clean plates.

perspective-correct (manual quads) -> flat-field (remove uneven light) ->
paper-white balance -> gentle contrast -> plates/NN.jpg (+ web thumbs)
"""
import cv2, numpy as np, os, json

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = None  # full frame

# TL, TR, BR, BL in source pixels; mode: 'flat' (paper visible) or 'wb' (painted ground)
WORKS = {
    "01": ([(44, 74), (2010, 64), (2010, 1508), (34, 1508)], "flat", 0),
    "02": ([(90, 72), (1952, 74), (1946, 1386), (100, 1392)], "flat", 0),
    "03": ([(60, 64), (1966, 56), (1972, 1428), (92, 1432)], "flat", 0),
    "04": ([(20, 60), (1952, 44), (1958, 1452), (16, 1452)], "flat", 0),
    "05": ([(40, 50), (1986, 42), (1984, 1478), (42, 1474)], "wb", 0),
    "06": ([(66, 72), (1958, 62), (1958, 1438), (62, 1440)], "flat", 0),
    "07": ([(42, 88), (1990, 76), (1990, 1462), (40, 1472)], "flat", 0),
    "08": ([(56, 76), (1962, 70), (1952, 1458), (56, 1468)], "flat", 0),
    "09": ([(78, 74), (1978, 60), (1990, 1480), (62, 1468)], "flat", 0),
    "10": ([(50, 82), (1952, 72), (1956, 1446), (48, 1432)], "flat", 0),
    "11": (F, "flat", 0),
    "12": ([(52, 72), (1956, 62), (1960, 1448), (50, 1440)], "flat", 0),
    "13": (F, "flat", 0),
    "14": (F, "flat", 0),
    "15": ([(90, 82), (1950, 72), (1942, 1406), (102, 1454)], "flat", 180),
    "16": ([(40, 96), (1960, 102), (1952, 1440), (36, 1450)], "wb", 0),
}
INSET = 0.012


def warp(img, quad):
    if quad is None:
        return img
    q = np.float32(quad)
    w = int(max(np.linalg.norm(q[1] - q[0]), np.linalg.norm(q[2] - q[3])))
    h = int(max(np.linalg.norm(q[3] - q[0]), np.linalg.norm(q[2] - q[1])))
    M = cv2.getPerspectiveTransform(q, np.float32([[0, 0], [w, 0], [w, h], [0, h]]))
    out = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LANCZOS4)
    dx, dy = int(w * INSET), int(h * INSET)
    return out[dy:h - dy, dx:w - dx]


def flatfield(img):
    """Divide by a smooth estimate of the paper illumination (per channel)."""
    f = img.astype(np.float32)
    h, w = f.shape[:2]
    s = 4
    small = cv2.resize(f, (w // s, h // s), interpolation=cv2.INTER_AREA)
    k = max(15, (min(h, w) // s) // 12) | 1
    ill = cv2.dilate(small, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    ill = cv2.GaussianBlur(ill, (0, 0), k / 1.5)
    ill = cv2.resize(ill, (w, h), interpolation=cv2.INTER_CUBIC)
    out = f / np.maximum(ill, 1) * 247.0
    return np.clip(out, 0, 255)


def whitebalance(img):
    f = img.astype(np.float32)
    lum = f.mean(2)
    m = lum > np.percentile(lum, 97)
    ref = f[m].mean(0)
    out = f * (247.0 / ref)
    return np.clip(out, 0, 255)


def neutralize(f):
    """Scale each channel so the paper (bright, low-chroma pixels) lands on neutral 252."""
    lum = f.mean(2)
    chroma = f.max(2) - f.min(2)
    m = (lum > np.percentile(lum, 60)) & (chroma < np.percentile(chroma, 50))
    if m.sum() < 1000:
        m = lum > np.percentile(lum, 95)
    ref = np.median(f[m], axis=0)
    return np.clip(f * (252.0 / ref), 0, 255)


def finish(f):
    # paper -> warm archival white; deepen pigments slightly (soft S-curve on luminance)
    x = f / 255.0
    lo = np.percentile(x.mean(2), 0.5)
    x = np.clip((x - lo * 0.6) / (1 - lo * 0.6), 0, 1)
    x = np.where(x > 0.90, 1.0 - (1 - x) * 0.35, x)  # push near-white paper to clean white
    x = x ** 1.08
    # pigment saturation boost in LAB-ish space
    hsv = cv2.cvtColor((x * 255).astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * 1.12, 0, 255)
    out = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    paper = np.array([238, 245, 249], np.float32)  # BGR of warm white #F9F5EE
    out = out * (paper / 255.0)
    # unsharp mask for print crispness
    blur = cv2.GaussianBlur(out, (0, 0), 1.2)
    out = cv2.addWeighted(out, 1.35, blur, -0.35, 0)
    return np.clip(out, 0, 255).astype(np.uint8)


def trim_edges(img, maxf=0.04):
    """Cut away leftover table/shadow rows+cols at the borders (yellowish or dark vs paper)."""
    f = img.astype(np.float32)
    def bad(line):
        med = np.median(line, axis=0)  # BGR
        yellow = (med[1] + med[2]) / 2 - med[0]
        return yellow > 20 or med.mean() < 205
    h, w = f.shape[:2]
    t = b = l = r = 0
    while t < h * maxf and bad(f[t]): t += 1
    while b < h * maxf and bad(f[h - 1 - b]): b += 1
    while l < w * maxf and bad(f[:, l]): l += 1
    while r < w * maxf and bad(f[:, w - 1 - r]): r += 1
    pad = lambda v: v + (4 if v else 0)
    return img[pad(t):h - pad(b), pad(l):w - pad(r)]


meta = {}
os.makedirs(f"{R}/plates/web", exist_ok=True)
for k, (quad, mode, rot) in WORKS.items():
    img = cv2.imread(f"{R}/src/{k}.jpg")
    img = warp(img, quad)
    img = neutralize(flatfield(img)) if mode == "flat" else whitebalance(img)
    img = finish(img)
    if mode == "flat" and quad is not None:
        img = trim_edges(img)
    if rot == 180:
        img = cv2.rotate(img, cv2.ROTATE_180)
    cv2.imwrite(f"{R}/plates/{k}.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 93])
    h, w = img.shape[:2]
    s = 1100 / max(h, w)
    cv2.imwrite(f"{R}/plates/web/{k}.jpg", cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA),
                [cv2.IMWRITE_JPEG_QUALITY, 86])
    meta[k] = {"w": w, "h": h}
json.dump(meta, open(f"{R}/plates/meta.json", "w"), indent=1)
print(meta)
