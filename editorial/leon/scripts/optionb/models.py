"""Option B — model pages for the reformulated books (V1 EN). New visual system, every activity built from the artwork.

Page 8.625 x 11.25 in (621 x 810 pt) incl. bleed; content >= 0.5 in inside the trim (45 pt from PDF edge).
Typography: Baloo 2 (titles), Andika (instructions), Lexend (labels/footer). Island colours sampled from the paintings.
"""
import json, os, math, html as H

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART, ARTB = f"file://{R}/art", f"file://{R}/art_b"
MAN = json.load(open(f"{R}/art/manifest.json"))
MB = json.load(open(f"{R}/art_b/manifest.json"))
PW, PH, M = 621, 810, 54
INK, MUTED, LINE, PAPER = "#1C2340", "#6A7183", "#E4E1DA", "#FFFFFF"
ISLAND = {  # name, colour (sampled from the artworks)
    "look": ("Look closely", "#D9462B"), "remember": ("Remember", "#2F49B5"), "shapes": ("Shapes", "#C98A12"),
    "patterns": ("Patterns", "#2E8B57"), "logic": ("Logic", "#8E5530"), "numbers": ("Numbers", "#17808F"),
    "words": ("Words", "#B83466"), "space": ("Space", "#3B82C4"), "feelings": ("Feelings", "#D9A21B"),
    "big": ("Big Challenge", "#1C2340")}

CSS = open(f"{R}/fonts/fonts.css").read().replace("../fonts/", f"file://{R}/fonts/") + f"""
@page {{ size: {PW}pt {PH}pt; margin: 0 }}
* {{ margin: 0; padding: 0; box-sizing: border-box }}
body {{ background: #888 }}
.page {{ width: {PW}pt; height: {PH}pt; position: relative; overflow: hidden; background: {PAPER}; page-break-after: always;
        color: {INK}; font-family: 'Andika', sans-serif }}
.a {{ position: absolute }}
.pill {{ font: 600 8.5pt 'Lexend'; letter-spacing: 1.4pt; text-transform: uppercase; color: #fff; padding: 4pt 10pt 3.5pt; border-radius: 20pt }}
h1 {{ font: 800 31pt/1 'Baloo 2'; letter-spacing: -.3pt }}
.ins {{ font: 16pt/1.3 'Andika'; margin-top: 6pt }}
.lens {{ position: absolute; border-radius: 50%; overflow: hidden; box-shadow: 0 0 0 3pt #fff, 0 0 0 4.2pt {LINE}, 0 4pt 10pt rgba(28,35,64,.10) }}
.lens img {{ width: 100%; height: 100%; object-fit: cover; display: block }}
.foot {{ font: 400 8.5pt 'Lexend'; color: {MUTED} }}
.num {{ font: 700 11pt 'Lexend'; color: #fff; width: 28pt; height: 28pt; border-radius: 50%; display: flex; align-items: center; justify-content: center }}
.lbl {{ font: 800 18pt 'Baloo 2'; width: 32pt; height: 32pt; border-radius: 50%; border: 2.4pt solid {INK}; display: flex; align-items: center; justify-content: center; padding-top: 3pt; background: #fff }}
.word {{ font: 800 26pt 'Baloo 2'; letter-spacing: 1pt }}
"""


def star(on, col):
    c = col if on else "#E6E3DC"
    return (f'<svg width="20pt" height="20pt" viewBox="0 0 24 24"><path d="M12 2.4l2.8 6.2 6.8.7-5.1 4.6 1.5 6.7L12 17.2 6 20.6l1.5-6.7L2.4 9.3l6.8-.7z" '
            f'fill="{c}" stroke="{c}" stroke-width="1.8" stroke-linejoin="round"/></svg>')


def page(n, island, title, ins, level, body, leon=False, full_bleed=False):
    name, col = ISLAND[island]
    L = M + (8 if n % 2 else 0)            # a little more room on the spine side
    Rr = M + (0 if n % 2 else 8)
    head_bg = ("background:rgba(255,255,255,.93);border-radius:16pt;padding:14pt 16pt 14pt;box-shadow:0 4pt 16pt rgba(0,0,0,.12)"
               if full_bleed else "")
    leon_img = (f'<img class="a" src="{ARTB}/leon.png" style="right:{Rr - 4}pt;top:92pt;width:62pt">' if leon else "")
    side = "right" if n % 2 else "left"
    return f"""<section class="page">{body}
  <div class="a" style="left:{L - (16 if full_bleed else 0)}pt;right:{Rr - (16 if full_bleed else 0)}pt;top:{40 if full_bleed else 46}pt;{head_bg}">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span class="pill" style="background:{col}">{name}</span>
      <span style="display:flex;gap:2pt">{''.join(star(i < level, col) for i in range(3))}</span></div>
    <h1 style="margin-top:12pt">{title}</h1>
    <div class="ins" style="max-width:{PW - L - Rr - (70 if leon else 0)}pt">{ins}</div>
  </div>{leon_img}
  <div class="a foot" style="left:{L}pt;right:{Rr}pt;bottom:40pt;display:flex;justify-content:space-between;align-items:center;flex-direction:{'row' if n % 2 else 'row-reverse'}">
    <span>Art: Robert de Farias</span><span class="num" style="background:{col}">{n}</span></div>
</section>"""


def lens(k, x, y, d):
    return f'<div class="lens" style="left:{x:.1f}pt;top:{y:.1f}pt;width:{d}pt;height:{d}pt"><img src="{ART}/{k}.jpg"></div>'


def dot(x, y, col=INK, r=5):
    return f'<div class="a" style="left:{x - r}pt;top:{y - r}pt;width:{2 * r}pt;height:{2 * r}pt;border-radius:50%;background:{col}"></div>'


def fit(k, bw, bh, man=MAN):
    m = man[k]; a = m["w"] / m["h"]
    return (bw, bw / a) if bw / a <= bh else (bh * a, bh)


# --------------------------------------------------------------------------------------------- models
PAIRS = ["tile_blue", "tile_red", "tile_honey", "tile_green"]
RIGHT = ["tile_honey", "tile_blue", "tile_green", "tile_red"]


def m_pairs(n=9):
    L, Rr = M, M + 8
    d, top, gap = 104, 205, 22
    out = []
    for i, (a, b) in enumerate(zip(PAIRS, RIGHT)):
        y = top + i * (d + gap)
        out += [lens(a, L + 20, y, d), dot(L + 20 + d + 26, y + d / 2), dot(PW - Rr - 20 - d - 26, y + d / 2), lens(b, PW - Rr - 20 - d, y, d)]
    return page(n, "look", "Same pairs", "Each circle has a twin. Draw a line between the two circles that are exactly the same.", 1,
                "".join(out), leon=True)


BIRDS12 = [(.12, .62, 0), (.47, .20, 1), (.71, .70, 0), (.88, .33, 1)]   # x, y (fraction of painting), flip


def m_hidden(n=12):
    m = MAN["painting12"]
    w = PW; h = w * m["h"] / m["w"]
    if h < PH: h = PH; w = h * m["w"] / m["h"]
    x0 = (PW - w) / 2
    bg = f'<img class="a" src="{ART}/painting12.png" style="left:{x0}pt;top:0;width:{w}pt;height:{h}pt">'
    birds = []
    for (fx, fy, _) in BIRDS12:
        bw = 74; bh = bw * MAN["bird"]["h"] / MAN["bird"]["w"]
        birds.append(f'<img class="a" src="{ART}/bird.png" style="left:{fx * PW - bw / 2:.1f}pt;top:{230 + fy * 480 - bh / 2:.1f}pt;width:{bw}pt">')
    return page(n, "look", "Hidden birds", "Robert’s bird is hiding in this painting. Find all 4 birds and circle them.", 2,
                bg + "".join(birds), full_bleed=True)


def m_color(n=24):
    L, Rr = M + 8, M
    bw = PW - L - Rr
    w, h = fit("lines09", bw, 600, {"lines09": {"w": MB["lines09"][0], "h": MB["lines09"][1]}})
    body = (f'<div class="a" style="left:{L}pt;top:190pt;width:{bw}pt;height:{h + 20}pt;border-radius:14pt;background:#fff"></div>'
            f'<img class="a" src="{ARTB}/lines09.png" style="left:{L + (bw - w) / 2}pt;top:200pt;width:{w}pt">'
            f'<div class="a" style="left:{L}pt;top:{215 + h}pt;display:flex;gap:16pt;align-items:center;font:600 13pt \'Lexend\'">'
            f'<span>Use:</span>' + "".join(f'<span style="display:inline-flex;align-items:center;gap:6pt"><span style="width:22pt;height:22pt;border-radius:50%;background:{c};display:inline-block"></span>{t}</span>'
                                          for c, t in [("#D9462B", "red"), ("#2F49B5", "blue"), ("#F2C230", "yellow")]) + "</div>")
    return page(n, "shapes", "Robert’s blocks", "These shapes float in the air! Color 3 shapes red, 3 blue and 3 yellow.", 1, body)


SUMS = [(2, 1), (1, 3), (2, 2), (3, 2)]


def m_add(n=48):
    L, Rr = M, M + 8
    bw = PW - L - Rr
    bwid = 60; bh = bwid * MAN["bird"]["h"] / MAN["bird"]["w"]
    out = []
    for r, (a, b) in enumerate(SUMS):
        y = 200 + r * 128
        out.append(f'<div class="a" style="left:{L}pt;top:{y}pt;width:{bw}pt;height:108pt;border-radius:16pt;background:#F5F3EE"></div>')
        x = L + 14
        for i in range(a):
            out.append(f'<img class="a" src="{ART}/bird.png" style="left:{x}pt;top:{y + 54 - bh / 2}pt;width:{bwid}pt">'); x += bwid + 4
        out.append(f'<div class="a word" style="left:{x + 4}pt;top:{y + 30}pt;color:{ISLAND["numbers"][1]}">+</div>'); x += 34
        for i in range(b):
            out.append(f'<img class="a" src="{ART}/bird.png" style="left:{x}pt;top:{y + 54 - bh / 2}pt;width:{bwid}pt">'); x += bwid + 4
        out.append(f'<div class="a word" style="left:{PW - Rr - 130}pt;top:{y + 30}pt;color:{ISLAND["numbers"][1]}">=</div>')
        out.append(f'<div class="a" style="left:{PW - Rr - 92}pt;top:{y + 22}pt;width:76pt;height:64pt;border:2.6pt solid {INK};border-radius:12pt;background:#fff"></div>')
    return page(n, "numbers", "Adding birds", "Count the birds on each side of the +. How many birds are there together? Write the number.", 2, "".join(out))


WORDS = [("RED", "tile_red"), ("BLUE", "tile_blue"), ("GREEN", "tile_green"), ("BLACK", "tile_black")]
WORD_R = ["tile_blue", "tile_black", "tile_red", "tile_green"]


def m_words(n=57):
    L, Rr = M + 8, M
    d, top, gap = 104, 205, 22
    out = []
    for i, (w, _) in enumerate(WORDS):
        y = top + i * (d + gap)
        out.append(f'<div class="a word" style="left:{L + 10}pt;top:{y + d / 2 - 22}pt">{w}</div>')
        out.append(dot(L + 190, y + d / 2))
        out.append(dot(PW - Rr - d - 40, y + d / 2))
        out.append(lens(WORD_R[i], PW - Rr - d - 4, y, d))
    return page(n, "words", "Color words", "Read each word with a grown-up. Draw a line to the circle painted in that color.", 2,
                "".join(out), leon=True)


def m_maze(n=65):
    m = MB["net15"]
    w = PW; h = w * m[1] / m[0]
    if h < PH: h = PH; w = h * m[0] / m[1]
    bg = f'<img class="a" src="{ARTB}/net15.jpg" style="left:{(PW - w) / 2}pt;top:0;width:{w}pt;height:{h}pt">'
    bw = 96; bh = bw * MAN["bird"]["h"] / MAN["bird"]["w"]
    start = f'<img class="a" src="{ART}/bird.png" style="left:30pt;top:610pt;width:{bw}pt;filter:drop-shadow(0 2pt 4pt rgba(0,0,0,.25))">'
    goal = (f'<div class="lens" style="left:{PW - 140}pt;top:250pt;width:84pt;height:84pt"><img src="{ART}/tile_red.jpg"></div>')
    return page(n, "space", "Robert’s maze", "Robert painted a web of blue lines. Help the bird walk on the lines to the red circle.", 3,
                bg + start + goal, full_bleed=True)


def m_answers(n=77):
    L, Rr = M + 8, M
    m = MAN["painting12"]
    tw = 200; th = tw * m["h"] / m["w"]
    # birds were placed on the PAGE; map page coords -> painting thumbnail coords
    w = PW; h = w * m["h"] / m["w"]
    if h < PH: h = PH; w = h * m["w"] / m["h"]
    x0 = (PW - w) / 2
    circ = ""
    for fx, fy, _ in BIRDS12:
        px, py = fx * PW - x0, 230 + fy * 480
        cx, cy = px / w * tw, py / h * th
        circ += f'<div class="a" style="left:{cx - 13}pt;top:{cy - 11}pt;width:26pt;height:22pt;border-radius:50%;border:2.6pt solid #D9462B;box-shadow:0 0 0 1.4pt #fff"></div>'
    thumb = (f'<div style="position:relative;width:{tw}pt;height:{th}pt;border-radius:6pt;overflow:hidden">'
             f'<img src="{ART}/painting12.png" style="width:100%;height:100%;display:block">'
             + "".join(f'<img class="a" src="{ART}/bird.png" style="left:{(fx * PW - x0 - 37) / w * tw:.1f}pt;top:{(230 + fy * 480 - 18) / h * th:.1f}pt;width:{74 / w * tw:.1f}pt">' for fx, fy, _ in BIRDS12)
             + circ + "</div>")
    def row(p, t, a, extra=""):
        return (f'<div style="display:flex;gap:14pt;padding:12pt 0;border-top:1pt solid {LINE};align-items:center">'
                f'<span class="num" style="background:{ISLAND[t][1]}">{p}</span>'
                f'<div style="flex:1;font:12pt/1.35 \'Andika\'"><b style="font:700 13pt \'Baloo 2\'">{a[0]}</b><br>{a[1]}</div>{extra}</div>')
    body = (f'<div class="a" style="left:{L}pt;right:{Rr}pt;top:170pt">'
            + row(9, "look", ("Same pairs", "Blue → 2nd, red → 4th, yellow-brown → 1st, green → 3rd."))
            + row(12, "look", ("Hidden birds", "4 birds — see the red circles."), thumb)
            + row(24, "shapes", ("Robert’s blocks", "Any 3 red, 3 blue and 3 yellow shapes."))
            + row(48, "numbers", ("Adding birds", "3, 4, 4, 5."))
            + row(57, "words", ("Color words", "RED → 3rd, BLUE → 1st, GREEN → 4th, BLACK → 2nd."))
            + row(65, "space", ("Robert’s maze", "Any way that stays on the blue lines."))
            + "</div>")
    return page(n, "big", "Answers for grown-ups", "Every answer can be checked in a few seconds. Red circles show where to look.", 0, body).replace(
        "<span style=\"display:flex;gap:2pt\">", "<span style=\"display:none\">")


if __name__ == "__main__":
    os.makedirs(f"{R}/build/optionb", exist_ok=True)
    pages = [m_pairs(), m_hidden(), m_color(), m_add(), m_words(), m_maze(), m_answers()]
    open(f"{R}/build/optionb/models.html", "w").write(
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>')
    print("ok", len(pages))
