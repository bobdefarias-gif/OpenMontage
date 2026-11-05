"""Compose the final KDP interiors: original interior + art-map overlays + text fixes + rebuilt answer key.

usage: python compose.py V1 EN [FR NL]
- art pages: the original activity area is redacted (stars + footer kept) and the art overlay is stamped
- 'Brain Challenge' -> 'Big Challenge' (EN), honest sales sentence on p.4 (all languages)
- answer key pp.76-79 rebuilt from the original entries, with the new answers + a picture answer (thumbnail + red circle)
"""
import fitz, json, os, re, subprocess, sys, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import v1_art_pages as V1
import v2_art_pages as V2

NAVY, GRAY, RED, BODY, LINE, BG = "#1E2A5A", "#5F6B78", "#E0533D", "#33405F", "#E3E7EC", (0.957, 0.969, 0.980)
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJAVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
OUT = f"{R}/build/kdp"
os.makedirs(OUT, exist_ok=True)

P4 = {
    "EN": ("<i>Leon’s Thinking Book</i> is a playful activity book for children aged 4 to 6. "
           "Many of the games are made with real artworks by Robert de Farias: his lines, his colors and his paintings."),
    "FR": ("<i>Leon’s Thinking Book</i> est un cahier d’activités ludiques pour les enfants de 4 à 6 ans. "
           "Beaucoup de jeux sont faits avec de vraies œuvres de Robert de Farias : ses lignes, ses couleurs et ses peintures."),
    "NL": ("<i>Leon’s Thinking Book</i> is een speels doeboek voor kinderen van 4 tot 6 jaar. "
           "Veel spelletjes zijn gemaakt met echte kunstwerken van Robert de Farias: zijn lijnen, zijn kleuren en zijn schilderijen."),
}
PICTURE = {"EN": "Picture answers", "FR": "Réponses en images", "NL": "Antwoorden in beeld"}


def render(html_path, pdf_path):
    subprocess.run(["node", f"{R}/scripts/render.js", html_path, pdf_path], check=True)


def page_html(body_pages):
    css = ("@page{size:621pt 810pt;margin:0}*{margin:0;padding:0;box-sizing:border-box}html,body{background:transparent}"
           ".page{width:621pt;height:810pt;position:relative;overflow:hidden;page-break-after:always}")
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(body_pages)}</body></html>'


def redact(page, rects):
    for r in rects:
        page.add_redact_annot(fitz.Rect(*r), fill=BG if page_bg(page) else (1, 1, 1))
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_REMOVE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED,
                          text=fitz.PDF_REDACT_TEXT_REMOVE)


def page_bg(page):
    for d in page.get_drawings()[:2]:
        if d.get("fill") and abs(d["rect"].width - 621) < 1 and abs(d["fill"][0] - BG[0]) < .01:
            return True
    return False


# ----------------------------------------------------------------------------- answer key
GEO = {1: dict(lab=63, title=114, ans=274.5, size=10.9, top=112, ymin=110, right=567),
       2: dict(lab=48, title=94, ans=246, size=9.75, top=88, ymin=85, right=573)}


def parse_answers(doc, first=76, last=79, g=GEO[1]):
    rows = []
    for pn in range(first - 1, last):
        spans = [s for b in doc[pn].get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"]
                 if g["ymin"] < s["bbox"][1] < 750]
        spans.sort(key=lambda s: (round(s["bbox"][1]), s["bbox"][0]))
        cur = None
        for s in spans:
            x, t = s["bbox"][0], s["text"]
            if x < g["title"] - 10 and re.match(r"p\.\s*\d+", t.strip()):
                cur = {"p": int(re.findall(r"\d+", t)[0]), "title": "", "ans": ""}
                rows.append(cur)
            elif cur is not None and g["title"] - 10 <= x < g["ans"] - 10:
                cur["title"] += (" " if cur["title"] else "") + t.strip()
            elif cur is not None and x >= g["ans"] - 10:
                cur["ans"] += (" " if cur["ans"] else "") + t.strip()
    return rows


def est_lines(s, chars):
    words, n, cur = s.split(), 1, 0
    for w in words:
        if cur + len(w) + (1 if cur else 0) > chars:
            n += 1; cur = len(w)
        else:
            cur += len(w) + (1 if cur else 0)
    return n


def answer_pages(rows, lang, vol, size=None):
    g = GEO[vol]; size = size or g["size"]
    """Lay out rows on pages 76-79 (same columns/typography as the original). Returns list of 4 html bodies."""
    pages, cur, y = [], [], 0
    top = {i: g["top"] for i in range(12)}
    limit = 740
    for r in rows:
        tw, aw = g["ans"] - g["title"] - 8, g["right"] - g["ans"]
        h = max(est_lines(r["title"], int(tw / (size * .66))), est_lines(r["ans"], int(aw / (size * .58)))) * size * 1.3 + 9
        if top[len(pages)] + y + h > limit:
            pages.append(cur); cur, y = [], 0
        cur.append((r, y, h)); y += h
    pages.append(cur)
    bodies = []
    for i, items in enumerate(pages):
        t = top[min(i, 3)]
        out = []
        for r, yy, h in items:
            out.append(f'<div style="position:absolute;left:{g["lab"]}pt;width:{g["right"] - g["lab"]}pt;top:{t + yy}pt;height:{h}pt;border-top:.75pt solid {LINE};padding-top:5pt;'
                       f'display:flex;font:{size}pt/{size * 1.3:.1f}pt \'DejaVu Sans\'">'
                       f'<div style="width:{g["title"] - g["lab"]}pt;color:{RED};font-weight:bold">p. {r["p"]}</div>'
                       f'<div style="width:{g["ans"] - g["title"]}pt;color:{NAVY};font-weight:bold;padding-right:8pt">{H.escape(r["title"])}</div>'
                       f'<div style="flex:1;color:{BODY}">{H.escape(r["ans"])}</div></div>')
        bodies.append((out, t + (items[-1][1] + items[-1][2] if items else 0)))
    return bodies


def picture_answers(lang, y0):
    """Thumbnail + red circle for answers that are a position in the art (V1: p.64)."""
    m, t = V1.MAN["painting12"], V1.MAN["piece_true"]
    tw = 180; th = tw * m["h"] / m["w"]
    px = (t["cx"] * m["W"] - m["x0"]) / m["w"] * tw
    py = (t["cy"] * m["H"] - m["y0"]) / m["h"] * th
    pr = t["r"] * m["W"] / m["w"] * tw
    return (f'<div style="position:absolute;left:63pt;top:{y0 + 16}pt;font:bold 13pt \'DejaVu Sans\';color:{NAVY}">{PICTURE[lang]}</div>'
            f'<div style="position:absolute;left:63pt;top:{y0 + 44}pt;display:flex;gap:18pt;align-items:flex-start;font:10.9pt/14.6pt \'DejaVu Sans\'">'
            f'<div style="width:51pt;color:{RED};font-weight:bold">p. 64</div>'
            f'<div style="position:relative;width:{tw}pt;height:{th}pt"><img src="{V1.A}/painting12.png" style="width:100%;height:100%;display:block">'
            f'<div style="position:absolute;left:{px - pr}pt;top:{py - pr}pt;width:{2 * pr}pt;height:{2 * pr}pt;border-radius:50%;'
            f'border:3.2pt solid {RED};box-shadow:0 0 0 1.6pt #fff"></div></div>'
            f'<div style="width:220pt;color:{BODY}">{H.escape(V1.ANSWERS[64][lang])}</div></div>')


# ----------------------------------------------------------------------------- main
def build_v1(lang):
    src = f"{R}/ref/leons-thinking-book-vol1-{lang}-interior.pdf"
    doc = fitz.open(src)
    tag = f"v1-{lang}"

    # 1) art overlays
    hp = f"{OUT}/v1-art-{lang}.html"
    open(hp, "w").write(V1.html(lang))
    render(hp, f"{OUT}/v1-art-{lang}.pdf")
    ov = fitz.open(f"{OUT}/v1-art-{lang}.pdf")
    for i, n in enumerate(V1.PAGES):
        page = doc[n - 1]
        sx0, sx1 = (468, 567) if n % 2 else (477, 576)
        redact(page, [(0, 0, sx0 - 4, 86), (sx1 + 4, 0, 621, 86), (sx0 - 4, 0, sx1 + 4, 47), (sx0 - 4, 79, sx1 + 4, 86),
                      (0, 86, 621, 757)])
        page.show_pdf_page(page.rect, ov, i)

    # 2) answer key: rebuild pp.76-79
    rows = parse_answers(doc)
    by_p = {r["p"]: r for r in rows}
    for n, ans in V1.ANSWERS.items():
        title = V1.T[n][lang][0]
        if n in by_p:
            by_p[n]["ans"], by_p[n]["title"] = ans[lang], title
        else:
            rows.append({"p": n, "title": title, "ans": ans[lang]})
    rows.sort(key=lambda r: r["p"])
    bodies = answer_pages(rows, lang, 1)
    assert len(bodies) <= 4, f"answer key overflows: {len(bodies)} pages"
    while len(bodies) < 4:
        bodies.append(([], 112))
    out, end = bodies[-1]
    out.append(picture_answers(lang, end))
    hp = f"{OUT}/v1-answers-{lang}.html"
    open(hp, "w").write(page_html([f'<section class="page">{"".join(b)}</section>' for b, _ in bodies]))
    render(hp, f"{OUT}/v1-answers-{lang}.pdf")
    ova = fitz.open(f"{OUT}/v1-answers-{lang}.pdf")
    for i in range(4):
        page = doc[75 + i]
        redact(page, [(0, 108, 621, 752)])
        page.show_pdf_page(page.rect, ova, i)

    # 3) p.4 honest sales sentence (first paragraph)
    p4 = doc[3]
    redact(p4, [(70, 112, 580, 200)])
    hp = f"{OUT}/v1-p4-{lang}.html"
    open(hp, "w").write(page_html([f'<section class="page"><div style="position:absolute;left:81pt;top:119pt;width:470pt;'
                                   f'font:14.2pt/20.6pt \'DejaVu Sans\';color:{NAVY}">{P4[lang]}</div></section>']))
    render(hp, f"{OUT}/v1-p4-{lang}.pdf")
    p4.show_pdf_page(p4.rect, fitz.open(f"{OUT}/v1-p4-{lang}.pdf"), 0)

    # 4) 'Brain Challenge' -> 'Big Challenge'
    fix_brain(doc)

    dst = f"{OUT}/leons-thinking-book-vol1-{lang}-interior.pdf"
    doc.save(dst, garbage=4, deflate=True)
    return dst


def fix_brain(doc):
    for page in doc:
        hits = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if "Brain Challenge" in s["text"]:
                        hits.append(s)
        if not hits:
            continue
        for s in hits:
            page.add_redact_annot(fitz.Rect(s["bbox"]), fill=False)
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
        for s in hits:
            new = s["text"].replace("Brain Challenge", "Big Challenge")
            bold = "Bold" in s["font"]
            fname, ffile = ("djb", DEJAVU_B) if bold else ("dj", DEJAVU)
            c = s["color"]; col = ((c >> 16) / 255, ((c >> 8) & 255) / 255, (c & 255) / 255)
            x0, x1 = s["bbox"][0], s["bbox"][2]
            f = fitz.Font(fontfile=ffile)
            w_old, w_new = f.text_length(s["text"], s["size"]), f.text_length(new, s["size"])
            # keep centred labels centred, left-aligned labels left-aligned
            x = x0 + (w_old - w_new) / 2 if x0 > 200 else x0
            page.insert_text((x, s["origin"][1]), new, fontname=fname, fontfile=ffile, fontsize=s["size"], color=col)


def build_v2(lang):
    doc = fitz.open(f"{R}/ref/leons-thinking-book-vol2-{lang}-interior.pdf")
    hp = f"{OUT}/v2-art-{lang}.html"
    open(hp, "w").write(V2.html(lang))
    render(hp, f"{OUT}/v2-art-{lang}.pdf")
    ov = fitz.open(f"{OUT}/v2-art-{lang}.pdf")
    for i, n in enumerate(V2.PAGES):
        page = doc[n - 1]
        sx0, sx1 = (468, 567) if n % 2 else (477, 576)
        redact(page, [(0, 0, sx0 - 4, 86), (sx1 + 4, 0, 621, 86), (sx0 - 4, 0, sx1 + 4, 47), (sx0 - 4, 79, sx1 + 4, 86),
                      (0, 86, 621, 757)])
        page.show_pdf_page(page.rect, ov, i)
    rows = parse_answers(doc, 77, 79, GEO[2])
    by_p = {r["p"]: r for r in rows}
    for n, ans in V2.ANSWERS.items():
        title = V2.T[n][lang][0]
        if n in by_p:
            by_p[n]["ans"], by_p[n]["title"] = ans[lang], title
        else:
            rows.append({"p": n, "title": title, "ans": ans[lang]})
    rows.sort(key=lambda r: r["p"])
    for size in (9.75, 9.4, 9.0):
        bodies = answer_pages(rows, lang, 2, size)
        if len(bodies) <= 3: break
    assert len(bodies) <= 3, "V2 answer key overflows"
    while len(bodies) < 3: bodies.append(([], 88))
    hp = f"{OUT}/v2-answers-{lang}.html"
    open(hp, "w").write(page_html([f'<section class="page">{"".join(b)}</section>' for b, _ in bodies]))
    render(hp, f"{OUT}/v2-answers-{lang}.pdf")
    ova = fitz.open(f"{OUT}/v2-answers-{lang}.pdf")
    for i in range(3):
        page = doc[76 + i]
        redact(page, [(0, 84, 621, 752)])
        page.show_pdf_page(page.rect, ova, i)
    fix_brain(doc)
    dst = f"{OUT}/leons-thinking-book-vol2-{lang}-interior.pdf"
    doc.save(dst, garbage=4, deflate=True)
    return dst


if __name__ == "__main__":
    vol, langs = sys.argv[1], sys.argv[2:] or ["EN", "FR", "NL"]
    for lang in langs:
        print(build_v1(lang) if vol == "V1" else build_v2(lang))
