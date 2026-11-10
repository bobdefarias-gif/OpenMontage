"""KDP live-area check: every text span and every drawing/image must be >= 0.375in from trim (36pt from PDF edge with bleed),
except full-bleed elements that touch the PDF edge (backgrounds)."""
import fitz, sys
S, W, H = 36, 621, 810
for f in sys.argv[1:]:
    d = fitz.open(f); bad = []
    for i, p in enumerate(d):
        for b in p.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    r = s["bbox"]
                    if s["text"].strip() and (r[0] < S or r[1] < S or r[2] > W - S or r[3] > H - S):
                        bad.append((i + 1, "text", s["text"][:20]))
        for dr in p.get_drawings():
            r = dr["rect"]
            bleed = r.x0 <= 1 or r.y0 <= 1 or r.x1 >= W - 1 or r.y1 >= H - 1
            if not bleed and (r.x0 < S or r.y0 < S or r.x1 > W - S or r.y1 > H - S):
                bad.append((i + 1, "draw", [round(v) for v in r]))
        for im in p.get_image_info():
            r = fitz.Rect(im["bbox"])
            bleed = r.x0 <= 1 or r.y0 <= 1 or r.x1 >= W - 1 or r.y1 >= H - 1
            if not bleed and (r.x0 < S or r.y0 < S or r.x1 > W - S or r.y1 > H - S):
                bad.append((i + 1, "image", [round(v) for v in r]))
    print(f.split("/")[-1], "OK" if not bad else bad[:12])
