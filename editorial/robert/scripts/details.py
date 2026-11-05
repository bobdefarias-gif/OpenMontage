"""Pick the most 'eventful' window of each plate for detail spreads (ink-energy maximum)."""
import cv2, numpy as np, json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
meta = json.load(open(f"{R}/plates/meta.json"))
out = {}
for k in meta:
    g = cv2.imread(f"{R}/plates/web/{k}.jpg", 0).astype(np.float32)
    h, w = g.shape
    e = np.abs(cv2.Sobel(g, cv2.CV_32F, 1, 0)) + np.abs(cv2.Sobel(g, cv2.CV_32F, 0, 1))
    ink = 255 - g
    score = e * 0.6 + ink * 0.4
    # window aspect matches a 300x240 page (1.25), ~55% of the sheet width
    ww = int(w * 0.55); wh = int(ww / 1.25)
    if wh > h * 0.9: wh = int(h * 0.5); ww = int(wh * 1.25)
    ii = cv2.integral(score)
    best, bxy = -1, (0, 0)
    for y in range(int(h*0.06), h - wh - int(h*0.06), 8):
        for x in range(int(w*0.06), w - ww - int(w*0.06), 8):
            s = ii[y+wh, x+ww] - ii[y, x+ww] - ii[y+wh, x] + ii[y, x]
            # prefer central-ish windows slightly
            cx, cy = (x + ww/2)/w - .5, (y + wh/2)/h - .5
            s *= 1 - 0.35*(cx*cx + cy*cy)
            if s > best: best, bxy = s, (x, y)
    x, y = bxy
    out[k] = [round(x/w, 4), round(y/h, 4), round(ww/w, 4), round(wh/h, 4)]
json.dump(out, open(f"{R}/plates/details.json", "w"), indent=1)
print(out)
