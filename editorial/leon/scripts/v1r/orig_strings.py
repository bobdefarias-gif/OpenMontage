"""Extract original title / instruction / footer-skill of every V1 page, per language."""
import fitz, json
out = {}
for L in ("EN", "FR", "NL"):
    d = fitz.open(f"ref/leons-thinking-book-vol1-{L}-interior.pdf")
    for pn in range(8, 75):
        p = d[pn - 1]
        sp = [s for b in p.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]
        title = " ".join(s["text"].strip() for s in sp if s["size"] >= 20 and s["bbox"][1] < 85)
        ins = " ".join(s["text"].strip() for s in sp if 14 <= s["size"] < 20 and 85 <= s["bbox"][1] < 175)
        foot = " ".join(s["text"].strip() for s in sp if s["bbox"][1] > 755 and not s["text"].strip().isdigit())
        out.setdefault(str(pn), {})[L] = {"title": title, "ins": ins, "foot": foot}
json.dump(out, open("build/v1_orig_strings.json", "w"), ensure_ascii=False, indent=0)
