"""Compose trimmed spread previews (contact sheet per volume) from pdftoppm page JPEGs."""
import glob, os, sys
from PIL import Image, ImageDraw

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B, PW, PH = 3, 306, 246


def trim(im):
    w, h = im.size
    dx, dy = w * B / PW, h * B / PH
    return im.crop((round(dx), round(dy), round(w - dx), round(h - dy)))


def sheet(prefix, out, cols=2, gap=24, bg=(52, 50, 47)):
    pages = [trim(Image.open(f).convert("RGB")) for f in sorted(glob.glob(f"{R}/build/prev/{prefix}-*.jpg"))]
    pw, ph = pages[0].size
    spreads = [[None, pages[0]]] + [pages[i:i + 2] for i in range(1, len(pages), 2)]
    rows = (len(spreads) + cols - 1) // cols
    S = Image.new("RGB", (cols * (2 * pw) + (cols + 1) * gap, rows * ph + (rows + 1) * gap), bg)
    for i, sp in enumerate(spreads):
        x0 = gap + (i % cols) * (2 * pw + gap)
        y0 = gap + (i // cols) * (ph + gap)
        for j, p in enumerate(sp):
            if p is not None:
                S.paste(p, (x0 + j * pw, y0))
        d = ImageDraw.Draw(S)
        d.line([(x0 + pw, y0), (x0 + pw, y0 + ph)], fill=(0, 0, 0), width=1)
    S.save(out, quality=88)
    return out


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(sheet(p, f"{R}/build/{p}-spreads.jpg"))
