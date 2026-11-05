"""Sample pages, V1 EN — 'Option B' (Robert's real artwork integrated, no frames).

KDP interior page: 8.625 x 11.25 in (621 x 810 pt) incl. 0.125 in bleed.
Safe zone 0.375 in from trim; we keep content >= 0.5 in from trim (= 45 pt from the PDF edge).
Recto pages (odd): spine on the left.
"""
import json, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(f"{R}/art/manifest.json"))
A = "../art"
INK, RED, OCHRE, MUTED, LINE = "#1F2A44", "#D5482F", "#E3A72F", "#7A8091", "#D9DDE6"
PW, PH = 621, 810
BLEED = 9
SAFE_OUT, SAFE_IN = 45 + 9, 45 + 9   # 0.5in work zone + bleed (+ a little air)

CSS = open(f"{R}/fonts/fonts.css").read() + f"""
@page {{ size: {PW}pt {PH}pt; margin: 0 }}
* {{ margin: 0; padding: 0; box-sizing: border-box }}
body {{ background: #777 }}
.page {{ width: {PW}pt; height: {PH}pt; position: relative; overflow: hidden; background: #fff; page-break-after: always;
        color: {INK}; font-family: 'Andika', sans-serif }}
.abs {{ position: absolute }}
h1 {{ font-family: 'Baloo 2', sans-serif; font-weight: 800; font-size: 31pt; line-height: 1; letter-spacing: -.2pt }}
.ins {{ font-size: 15pt; line-height: 1.28; margin-top: 7pt }}
.stars {{ display: flex; gap: 3pt }}
.foot {{ font-family: 'Lexend', sans-serif; font-size: 8.5pt; color: {MUTED}; letter-spacing: .2pt }}
.credit {{ font-family: 'Lexend', sans-serif; font-size: 8pt; color: {MUTED} }}
.lbl {{ font-family: 'Baloo 2', sans-serif; font-weight: 800; font-size: 19pt; color: {INK};
        width: 30pt; height: 30pt; border-radius: 50%; border: 2pt solid {INK}; display: flex; align-items: center; justify-content: center; line-height: 1; padding-top: 3pt }}
.lens {{ position: absolute; border-radius: 50%; box-shadow: 0 0 0 2.2pt #fff, 0 0 0 3.2pt {LINE} }}
.lens img {{ width: 100%; height: 100%; display: block; border-radius: 50% }}
"""


def star(on):
    c = OCHRE if on else "#E3E6EC"
    return (f'<svg width="21pt" height="21pt" viewBox="0 0 24 24"><path d="M12 2.2l2.9 6.3 6.9.7-5.2 4.6 1.5 6.8L12 17.1 5.9 20.6l1.5-6.8L2.2 9.2l6.9-.7z" '
            f'fill="{c}" stroke="{c}" stroke-width="1.6" stroke-linejoin="round"/></svg>')


def page(n, title, instr, level, skill, body, credit):
    recto = n % 2 == 1
    L = SAFE_IN if recto else SAFE_OUT
    Rr = SAFE_OUT if recto else SAFE_IN
    stars = "".join(star(i < level) for i in range(3))
    return f"""<section class="page">
  <div class="abs" style="left:{L}pt;right:{Rr + 80}pt;top:58pt"><h1>{title}</h1><div class="ins">{instr}</div></div>
  <div class="abs stars" style="right:{Rr}pt;top:62pt">{stars}</div>
  {body}
  <div class="abs credit" style="left:{L}pt;bottom:76pt">{credit}</div>
  <div class="abs foot" style="left:{L}pt;right:{Rr}pt;bottom:54pt;display:flex;justify-content:space-between">
    <span>{skill}</span><b style="color:{INK}">{n}</b></div>
</section>"""


def p10():
    n, recto = 10, False
    L, Rr = SAFE_OUT, SAFE_IN
    d, gap = 98, 22
    rows_top, rowh = 168, 128
    body = []
    total = 4 * d + 3 * gap
    x0 = L + 40 + ((PW - L - Rr - 40) - total) / 2
    for r in range(4):
        y = rows_top + r * rowh
        body.append(f'<div class="abs" style="left:{L}pt;top:{y + d / 2 - 14}pt;font-family:\'Baloo 2\';font-weight:800;font-size:20pt;color:{MUTED}">{r + 1}</div>')
        if r:
            body.append(f'<div class="abs" style="left:{L}pt;right:{Rr}pt;top:{y - 15}pt;border-top:1.2pt dashed {LINE}"></div>')
        for c in range(4):
            body.append(f'<div class="lens" style="left:{x0 + c * (d + gap)}pt;top:{y}pt;width:{d}pt;height:{d}pt"><img src="{A}/odd_r{r}_c{c}.png"></div>')
    return page(n, "Odd one out",
                "Three circles in each row come from the same painting. Circle the one with <b>different colors</b>.",
                2, "Attention &amp; Observation", "".join(body),
                "Details from paintings by Robert de Farias")


def p14():
    n = 14
    L, Rr = SAFE_OUT, SAFE_IN
    bw = PW - L - Rr
    m = M["bird"]
    bh = bw * m["h"] / m["w"]
    body = [f'<img class="abs" src="{A}/bird.png" style="left:{L}pt;top:170pt;width:{bw}pt">']
    opts = [("sh_creature", "A"), ("sh_bird_flip", "B"), ("sh_bird", "C")]
    cw = (bw - 2 * 10) / 3
    y = 170 + bh + 70
    body.append(f'<div class="abs" style="left:{L}pt;right:{Rr}pt;top:{y - 36}pt;border-top:1.2pt dashed {LINE}"></div>')
    for i, (k, lab) in enumerate(opts):
        mm = M[k]
        w = cw - 14
        h = w * mm["h"] / mm["w"]
        if h > 120: w, h = 120 * mm["w"] / mm["h"], 120
        x = L + i * (cw + 10)
        body.append(f'<div class="abs" style="left:{x}pt;top:{y}pt;width:{cw}pt;height:130pt;display:flex;align-items:center;justify-content:center">'
                    f'<img src="{A}/{k}.png" style="width:{w}pt;height:{h}pt;opacity:.92"></div>')
        body.append(f'<div class="abs lbl" style="left:{x + cw / 2 - 15}pt;top:{y + 146}pt">{lab}</div>')
    return page(n, "Find the shadow",
                "This is Robert’s bird. Which shadow belongs to it? Circle the letter.",
                2, "Attention &amp; Observation", "".join(body),
                "Robert de Farias, bird, watercolor on paper")


def p64():
    n = 64
    L, Rr = SAFE_OUT, SAFE_IN
    bw = PW - L - Rr
    m = M["painting12"]
    pw_ = bw * 0.86
    bh = pw_ * m["h"] / m["w"]
    top = 158
    body = [f'<img class="abs" src="{A}/painting12.png" style="left:{L + (bw - pw_) / 2}pt;top:{top}pt;width:{pw_}pt">']
    d = 104
    y = top + bh + 56
    opts = [("piece_d1", "A"), ("piece_true", "B"), ("piece_d2", "C")]
    sp = (bw - 3 * d) / 2
    body.append(f'<div class="abs" style="left:{L}pt;right:{Rr}pt;top:{y - 30}pt;border-top:1.2pt dashed {LINE}"></div>')
    for i, (k, lab) in enumerate(opts):
        x = L + i * (d + sp)
        body.append(f'<div class="lens" style="left:{x}pt;top:{y}pt;width:{d}pt;height:{d}pt"><img src="{A}/{k}.png"></div>')
        body.append(f'<div class="abs lbl" style="left:{x + d / 2 - 15}pt;top:{y + d + 14}pt">{lab}</div>')
    return page(n, "Where is this piece?",
                "Only one circle comes from this painting. Which one? Circle the letter.",
                3, "Spatial Thinking", "".join(body),
                "Robert de Farias, untitled, watercolor on paper")


def answers():
    """Answer key sample: thumbnail + red circle where the answer is a position in the art."""
    n = 77
    L, Rr = SAFE_IN, SAFE_OUT
    m = M["painting12"]; t = M["piece_true"]
    tw = 200; th = tw * m["h"] / m["w"]
    # piece position (plate coords) -> cutout coords -> thumbnail pt
    px = (t["cx"] * m["W"] - m["x0"]) / m["w"] * tw
    py = (t["cy"] * m["H"] - m["y0"]) / m["h"] * th
    pr = t["r"] * m["W"] / m["w"] * tw
    odd_pos = [2, 0, 3, 1]
    dots = "".join(
        f'<div style="display:flex;gap:5pt;align-items:center;margin:3pt 0"><span class="foot" style="width:10pt">{r + 1}</span>' +
        "".join(f'<span style="width:13pt;height:13pt;border-radius:50%;background:{"#fff" if c == p else "#C9CED8"};border:{"2.2pt solid " + RED if c == p else "0"}"></span>' for c in range(4)) +
        "</div>" for r, p in enumerate(odd_pos))

    def row(pg, title, ans, extra=""):
        return (f'<div style="display:flex;gap:16pt;padding:13pt 0;border-top:1pt solid {LINE};align-items:flex-start">'
                f'<div class="foot" style="width:34pt;color:{INK};font-weight:600">p. {pg}</div>'
                f'<div style="flex:1"><div style="font-family:\'Baloo 2\';font-weight:700;font-size:13pt">{title}</div>'
                f'<div style="font-size:11.5pt;line-height:1.3">{ans}</div></div>{extra}</div>')
    thumb = (f'<div style="position:relative;width:{tw}pt;height:{th}pt"><img src="{A}/painting12.png" style="width:100%;height:100%">'
             f'<div style="position:absolute;left:{px - pr}pt;top:{py - pr}pt;width:{2 * pr}pt;height:{2 * pr}pt;border-radius:50%;border:3.4pt solid {RED};box-shadow:0 0 0 2pt #fff, inset 0 0 0 1.5pt #fff"></div></div>')
    sh = (f'<div style="display:flex;gap:8pt;align-items:flex-end">'
          f'<img src="{A}/sh_bird.png" style="width:70pt"><span class="lbl" style="border-color:{RED};color:{RED};width:24pt;height:24pt;font-size:14pt">C</span></div>')
    body = (f'<div class="abs" style="left:{L}pt;right:{Rr}pt;top:150pt">'
            + row(10, "Odd one out", "Row 1: third · Row 2: first · Row 3: fourth · Row 4: second.", f"<div>{dots}</div>")
            + row(14, "Find the shadow", "C — the bird standing the right way up.", sh)
            + row(64, "Where is this piece?", "B — it is here, in the top right of the painting.", thumb)
            + "</div>")
    return page(n, "Answers for grown-ups", "Each answer can be checked in a few seconds. Red circles show where to look.",
                0, "Answers", body, "").replace('<div class="abs stars"', '<div class="abs stars" style="display:none"')


if __name__ == "__main__":
    os.makedirs(f"{R}/build", exist_ok=True)
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{p10()}{p14()}{p64()}{answers()}</body></html>'
    open(f"{R}/build/samples-v1-en.html", "w").write(html)
    print("ok")
