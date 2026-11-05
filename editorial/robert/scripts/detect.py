"""Detect the paper sheet in each photo and write a debug overlay + corners JSON."""
import cv2, numpy as np, json, glob, os, sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = {}
os.makedirs(f"{root}/build/debug", exist_ok=True)

def order(pts):
    pts = np.array(pts, dtype=np.float32)
    s = pts.sum(1); d = np.diff(pts, axis=1).ravel()
    return np.array([pts[s.argmin()], pts[d.argmin()], pts[s.argmax()], pts[d.argmax()]])

for f in sorted(glob.glob(f"{root}/src/*.jpg")):
    name = os.path.basename(f)[:-4]
    img = cv2.imread(f)
    h, w = img.shape[:2]
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
    # paper = brightest, most neutral/blue-ish region. table is warmer (b* higher)
    L, a, b = cv2.split(lab)
    score = L - 2.2 * (b - 128) - 0.0 * np.abs(a - 128)
    score = cv2.GaussianBlur(score, (0, 0), 6)
    best = None
    for q in (55, 45, 35, 25):
        thr = np.percentile(score, q)
        m = (score > thr).astype(np.uint8) * 255
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((41, 41), np.uint8))
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((21, 21), np.uint8))
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not cs: continue
        c = max(cs, key=cv2.contourArea)
        hull = cv2.convexHull(c)
        for eps in (0.01, 0.02, 0.03, 0.05):
            ap = cv2.approxPolyDP(hull, eps * cv2.arcLength(hull, True), True)
            if len(ap) == 4: break
        area = cv2.contourArea(hull) / (w * h)
        if len(ap) == 4 and 0.45 < area < 0.995:
            best = order(ap.reshape(-1, 2)); break
    if best is None:
        best = order([[0, 0], [w, 0], [w, h], [0, h]])
    out[name] = best.tolist()
    dbg = img.copy()
    cv2.polylines(dbg, [best.astype(np.int32)], True, (0, 0, 255), 6)
    cv2.imwrite(f"{root}/build/debug/{name}.jpg", cv2.resize(dbg, (w // 4, h // 4)))
json.dump(out, open(f"{root}/build/corners_auto.json", "w"), indent=1)
print(json.dumps({k: [list(map(int, p)) for p in v] for k, v in out.items()}))
