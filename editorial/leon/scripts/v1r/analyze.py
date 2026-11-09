"""Measure every original V1 page: instruction bottom, activity-content bbox, 'For grown-ups' boxes."""
import fitz, json, sys
SRC = sys.argv[1] if len(sys.argv) > 1 else "ref/leons-thinking-book-vol1-EN-interior.pdf"
d = fitz.open(SRC)
out = {}
for pn in range(1, 81):
    p = d[pn - 1]
    spans = [s for b in p.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]
    head = [s for s in spans if s["size"] in (33.0, 18.0) and s["bbox"][1] < 175]
    hb = max([s["bbox"][3] for s in head], default=40)
    items = [fitz.Rect(s["bbox"]) for s in spans if s["bbox"][1] > hb + 1 and s["bbox"][3] < 752]
    for dr in p.get_drawings():
        r = dr["rect"]
        if r.width > 600 and r.height > 780:
            continue
        if r.y0 > hb + 1 and r.y1 < 752:
            items.append(r)
    bb = fitz.Rect()
    for r in items:
        bb |= r
    gu = []
    for b in p.get_text("dict")["blocks"]:
        txt = " ".join(s["text"] for l in b.get("lines", []) for s in l["spans"])
        if txt.strip().startswith("For grown-ups"):
            gu.append({"rect": list(fitz.Rect(b["bbox"])), "text": txt.strip()})
    out[pn] = {"head_bottom": round(hb, 1), "content": [round(v, 1) for v in bb] if not bb.is_empty else None, "grownups": gu}
json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else "build/v1r_geom.json", "w"), indent=0)
for pn in range(8, 76):
    o = out[pn]
    print(pn, o["head_bottom"], o["content"], "GU" if o["grownups"] else "")
