"""Shrink the content of given pages around the page centre so all ink sits inside the KDP safe area.
usage: fit_safe.py file.pdf scale page [page ...]"""
import fitz, sys
f, sc, pages = sys.argv[1], float(sys.argv[2]), [int(x) for x in sys.argv[3:]]
src = fitz.open(f); out = fitz.open()
for i in range(len(src)):
    if i + 1 not in pages:
        out.insert_pdf(src, from_page=i, to_page=i); continue
    p = src[i]
    pix = p.get_pixmap(dpi=20); c = pix.pixel(1, pix.height // 2)
    np_ = out.new_page(width=p.rect.width, height=p.rect.height)
    np_.draw_rect(np_.rect, color=None, fill=tuple(v / 255 for v in c[:3]))
    w, h = p.rect.width * sc, p.rect.height * sc
    x0, y0 = (p.rect.width - w) / 2, (p.rect.height - h) / 2
    np_.show_pdf_page(fitz.Rect(x0, y0, x0 + w, y0 + h), src, i)
out.save(f + ".tmp", garbage=4, deflate=True)
import os; os.replace(f + ".tmp", f)
print("ok", f)
