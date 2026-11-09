"""Build the revised V1 EN interior (96 pages) — reuses the ORIGINAL vector artwork, new typography/layout.

python scripts/v1r/build.py  ->  build/v2r/leons-thinking-book-vol1-EN-interior-revised.pdf
"""
import fitz, json, os, sys, subprocess, html as H, re, copy

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from spec import ISLANDS, ACT, OPENERS, OPENER_TITLES, ORIG_TO_NEW
import pages_html
from pages_html import html_pages
import i18n
LANG = os.environ.get("V2R_LANG", "EN")
pages_html.set_lang(LANG)

SRC = f"{R}/ref/leons-thinking-book-vol2-{os.environ.get('V2R_LANG', 'EN')}-interior.pdf"
OUT = f"{R}/build/v2r/{os.environ.get('V2R_LANG', 'EN')}"
FT = f"{R}/fonts/ttf"
F_REG, F_BOLD, F_TITLE = f"{FT}/Andika-Regular.ttf", f"{FT}/Andika-Bold.ttf", f"{FT}/Baloo2-800.ttf"
BG = (0.957, 0.969, 0.980)
SCALE = {}
os.makedirs(OUT, exist_ok=True)

src = fitz.open(SRC)
FONTS = {k: fitz.Font(fontfile=v) for k, v in {"reg": F_REG, "bold": F_BOLD, "title": F_TITLE}.items()}


def spans_of(page):
    return [s for b in page.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]


def gu_rects(page):
    """'For grown-ups' blocks -> rect of the surrounding card."""
    out = []
    cards = [d["rect"] for d in page.get_drawings() if d.get("fill") and d["rect"].width > 200 and d["rect"].height < 120]
    for b in page.get_text("dict")["blocks"]:
        txt = " ".join(s["text"] for l in b.get("lines", []) for s in l["spans"])
        if txt.strip().startswith(("For grown-ups", "Pour l’adulte", "Voor volwassenen")):
            r = fitz.Rect(b["bbox"])
            box = [c for c in cards if c.contains(r)]
            out.append((min(box, key=lambda c: c.get_area()) if box else r) + (-5, -5, 5, 5))
    return out


def restyle(doc, pno, header_bottom=None, replace=None, drop=(), keep_header=False, extra_redact=()):
    """Re-set all text of page pno in Andika (vector art untouched). Removes header/footer text when header_bottom given."""
    replace = replace or {}
    page = doc[pno]
    sp = spans_of(page)
    gus = gu_rects(page)
    GU_CACHE[(id(doc), pno)] = gus
    keep = []
    for s in sp:
        r = fitz.Rect(s["bbox"])
        if any(g.intersects(r) for g in gus):
            continue
        if header_bottom is not None and (r.y1 <= header_bottom + 1 or r.y0 >= 752):
            continue
        if s["text"].strip() in drop:
            continue
        keep.append(s)
    for s in sp:
        page.add_redact_annot(fitz.Rect(s["bbox"]), fill=False)
    for g in gus:
        page.add_redact_annot(g, fill=BG)
    for r in extra_redact:
        page.add_redact_annot(fitz.Rect(r), fill=BG)
    if header_bottom is not None:      # old asterisk stars + header icons area
        for r in [(440, 40, 600, 82)]:
            page.add_redact_annot(fitz.Rect(r), fill=False)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                          text=fitz.PDF_REDACT_TEXT_REMOVE)
    for s in keep:
        t = s["text"].strip()
        t = replace.get(t, replace.get(t.replace("\u202f", " "), t)).replace("\u202f", "\u00a0")
        bold = "Bold" in s["font"] or "Oblique" in s["font"] and False
        big = s["size"] >= 22
        key = "title" if big else ("bold" if "Bold" in s["font"] else "reg")
        f = FONTS[key]
        size = s["size"] * (1.0 if key != "title" else 1.02)
        x0, x1 = s["bbox"][0], s["bbox"][2]
        w_old = x1 - x0
        w_new = f.text_length(t, size)
        if w_new > w_old * 1.12 and len(t) > 3:
            size *= (w_old * 1.12) / w_new
            w_new = f.text_length(t, size)
        x = x0 + (w_old - w_new) / 2
        c = s["color"]
        col = ((c >> 16) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255)
        page.insert_text((x, s["origin"][1]), t, fontname=key, fontfile={"title": F_TITLE, "bold": F_BOLD, "reg": F_REG}[key],
                         fontsize=size, color=col)
    return page


GU_CACHE = {}


def content_bottom(page, top=150, gus=()):
    ys = [d["rect"].y1 for d in page.get_drawings() if top < d["rect"].y0 and d["rect"].y1 < 752 and d["rect"].width < 600
          and not any((g + (-2, -2, 2, 2)).contains(d["rect"]) for g in gus)]
    ys += [s["bbox"][3] for s in spans_of(page) if top < s["bbox"][1] < 752]
    return max(ys) if ys else top


def render(html_path, pdf_path):
    subprocess.run(["node", f"{R}/scripts/render.js", html_path, pdf_path], check=True)


def main():
    gp = f"{R}/build/v2r_geom_{LANG}.json"
    if not os.path.exists(gp):
        subprocess.run([sys.executable, f"{HERE}/analyze.py", SRC, gp], check=True, capture_output=True)
    geom = json.load(open(gp))
    work = fitz.open(SRC)            # restyled copy
    pristine = fitz.open(SRC)        # untouched (for stamps)
    act = {a[0]: a for a in ACT}

    # ---------- restyle the original activity pages
    special = {73: dict(replace={"75!": "90!", "75 !": "90 !", "page 75!": "page 90!"})}
    bottoms = {}
    for new, a in act.items():
        o = a[1] - 1
        hb = geom[str(a[1])]["head_bottom"]
        restyle(work, o, header_bottom=hb, **special.get(a[1], {}))
        bottoms[new] = content_bottom(work[o], hb, GU_CACHE.get((id(work), o), ()))
        sc = None
        if a[6]:
            bw = 527
            need = pages_html.box_height(a[6][1], bw)
            if bottoms[new] + 16 + need > 740:
                sc = (740 - need - 16 - (hb + 4)) / (bottoms[new] + 3 - (hb + 4))
                sc = sc if sc >= 0.80 else None
        if sc:
            top = hb + 4
            bot = bottoms[new] + 3
            tmp = fitz.open()
            pg = tmp.new_page(width=621, height=810)
            pg.draw_rect(pg.rect, color=None, fill=BG)
            w_ = 621 * sc
            pg.show_pdf_page(fitz.Rect((621 - w_) / 2, top, (621 + w_) / 2, top + (bot - top) * sc), work, o,
                             clip=fitz.Rect(0, top, 621, bot))
            work.delete_page(o)
            work.insert_pdf(tmp, start_at=o)
            bottoms[new] = top + (bot - top) * sc
    # full-page restyles
    restyle(work, 2)                                                       # p.3 explorer card
    TRACK = i18n.TRACK[LANG]
    restyle(work, 5, replace=TRACK)                                        # mission tracker
    restyle(work, 6, replace=TRACK)                                        # mission map
    restyle(work, 75, replace=i18n.CERT2[LANG])                            # certificate
    restyle(work, 79)                                                      # series page

    # ---------- HTML pages / overlays
    hp = f"{OUT}/pages.html"
    open(hp, "w").write(html_pages(bottoms))
    render(hp, f"{OUT}/pages.pdf")
    ov = fitz.open(f"{OUT}/pages.pdf")
    assert len(ov) == 96, len(ov)

    out = fitz.open()
    full = {3: 3, 8: 6, 9: 7, 91: 76, 96: 80}
    for n in range(1, 97):
        if n in act:
            out.insert_pdf(work, from_page=act[n][1] - 1, to_page=act[n][1] - 1)
        elif n in full:
            out.insert_pdf(work, from_page=full[n] - 1, to_page=full[n] - 1)
        else:
            out.insert_pdf(ov, from_page=n - 1, to_page=n - 1)
            continue
        out[-1].show_pdf_page(out[-1].rect, ov, n - 1)

    # ---------- vector stamps
    def stamp(page_no, src_doc, src_pno, clip, dest):
        out[page_no - 1].show_pdf_page(fitz.Rect(dest), src_doc, src_pno, clip=fitz.Rect(clip))

    # p.1 / p.6 / openers: Leon (without Luz) and Luz from the original title page
    leon_src = fitz.open(SRC)
    lp = leon_src[0]
    for s in spans_of(lp):
        lp.add_redact_annot(fitz.Rect(s["bbox"]), fill=False)
    lp.add_redact_annot(fitz.Rect(430, 172, 540, 282), fill=False)
    lp.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED)
    LEON, LUZ = (108, 186, 528, 636), (430, 172, 540, 282)
    ll_src = fitz.open(SRC)                 # title page without any text (Leon + Luz)
    for s_ in spans_of(ll_src[0]):
        ll_src[0].add_redact_annot(fitz.Rect(s_["bbox"]), fill=False)
    ll_src[0].apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    from pages_html import STAMPS
    for (pg, who, rect) in STAMPS:
        if who == "leon":
            stamp(pg, leon_src, 0, LEON, rect)
        elif who == "luz":
            stamp(pg, ll_src, 0, LUZ, rect)
        elif who == "leonluz":
            stamp(pg, ll_src, 0, (108, 172, 540, 636), rect)
        elif who.startswith("orig:"):                      # orig:<page>:<x0,y0,x1,y1>
            _, opg, clip = who.split(":")
            stamp(pg, work, int(opg) - 1, tuple(map(float, clip.split(","))), rect)

    dst = f"{OUT}/leons-thinking-book-vol2-{LANG}-interior-revised.pdf"
    out.save(dst, garbage=4, deflate=True)
    print(dst, len(out))


if __name__ == "__main__":
    main()
