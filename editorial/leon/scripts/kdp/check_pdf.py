"""KDP preflight: trim+bleed size, page count, embedded fonts, effective image resolution (dpi at printed size)."""
import fitz, sys

IN = 72


def check(path):
    d = fitz.open(path)
    cover = "cover" in path
    pages = int(__import__('os').environ.get('PAGES', 80))
    want = (round(2 * 8.5 + .25 + pages * 0.002347, 4), 11.25) if cover else (8.625, 11.25)
    issues, low = [], []
    for i, p in enumerate(d):
        w, h = p.rect.width / IN, p.rect.height / IN
        if abs(w - want[0]) > .005 or abs(h - want[1]) > .01:
            issues.append(f"p{i + 1} size {w:.4f}x{h:.4f}")
        for info in p.get_image_info(xrefs=True):
            bb = fitz.Rect(info["bbox"]) & p.rect
            if bb.is_empty or bb.width < 20:
                continue
            dpi = min(info["width"] / (fitz.Rect(info["bbox"]).width / IN), info["height"] / (fitz.Rect(info["bbox"]).height / IN))
            if dpi < 300:
                low.append((i + 1, round(dpi)))
    fonts = {f[3]: f for p in d for f in p.get_fonts(full=True)}
    not_emb = [n for n, f in fonts.items() if (f[1] in ("", "n/a") and f[2] != "Type3") or not f[0]]
    n = len(d)
    if not cover and n != pages:
        issues.append(f"{n} pages (expected {pages})")
    print(f"{path.split('/')[-1]}: {n} p, {want[0]}x{want[1]} in, fonts {len(fonts)} (not embedded: {not_emb or 'none'}),"
          f" images <300dpi: {len(low)}" + (f" min {min(x[1] for x in low)} dpi" if low else "") + (f" | ISSUES: {issues}" if issues else ""))
    return low


if __name__ == "__main__":
    for f in sys.argv[1:]:
        check(f)
