"""HTML for every page of the revised V1 EN: overlays (header/footer/boxes) for restyled original pages,
and complete new pages (front matter, island openers, new activities, answers)."""
import os, re, json, html as H, fitz
from spec import ISLANDS, ACT, OPENERS, OPENER_TITLES, ORIG_TO_NEW

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(HERE))
LANG = "EN"
SRC = f"{R}/ref/leons-thinking-book-vol2-EN-interior.pdf"


def set_lang(lang):
    global LANG, SRC
    LANG = lang
    SRC = f"{R}/ref/leons-thinking-book-vol2-{lang}-interior.pdf"
FONTS = f"file://{R}/fonts/"
ARTB, ART = f"file://{R}/art_b", f"file://{R}/art"
NAVY, GRAY, RED, GOLD, BORDER, BGC, CREAM = "#1E2A5A", "#5F6B78", "#E0533D", "#F7C93E", "#D5DAE0", "#F4F7FA", "#FFF8E1"
PW, PH = 621, 810
STAMPS = []
VOL = 2
SKIP_ANS = set()
ANS_FIRST = 92
ON_THIS = "On this mission,"          # (page, who, rect) — vector stamps applied after rendering

TTF = f"file://{R}/fonts/ttf/"
CSS = "".join(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:normal;src:url({TTF}{f}) format('truetype')}}"
              for fam, w, f in [("Andika", 400, "Andika-Regular.ttf"), ("Andika", 700, "Andika-Bold.ttf"),
                                ("Baloo 2", 600, "Baloo2-600.ttf"), ("Baloo 2", 700, "Baloo2-800.ttf"), ("Baloo 2", 800, "Baloo2-800.ttf"),
                                ("Lexend", 400, "Lexend-400.ttf"), ("Lexend", 600, "Lexend-600.ttf"), ("Lexend", 700, "Lexend-600.ttf")]) + f"""
@page {{ size: {PW}pt {PH}pt; margin: 0 }}
* {{ margin: 0; padding: 0; box-sizing: border-box }}
html, body {{ background: transparent }}
.page {{ width: {PW}pt; height: {PH}pt; position: relative; overflow: hidden; page-break-after: always; color: {NAVY}; font-family: 'Andika' }}
.a {{ position: absolute }}
.pill {{ font: 600 7.6pt 'Lexend'; letter-spacing: 1.3pt; text-transform: uppercase; padding: 4pt 9pt 3.5pt; border-radius: 20pt; display: inline-block }}
.t {{ font: 800 29pt/1.02 'Baloo 2'; letter-spacing: -.2pt }}
.ins {{ font: 400 15pt/19pt 'Andika' }}
.foot {{ font: 400 8pt 'Lexend'; color: {GRAY} }}
.num {{ font: 600 10pt 'Lexend'; width: 25pt; height: 25pt; border-radius: 50%; display: flex; align-items: center; justify-content: center }}
.box {{ background: {CREAM}; border: 1.4pt solid {GOLD}; border-radius: 10pt; padding: 7pt 11pt; font: 400 10.5pt/1.32 'Andika' }}
.box b {{ font-weight: 700 }}
.card {{ background: #fff; border: 2pt solid {BORDER}; border-radius: 14pt }}
.body {{ font: 400 13pt/1.42 'Andika' }}
.h2 {{ font: 800 21pt/1.1 'Baloo 2' }}
"""


def box_x(n):
    return (51, 578) if n % 2 == 0 else (42, 569)


def star(on, size=17):
    c = GOLD if on else "#DCDFE6"
    return (f'<svg width="{size}pt" height="{size}pt" viewBox="0 0 24 24"><path d="M12 2.4l2.8 6.2 6.8.7-5.1 4.6 1.5 6.7L12 17.2 6 20.6l1.5-6.7L2.4 9.3l6.8-.7z" '
            f'fill="{c}" stroke="{NAVY if on else c}" stroke-width="{1.2 if on else 0}" stroke-linejoin="round"/></svg>')


def stars(level, size=17):
    return "".join(star(i < level, size) for i in range(3))


def header(n, island, level, title, ins, ins_w=None, top_title=56):
    x0, x1 = box_x(n)
    name, skill, col, tc = ISLANDS[island]
    w = ins_w or (x1 - x0 - 70)
    st = f'<div class="a" style="right:{PW - x1}pt;top:38pt;display:flex;gap:2pt">{stars(level)}</div>' if level else ""
    return (f'<div class="a" style="left:{x0}pt;top:38pt"><span class="pill" style="background:{col};color:{tc}">{name}</span></div>{st}'
            f'<div class="a t" style="left:{x0}pt;top:{top_title}pt;width:{x1 - x0 - 10}pt">{H.escape(title)}</div>'
            f'<div class="a ins" style="left:{x0}pt;top:{top_title + 36}pt;width:{w}pt">{arrow(H.escape(ins)).replace('width="9pt" height="7pt"', 'width="16pt" height="11pt"')}</div>')


def footer(n, island):
    x0, x1 = box_x(n)
    name, skill, col, tc = ISLANDS[island]
    lab = f"{name} · {skill}" if name != skill else name
    num = f'<span class="num" style="background:{col};color:{tc}">{n}</span>'
    txt = f'<span class="foot">{H.escape(lab)}</span>'
    inner = (num + txt) if n % 2 == 0 else (txt + num)
    return (f'<div class="a" style="left:{x0}pt;width:{x1 - x0}pt;top:747pt;display:flex;align-items:center;'
            f'justify-content:space-between;gap:10pt">{inner}</div>')


def pbox(n, kind, text, top, x0=None, x1=None):
    a, b = box_x(n)
    x0, x1 = x0 or a, x1 or b
    return f'<div class="a box" style="left:{x0}pt;width:{x1 - x0}pt;top:{top}pt"><b>{H.escape(kind)}:</b> {arrow(H.escape(text))}</div>'


def box_height(text, width):
    chars = max(20, int(width / 5.3))
    lines = (len(text) + 16) // chars + 1
    return lines * 13.9 + 16


def section(body, bg="transparent"):
    return f'<section class="page" style="background:{bg}">{body}</section>'


def island_of(n):
    marks = [(10, "look"), (19, "remember"), (28, "shapes"), (35, "patterns"), (42, "logic"), (50, "numbers"),
             (60, "words"), (69, "space"), (76, "feelings"), (85, "big"), (90, None)]
    cur = None
    for p, isl in marks:
        if n >= p:
            cur = isl
    return cur


# ----------------------------------------------------------------------------------------------------------- front
def p_title():
    STAMPS.append((1, "leonluz", (150, 240, 470, 584)))
    return section(f"""
      <div class="a" style="left:0;right:0;top:88pt;text-align:center;font:800 44pt/1 'Baloo 2'">Leon’s Thinking Book</div>
      <div class="a" style="left:0;right:0;top:146pt;text-align:center;font:600 15pt 'Lexend';color:{RED}">Volume 1 · Ages 4–6</div>
      <div class="a" style="left:0;right:0;top:620pt;text-align:center;font:400 16pt 'Andika';color:{NAVY}">Learning to think, not just learning to answer.</div>
      <div class="a" style="left:0;right:0;top:700pt;text-align:center;font:400 12.5pt 'Andika'">Written and illustrated by <b>Robert de Farias</b></div>""", "#fff")


def p_credits():
    t = ("<b>Leon’s Thinking Book — Volume 1 (Ages 4–6)</b><br>Written and illustrated by Robert de Farias<br><br>"
         "Copyright © 2026 Robert de Farias. All rights reserved. Artwork and paintings © Robert de Farias.<br>"
         "No part of this book may be reproduced without written permission from the author, except for copying activity pages "
         "for personal or classroom use.<br><br>First edition. Independently published.<br><br>"
         "<b>Safety:</b> For children aged 4 and up. Use crayons or colored pencils. Adult supervision is recommended.<br><br>"
         "This book offers playful practice for young children. It is not a test, a diagnosis or a substitute for advice "
         "from a teacher or health professional.")
    return section(f'<div class="a" style="left:51pt;width:420pt;bottom:90pt;font:400 10pt/1.45 \'Andika\';color:{GRAY}">{t}</div>', "#fff")


HELLO1 = [
    ("p", "<i>Leon’s Thinking Book</i> is a playful activity book for children aged 4 to 6. Its idea is simple: <b>learning to think, not just learning to answer.</b>"),
    ("p", "Inside, Leon and Luz invite your child to nine islands of games. On each island, your child can practise one way of thinking:"),
    ("ul", [("Look Closely", "noticing small details."), ("Remember", "keeping pictures and words in mind."),
            ("Shapes & Colors", "naming and comparing shapes, colors and sizes."), ("Patterns", "seeing what repeats and what comes next."),
            ("Logic", "sorting, matching and explaining “why”."), ("Numbers", "counting, comparing and adding small amounts."),
            ("Words", "sounds, letters, rhymes and first words."), ("Space", "where things are and how they fit."),
            ("Feelings", "naming feelings and finding ways to calm down.")]),
    ("p", "Each island opens with a painting by the artist Robert de Farias, the author of this book. Take a moment to look at it together — there are no wrong answers when you talk about art."),
    ("h", "Before you start"),
    ("ul2", ["Keep it short: 10 to 15 minutes is plenty.", "Read the instructions aloud. Most children of this age don’t read yet.",
             "Children can answer in many ways: pointing, saying, drawing, coloring or writing. All of them count.",
             "You don’t have to go in order. It is fine to skip a page and come back later."]),
]
HELLO2 = [
    ("h", "How to help without giving the answer"),
    ("p", "<b>Ask, don’t tell.</b> Try: “What do you see?” “How did you find it?” “Is there another way?” “What would Leon do?”"),
    ("p", "<b>Give a small clue, not the answer.</b> Point to one row, or cover part of the page: “Look at the top. Is it there?”"),
    ("p", "<b>Mistakes are part of thinking.</b> Leon makes mistakes too — and then he tries again. You can say: “Interesting! Let’s check together.” or “Oops, like Leon! What could we try now?”"),
    ("p", "<b>Praise the effort.</b> Instead of “Clever!”, try: “You looked very carefully!” “You didn’t give up!” “You found a new way!”"),
    ("p", "<b>Adapt to your child.</b> Younger children can start with one-star pages, point instead of writing, or do half a page. Older children can try three-star pages and the “Try Another Way” boxes, and explain their answers."),
    ("p", "<b>Look for the little boxes:</b> <i>Parent’s Little Tip</i>, <i>Ask Leon</i>, <i>Talk About It</i> and <i>Try Another Way</i> give you short ideas for each page."),
    ("p", "The answers are at the back of the book (pages 91–95). Some pages have many good answers. Talk about them together!"),
    ("p2", "This book offers playful practice. It is not a test, a diagnosis or a substitute for advice from a teacher or health professional."),
]


def render_blocks(blocks):
    out = []
    for kind, v in blocks:
        if kind == "p":
            out.append(f'<p style="margin:0 0 9pt">{v}</p>')
        elif kind == "p2":
            out.append(f'<p style="margin:12pt 0 0;font-size:10pt;color:{GRAY}">{v}</p>')
        elif kind == "h":
            out.append(f'<div class="h2" style="margin:8pt 0 6pt">{v}</div>')
        elif kind == "ul":
            out.append('<div style="margin:2pt 0 10pt">' + "".join(
                f'<div style="display:flex;gap:8pt;margin:2.5pt 0"><span style="width:10pt;height:10pt;border-radius:50%;margin-top:4pt;flex:none;background:{ISLANDS[k][2]}"></span>'
                f'<span><b>{nm}:</b> {d}</span></div>' for (nm, d), k in zip(v, ISLANDS)) + "</div>")
        elif kind == "ul2":
            out.append('<div style="margin:0 0 6pt">' + "".join(f'<div style="margin:3pt 0">• {x}</div>' for x in v) + "</div>")
    return "".join(out)


def p_hello(n, blocks, first):
    x0, x1 = box_x(n)
    head = f'<div class="a t" style="left:{x0}pt;top:52pt">Hello, grown-ups!</div>' if first else ""
    return section(head + f'<div class="a body" style="left:{x0}pt;width:{x1 - x0}pt;top:{104 if first else 52}pt;font-size:12.6pt">{render_blocks(blocks)}</div>' + footer_plain(n), "#fff")


def footer_plain(n):
    x0, x1 = box_x(n)
    return f'<div class="a foot" style="left:{x0}pt;width:{x1 - x0}pt;top:756pt;text-align:{"left" if n % 2 == 0 else "right"}">{n}</div>'


def p_meet():
    STAMPS.append((6, "leon", (60, 170, 300, 427)))
    STAMPS.append((6, "luz", (395, 190, 535, 330)))
    bub = lambda x, y, w, t: (f'<div class="a" style="left:{x}pt;top:{y}pt;width:{w}pt;background:#fff;border:2pt solid {NAVY};border-radius:16pt;'
                             f'padding:10pt 13pt;font:400 14pt/1.3 \'Andika\'">{t}</div>')
    steps = "".join(f'<div style="flex:1;text-align:center"><div style="font:800 22pt \'Baloo 2\';color:{c}">{t}</div>'
                    f'<div style="font:400 11pt \'Andika\';color:{GRAY}">{d}</div></div>'
                    for t, c, d in [("Try", "#2E9EA0", "Leon has a go."), ("Oops!", RED, "It doesn’t work… yet."), ("Try again!", "#9ACB45", "Leon finds another way.")])
    return section(f"""
      <div class="a t" style="left:51pt;top:52pt">Meet Leon &amp; Luz!</div>
      {bub(60, 450, 250, "“Hi, I’m <b>Leon</b>! I love to explore. Sometimes I make mistakes — then I try again!”")}
      {bub(330, 350, 240, "“Hi, I’m <b>Luz</b>! I light up when someone has an idea. What will <i>your</i> idea be?”")}
      <div class="a card" style="left:51pt;width:527pt;top:600pt;padding:14pt;display:flex;align-items:center">
        {steps.replace('</div></div><div', '</div></div>' + ARROW.replace('width="9pt" height="7pt"', 'width="22pt" height="15pt"') + '<div')}</div>
      <div class="a box" style="left:51pt;width:527pt;top:700pt"><b>Parent’s Little Tip:</b> When your child gets stuck, ask: “What would Leon do?” Leon never gives up — he just tries another way.</div>
      {footer_plain(6)}""", "#fff")


def p_howto():
    lv = [(1, "I Can Do It!", "An easy start."), (2, "Let Me Think!", "Time to think a little more."), (3, "Big Challenge!", "For brave thinkers. Help is welcome!")]
    rows = "".join(f'<div style="display:flex;align-items:center;gap:14pt;margin:7pt 0"><span style="display:flex;gap:2pt;width:64pt">{stars(l, 19)}</span>'
                   f'<span><b style="font:800 15pt \'Baloo 2\'">{t}</b> &nbsp;{d}</span></div>' for l, t, d in lv)
    ic = lambda svg, t: f'<div style="display:flex;align-items:center;gap:14pt;margin:9pt 0"><span style="width:64pt;display:flex;justify-content:center">{svg}</span><span>{t}</span></div>'
    ear = f'<svg width="26pt" height="26pt" viewBox="0 0 24 24"><path d="M7 9a5 5 0 0 1 10 0c0 3-3 4-3 7a3 3 0 0 1-6 0" fill="none" stroke="{NAVY}" stroke-width="2.2" stroke-linecap="round"/><path d="M10 9a2 2 0 0 1 4 0" fill="none" stroke="{NAVY}" stroke-width="2"/></svg>'
    eye = f'<svg width="34pt" height="22pt" viewBox="0 0 34 22"><path d="M2 11C8 2 26 2 32 11C26 20 8 20 2 11Z" fill="#fff" stroke="{NAVY}" stroke-width="2.4"/><circle cx="17" cy="11" r="5" fill="#2E9EA0"/><circle cx="17" cy="11" r="2.2" fill="{NAVY}"/></svg>'
    boxes = "".join(f'<div class="box" style="margin:6pt 0"><b>{k}:</b> {d}</div>' for k, d in [
        ("Parent’s Little Tip", "a short idea for the grown-up."), ("Ask Leon", "one more question to think about."),
        ("Talk About It", "a question to talk about together."), ("Try Another Way", "an extra challenge for children who want more.")])
    return section(f"""
      <div class="a t" style="left:42pt;top:52pt">How to use this book</div>
      <div class="a body" style="left:42pt;width:527pt;top:104pt">
        <div class="h2" style="font-size:17pt;margin-bottom:4pt">Stars show how hard a page is</div>{rows}
        <div class="h2" style="font-size:17pt;margin:14pt 0 2pt">Little signs</div>
        {ic(ear, "<b>Listen:</b> a grown-up reads something aloud.")}
        {ic(eye, "<b>Look and remember:</b> look carefully, then turn the page.")}
        <div class="h2" style="font-size:17pt;margin:14pt 0 2pt">Little boxes for grown-ups</div>{boxes}
        <div style="margin-top:12pt"><b>Leon</b> is your thinking friend. He tries, makes mistakes and tries again! <b>Luz</b> lights up when you have an idea.</div>
      </div>{footer_plain(7)}""", "#fff")


def p_starchart():
    rows = []
    for isl in ["look", "remember", "shapes", "patterns", "logic", "numbers", "words", "space", "feelings", "big"]:
        name, _, col, tc = ISLANDS[isl]
        pages = [a[0] for a in ACT if a[2] == isl]
        extra = {"remember": [27], "logic": [45], "feelings": [79, 80], "big": [87]}.get(isl, [])
        pages = sorted(set(pages + extra) - {45} | ({45} if isl == "logic" else set()))
        cells = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;width:30pt">{star(False, 22).replace("#DCDFE6", "#fff").replace("stroke-width=\"0\"", f"stroke-width=\"1.4\" stroke=\"{NAVY}\"")}'
                        f'<span style="font:600 7.5pt \'Lexend\';color:{GRAY}">{p}</span></div>' for p in pages)
        rows.append(f'<div style="display:flex;align-items:center;gap:8pt;margin:5pt 0"><span class="pill" style="background:{col};color:{tc};width:104pt;text-align:center">{name}</span>'
                    f'<div style="display:flex;gap:2pt;flex-wrap:wrap">{cells}</div></div>')
    return section(f"""
      <div class="a t" style="left:51pt;top:52pt">My star chart</div>
      <div class="a ins" style="left:51pt;top:90pt;width:500pt">Color a star for every page you try — trying is what counts!</div>
      <div class="a" style="left:51pt;width:527pt;top:132pt">{''.join(rows)}</div>
      <div class="a box" style="left:51pt;width:527pt;top:700pt"><b>Island explored!</b> When you finish an island, draw a big star next to its name.</div>
      {footer_plain(8)}""", "#fff")


# ----------------------------------------------------------------------------------------------------------- openers
def p_opener(n, isl, paint, who, bubble, detective, adult):
    name, skill, col, tc = ISLANDS[isl]
    x0, x1 = box_x(n)
    if paint == "13":
        img = f'<img class="a" src="{ART}/bird.png" style="left:{x0 + 10}pt;top:230pt;width:{x1 - x0 - 20}pt">'
    else:
        img = f'<img class="a" src="{ARTB}/open_{paint}.jpg" style="left:{x0}pt;top:178pt;width:{x1 - x0}pt;height:380pt;object-fit:cover;border-radius:4pt">'
    cw = 120 if who != "both" else 150
    if who == "leon":
        STAMPS.append((n, "leon", (x0, 556, x0 + 112, 676)))
    elif who == "luz":
        STAMPS.append((n, "luz", (x0 + 6, 566, x0 + 106, 666)))
    else:
        STAMPS.append((n, "leonluz", (x0, 552, x0 + 118, 679)))
    return section(f"""
      <div class="a" style="left:0;right:0;top:0;height:150pt;background:{col}"></div>
      <div class="a" style="left:{x0}pt;top:50pt;font:600 9pt 'Lexend';letter-spacing:1.6pt;text-transform:uppercase;color:{tc};opacity:.85">{H.escape(skill)}</div>
      <div class="a" style="left:{x0}pt;top:68pt;width:{x1 - x0}pt;white-space:nowrap;font:800 40pt/1 'Baloo 2';color:{tc}" class="fitop">{H.escape(OPENER_TITLES[isl])}</div>
      {img}
      <div class="a" style="left:{x0 + 130}pt;top:572pt;width:{x1 - x0 - 130}pt;background:#fff;border:2pt solid {NAVY};border-radius:16pt;padding:9pt 13pt;font:400 15pt/1.3 'Andika'">“{H.escape(bubble)}”</div>
      <div class="a card" style="left:{x0}pt;width:{x1 - x0}pt;top:680pt;padding:9pt 13pt;font:400 12.5pt/1.3 'Andika';border-color:{col}">
        <b style="font:800 13pt 'Baloo 2';color:{NAVY}">Art Detective:</b> {H.escape(detective)}</div>
      <div class="a foot" style="left:{x0}pt;width:{x1 - x0}pt;top:734pt">{ON_THIS} {H.escape(adult)} &nbsp;·&nbsp; Painting: Robert de Farias</div>
      {footer(n, isl)}""", "#fff")


# ----------------------------------------------------------------------------------------------------------- new / rebuilt activities
def p27():
    n, isl = 27, "remember"
    x0, x1 = box_x(n)
    sv = lambda inner: f'<svg width="110pt" height="90pt" viewBox="0 0 110 90">{inner}</svg>'
    s = f'stroke="{NAVY}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    models = [(1, sv(f'<circle cx="55" cy="45" r="28" {s}/><circle cx="55" cy="45" r="4" fill="{NAVY}"/>')),
              (2, sv(f'<path d="M30 45 L55 22 L80 45 V75 H30 Z" {s}/><rect x="49" y="55" width="12" height="20" {s}/>')),
              (3, sv(f'<circle cx="55" cy="34" r="13" {s}/><path d="M55 12v-6M55 62v-6M33 34h-6M83 34h-6" {s}/><path d="M12 78 q12-10 24 0 t24 0 t24 0 t24 0" {s}/>'))]
    rows = []
    for i, (lv, svg) in enumerate(models):
        y = 160 + i * 182
        rows.append(f'<div class="a card" style="left:{x0}pt;top:{y}pt;width:170pt;height:160pt;display:flex;flex-direction:column;align-items:center;justify-content:center">'
                    f'<div style="display:flex;gap:1pt;margin-bottom:6pt">{stars(lv, 13)}</div>{svg}</div>'
                    f'<div class="a" style="left:{x0 + 190}pt;top:{y}pt;width:{x1 - x0 - 190}pt;height:160pt;border:2pt dashed #B8C0CC;border-radius:14pt;background:#fff"></div>')
    return section(header(n, isl, 2, "Look, cover, draw", "Look at one picture. Cover it with your hand. Draw it from memory. Start with number 1!")
                   + "".join(rows) + pbox(n, "Parent's Little Tip", "It doesn’t need to be perfect. Ask: “What did you remember first?”", 700) + footer(n, isl), BGC)


def p45():
    n, isl = 45, "logic"
    x0, x1 = box_x(n)
    rows = [(51, 185, 579, 313), (51, 335, 579, 463), (51, 485, 579, 613)]
    sc = 0.78
    w, h = 528 * sc, 128 * sc
    left = x0 + (x1 - x0 - w) / 2
    for i, r in enumerate(rows):
        y = 158 + i * (h + 8)
        STAMPS.append((n, f"orig:38:{','.join(map(str, r))}", (left, y, left + w, y + h)))
    y4 = 158 + 3 * (h + 8)
    card4 = (f'<div class="a card" style="left:{left}pt;top:{y4}pt;width:{w}pt;height:{h}pt"></div>'
             f'<div class="a" style="left:{left + 14}pt;top:{y4 + h / 2 - 12}pt;font:700 15pt \'Andika\'">4</div>')
    icons = [((52, 405, 132, 445), 0), ((346, 226, 410, 280), 1), ((56, 226, 116, 272), 2)]   # snail, bird, fish (from p.37)
    for (clip, k) in icons:
        cx = left + w * (0.36 + 0.24 * k)
        ww, hh = (clip[2] - clip[0]) * .78, (clip[3] - clip[1]) * .78
        STAMPS.append((n, f"orig:37:{','.join(map(str, clip))}", (cx - ww / 2, y4 + h / 2 - hh / 2, cx + ww / 2, y4 + h / 2 + hh / 2)))
    riddles = ("Read one at a time: 1. “I live in the water and I can swim.” 2. “I am hot and yellow. I shine in the sky.” "
               "3. “You can drink from me.” 4. “I am slow. I carry my house on my back.”")
    return section(header(n, isl, 2, "Who am I?", "Listen to each riddle. Circle the answer.") + card4
                   + pbox(n, "For grown-ups", riddles, y4 + h + 14) + footer(n, isl), "transparent_bg")


def feelings_faces(y, x, size=30):
    faces = [("happy", "M8 14 q4 4 8 0"), ("sad", "M8 16 q4 -4 8 0"), ("angry", "M8 16 h8"), ("worried", "M9 16 q3 -2 6 0")]
    out = []
    for i, (lab, mouth) in enumerate(faces):
        brows = '<path d="M7 8 l3 1.5 M17 8 l-3 1.5" stroke="#1E2A5A" stroke-width="1.4"/>' if lab == "angry" else (
            '<path d="M7 9 l3 -1.5 M17 9 l-3 -1.5" stroke="#1E2A5A" stroke-width="1.4"/>' if lab == "worried" else "")
        out.append(f'<div class="a" style="left:{x + i * (size + 22)}pt;top:{y}pt;text-align:center;width:{size + 12}pt">'
                   f'<svg width="{size}pt" height="{size}pt" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10.5" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.6"/>'
                   f'<circle cx="9" cy="10.5" r="1.3" fill="{NAVY}"/><circle cx="15" cy="10.5" r="1.3" fill="{NAVY}"/>{brows}'
                   f'<path d="{mouth}" stroke="{NAVY}" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>'
                   f'<div style="font:400 8.5pt \'Andika\';color:{GRAY}">{lab}</div></div>')
    return "".join(out)


def scene_svg(kind):
    s = f'stroke="{NAVY}" stroke-width="2.2" stroke-linejoin="round"'
    if kind == "blocks":
        return (f'<svg width="150pt" height="110pt" viewBox="0 0 150 110"><rect x="20" y="80" width="26" height="26" fill="{RED}" {s}/>'
                f'<rect x="58" y="70" width="26" height="26" fill="#2E9EA0" {s} transform="rotate(18 71 83)"/><rect x="96" y="78" width="26" height="26" fill="{GOLD}" {s} transform="rotate(-25 109 91)"/>'
                f'<rect x="64" y="30" width="26" height="26" fill="#9ACB45" {s} transform="rotate(35 77 43)"/><path d="M40 30 l-8 -8 M110 40 l8 -8 M30 55 l-10 0" stroke="{GRAY}" stroke-width="2"/></svg>')
    if kind == "crayons":
        cs = [RED, "#2E9EA0", GOLD, "#9ACB45", "#ED8A33"]
        return (f'<svg width="150pt" height="110pt" viewBox="0 0 150 110"><rect x="20" y="40" width="110" height="62" rx="6" fill="#fff" {s}/>'
                + "".join(f'<path d="M{32 + i * 20} 44 v-22 l7 -10 l7 10 v22 Z" fill="{c}" {s}/>' for i, c in enumerate(cs)) + "</svg>")
    if kind == "line":
        return (f'<svg width="150pt" height="110pt" viewBox="0 0 150 110">' + "".join(
            f'<circle cx="{25 + i * 30}" cy="40" r="11" fill="{c}" {s}/><rect x="{16 + i * 30}" y="52" width="18" height="40" rx="6" fill="{c}" {s}/>'
            for i, c in enumerate(["#C8B8F0", "#9CC4F0", "#F6C6D0", "#9ACB45", "#F9DD83"])) + f'<path d="M5 96 h140" {s}/></svg>')
    if kind == "night":
        return (f'<svg width="150pt" height="110pt" viewBox="0 0 150 110"><rect x="5" y="5" width="140" height="100" rx="10" fill="{NAVY}"/>'
                f'<path d="M110 22 a14 14 0 1 0 10 24 a11 11 0 1 1 -10 -24Z" fill="{GOLD}"/><text x="30" y="70" font-family="Baloo 2" font-weight="800" font-size="30" fill="#fff">BANG!</text></svg>')
    return ""


def p79():
    n, isl = 79, "feelings"
    x0, x1 = box_x(n)
    cards = [("blocks", "Leon’s tower of blocks falls down."), ("crayons", "Luz gets a new box of crayons."),
             ("line", "Leon has to wait a long time in a line."), ("night", "Luz hears a loud noise at night.")]
    out = []
    cw = (x1 - x0 - 14) / 2
    for i, (k, t) in enumerate(cards):
        cx, cy = x0 + (i % 2) * (cw + 14), 168 + (i // 2) * 262
        out.append(f'<div class="a card" style="left:{cx}pt;top:{cy}pt;width:{cw}pt;height:246pt"></div>'
                   f'<div class="a" style="left:{cx}pt;width:{cw}pt;top:{cy + 12}pt;text-align:center">{scene_svg(k)}</div>'
                   f'<div class="a" style="left:{cx + 12}pt;width:{cw - 24}pt;top:{cy + 132}pt;text-align:center;font:700 12.5pt/1.25 \'Andika\'">{t}</div>'
                   + feelings_faces(cy + 176, cx + 14, 30))
    return section(header(n, isl, 2, "Everyday feelings", "How might Leon and Luz feel? Circle a face. You can circle more than one!")
                   + "".join(out) + pbox(n, "Talk About It", "Have you ever felt like this? What helped you?", 694) + footer(n, isl), BGC)


def p80():
    n, isl = 80, "feelings"
    x0, x1 = box_x(n)
    s = f'stroke="{NAVY}" stroke-width="2.2"'
    rain = "".join(f'<path d="M{30 + (i * 37) % 480} {20 + (i * 53) % 120} l-6 14" stroke="#3B82C4" stroke-width="2.4" stroke-linecap="round"/>' for i in range(26))
    scene = (f'<svg width="{x1 - x0}pt" height="250pt" viewBox="0 0 {x1 - x0} 250"><rect x="0" y="0" width="{x1 - x0}" height="250" rx="14" fill="#E3F0FB" {s}/>'
             f'<rect x="0" y="185" width="{x1 - x0}" height="65" rx="0" fill="#CFE8B4"/><path d="M60 40 q20 -30 50 -8 q30 -20 45 10 q25 0 20 22 h-120 q-15 -20 5 -24Z" fill="#fff" {s}/>'
             f'<path d="M330 30 q20 -30 50 -8 q30 -20 45 10 q25 0 20 22 h-120 q-15 -20 5 -24Z" fill="#fff" {s}/>{rain}</svg>')
    leon_svg = f'<div class="a" style="left:{x0 + 50}pt;top:262pt;width:150pt;height:155pt;overflow:hidden"><img src="{ARTB}/leon.svg" style="width:150pt;height:160pt;clip-path:inset(18% 0 0 0)"></div>'
    luz_svg = f'<img class="a" src="{ARTB}/luz.svg" style="left:{x1 - 190}pt;top:290pt;width:96pt;height:96pt">'

    face = lambda x: f'<div class="a" style="left:{x}pt;top:186pt;width:56pt;height:56pt;border-radius:50%;border:2.4pt dashed {NAVY};background:#fff"></div>'
    lines = lambda y, t: (f'<div class="a" style="left:{x0}pt;top:{y}pt;font:700 14pt \'Andika\'">{t}</div>'
                          f'<div class="a" style="left:{x0}pt;width:{x1 - x0}pt;top:{y + 28}pt;height:62pt;border:2pt dashed #B8C0CC;border-radius:12pt;background:#fff"></div>')
    return section(header(n, isl, 2, "Same day, different feelings",
                          "It starts to rain! Leon loves rain. Luz wanted to play outside. Draw how they feel in the circles. What could they do?")
                   + f'<div class="a" style="left:{x0}pt;top:170pt">{scene}</div>' + leon_svg + luz_svg + face(x0 + 102) + face(x1 - 168)
                   + lines(440, "What could Leon do?") + lines(560, "What could Luz do?")
                   + pbox(n, "Ask Leon", "Can two friends feel different things about the same rain?", 694) + footer(n, isl), BGC)


def p87():
    n, isl = 87, "big"
    x0, x1 = box_x(n)
    STAMPS.append((n, "orig:73:42,185,580,530", (x0, 170, x1, 170 + (x1 - x0) * 345 / 538)))
    eye = f'<svg width="40pt" height="26pt" viewBox="0 0 34 22"><path d="M2 11C8 2 26 2 32 11C26 20 8 20 2 11Z" fill="#fff" stroke="{NAVY}" stroke-width="2.4"/><circle cx="17" cy="11" r="5" fill="#2E9EA0"/><circle cx="17" cy="11" r="2.2" fill="{NAVY}"/></svg>'
    return section(header(n, isl, 3, "Picnic Mission", "Mission time! Leon and Luz are having a picnic. Look for 20 seconds. Remember everything you can. Then turn the page!")
                   + f'<div class="a" style="left:{x0}pt;width:{x1 - x0}pt;top:560pt;text-align:center">{eye}<div style="font:700 16pt \'Andika\'">Now turn the page!</div></div>'
                   + pbox(n, "Parent's Little Tip", "Count 20 seconds together. On the next page, hide this picture completely.", 676) + footer(n, isl), BGC)


def p88():
    n, isl = 88, "big"
    x0, x1 = box_x(n)
    q = [("How many sandwiches?", ["2", "3", "4"]), ("What color is the basket?", ["red", "blue", "yellow"]),
         ("How many ants?", ["1", "2", "3"]), ("How many apples?", ["1", "2", "3"])]
    colmap = {"red": RED, "blue": "#3B82C4", "yellow": GOLD}
    out = []
    for i, (t, opts) in enumerate(q):
        y = 160 + i * 112
        out.append(f'<div class="a card" style="left:{x0}pt;top:{y}pt;width:{x1 - x0}pt;height:98pt"></div>'
                   f'<div class="a" style="left:{x0 + 16}pt;top:{y + 12}pt;font:700 15pt \'Andika\'">{i + 1}. {t}</div>')
        for j, o in enumerate(opts):
            cx = x0 + 60 + j * 150
            inner = (f'<span style="width:30pt;height:30pt;border-radius:50%;background:{colmap[o]};border:2pt solid {NAVY};display:inline-block"></span>'
                     if o in colmap else f'<span style="font:800 24pt \'Baloo 2\'">{o}</span>')
            out.append(f'<div class="a" style="left:{cx}pt;top:{y + 44}pt;width:90pt;height:44pt;border:2pt solid {BORDER};border-radius:22pt;background:#fff;'
                       f'display:flex;align-items:center;justify-content:center;gap:6pt">{inner}</div>')
    out.append(f'<div class="a" style="left:{x0}pt;top:612pt;font:700 15pt \'Andika\'">Bonus: apples + sandwiches =</div>'
               f'<div class="a" style="left:{x0 + 250}pt;top:604pt;width:70pt;height:42pt;border:2.4pt solid {NAVY};border-radius:10pt;background:#fff"></div>')
    return section(header(n, isl, 3, "Picnic Mission: questions", "Don’t look back! Circle the right answer.")
                   + "".join(out) + pbox(n, "Ask Leon", "Tell a little story about the picnic!", 676) + footer(n, isl), BGC)


# ----------------------------------------------------------------------------------------------------------- overlays for restyled original pages
def overlay(n, a, bottoms):
    new, orig, isl, level, title, ins, box = a
    x0, x1 = box_x(n)
    body = header(n, isl, level, title, ins)
    extra = ""
    if VOL == 1 and n == 16:   # balloon strings: names under the characters
        for x, t in [(152, "Leon"), (306, "Luz"), (462, "bird")]:
            extra += f'<div class="a" style="left:{x - 40}pt;width:80pt;top:679pt;text-align:center;font:700 11pt \'Andika\'">{t}</div>'
    if VOL == 1 and n == 64 and LANG == "EN":   # rhyme time: name the dish
        extra += f'<div class="a" style="left:430pt;width:84pt;top:522pt;text-align:center;font:700 11pt \'Andika\';color:{GRAY}">dish</div>'
    if VOL == 1 and n == 40:   # my own pattern: two examples first
        ex = lambda cols, who: ('<div style="display:flex;align-items:center;gap:6pt;margin:4pt 0"><span style="font:700 11pt Andika;width:120pt;white-space:nowrap">' + who + "</span>"
                                + "".join(f'<span style="width:22pt;height:22pt;border-radius:50%;background:{c};border:1.8pt solid {NAVY};display:inline-block"></span>' for c in cols) + "</div>")
        extra += (f'<div class="a" style="left:{x0 + 60}pt;top:178pt">' + ex([RED, "#3B82C4"] * 3, "Leon’s pattern:")
                  + ex([GOLD, GOLD, "#9ACB45"] * 2, "Luz’s pattern:") + "</div>")
    if VOL == 1 and n == 54:   # number path: super path to 15
        g = [[10, 11, 18, 14], [16, 12, 13, 17], [19, 20, 14, 15], [11, 16, 18, 13]]
        cells = "".join(f'<div style="width:26pt;height:22pt;border:1.4pt solid {NAVY};display:flex;align-items:center;justify-content:center;font:700 11pt Andika;background:#fff">{v}</div>'
                        for row in g for v in row)
        extra += (f'<div class="a" style="left:{x0 + 20}pt;top:640pt;font:700 12pt \'Andika\';width:300pt">Try Another Way — Super path!<br>'
                  f'<span style="font-weight:400;font-size:11pt">Start at 10. Follow 11, 12 … 15. Move up, down, left or right.</span></div>'
                  f'<div class="a" style="left:{x1 - 130}pt;top:636pt;display:grid;grid-template-columns:repeat(4,26pt)">{cells}</div>')
    if box and not (VOL == 1 and n == 54):
        bw = x1 - x0
        top = bottoms.get(n, 600) + 16 + (30 if VOL == 1 and n == 16 else 0)
        h = box_height(box[1], bw)
        if top + h <= 740:
            body += pbox(n, box[0], box[1], top)
        else:
            print(f"  [box skipped p.{n}: no room — {box[0]}]")
    return section(body + extra + footer(n, isl))


# ----------------------------------------------------------------------------------------------------------- answers
def parse_original_answers():
    d = fitz.open(SRC)
    rows = []
    for pn in range(76, 79):
        spans = sorted([s for b in d[pn].get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if 84 < s["bbox"][1] < 750],
                       key=lambda s: (round(s["bbox"][1]), s["bbox"][0]))
        cur = None
        for s in spans:
            x, t = s["bbox"][0], s["text"]
            if x < 90 and re.match(r"(p\.|blz\.)\s*\d+", t.strip()):
                cur = {"p": int(re.findall(r"\d+", t)[0]), "title": "", "ans": ""}; rows.append(cur)
            elif cur and 90 <= x < 240:
                cur["title"] += (" " if cur["title"] else "") + t.strip()
            elif cur and x >= 240:
                cur["ans"] += (" " if cur["ans"] else "") + t.strip()
    return rows


OVERRIDE = {
    13: "Row 1: 3rd fish (faces the other way). Row 2: 4th (a pear). Row 3: 2nd boat (no sails). Row 4: 1st cup (no handle, no steam).",
    14: "Bottom picture: the sun is missing, the tree is missing, the balloon is a different color.",
    20: "Apple, cup, star (in this order).",
    27: "Drawings that look like the models: a circle with a dot, a house, a sun over a wavy line. They don’t need to be perfect.",
    29: "5 circles red (2 eyes, 2 buttons, the ball on the antenna). 3 squares blue (head and 2 hands). The body is a rectangle.",
    40: "Any pattern that repeats a rule. Ask your child to say the rule.",
    45: "1: fish. 2: sun. 3: cup. 4: snail.",
    54: "1 → 2 (right) → 3 (down) → 4 (right) → 5 (down) → 6 (right) → 7 (down) → 8 (down) → 9 (right). Super path: 10 → 11 (right) → 12 (down) → 13 (right) → 14 (down) → 15 (right).",
    67: "1: a blue hat. 2: a sun in the sky and a green tree. 3: an X on the fish, a cloud, and a circle around the hat.",
    77: "Leon 1 (happy) → 3rd face. Leon 2 (sad) → 4th face. Leon 3 (angry) → 1st face. Leon 4 (scared) → 2nd face.",
    78: "Many answers are OK. For example: dropped ice cream → sad or angry; birthday cake → happy or excited; thunder → scared or surprised.",
    83: "Helps pick them up. Shares it with Luz. Gives her a hug.",
}
NEW_ROWS = [
    (10, "Art Detective", "There are several spirals in the painting. Any one is right."),
    (19, "Art Detective", "Any color your child remembers."),
    (28, "Art Detective", "Any shape with 3 corners."),
    (35, "Art Detective", "Any group of lines that go the same way."),
    (42, "Art Detective", "Any answer with a reason. (It is Robert’s bird.)"),
    (50, "Art Detective", "2 round circles."),
    (60, "Art Detective", "Any invented word is great."),
    (69, "Art Detective", "Any way down the blue lines."),
    (76, "Art Detective", "There is no wrong answer."),
    (79, "Everyday feelings", "Many answers are OK. For example: 1 sad or angry; 2 happy or excited; 3 bored or impatient; 4 scared or surprised."),
    (80, "Same day, different feelings", "Leon: happy. Luz: sad or disappointed. Any helpful idea is a good answer (an umbrella, play inside, jump in puddles together)."),
    (85, "Art Detective", "Any stripe followed from one side to the other."),
    (88, "Picnic Mission", "3 sandwiches, a red basket, 1 ant, 2 apples. Bonus: 2 + 3 = 5."),
]


def answer_rows():
    if LANG != "EN":
        return answer_rows_loc()
    rows = []
    for r in parse_original_answers():
        if r["p"] in SKIP_ANS:
            continue
        n = ORIG_TO_NEW.get(r["p"])
        if n is None:
            continue
        title = next((a[4] for a in ACT if a[0] == n), r["title"])
        rows.append({"p": n, "title": title, "ans": OVERRIDE.get(n, r["ans"])})
    have = {r["p"] for r in rows}
    for n, ans in OVERRIDE.items():
        if n not in have:
            title = next((a[4] for a in ACT if a[0] == n), {27: "Look, cover, draw", 45: "Who am I?"}.get(n, ""))
            rows.append({"p": n, "title": title, "ans": ans})
    for n, t, a in NEW_ROWS:
        rows.append({"p": n, "title": t, "ans": a})
    rows.sort(key=lambda r: r["p"])
    return rows


def answer_rows_loc():
    import i18n, json
    ov, new_rows = i18n.OVERRIDE[LANG], i18n.NEW_ROWS[LANG]
    orig = json.load(open(f"{R}/build/v2_orig_strings.json"))
    new_to_orig = {v: k for k, v in ORIG_TO_NEW.items()}
    def title_of(n):
        if n in i18n.NEW_TITLES[LANG]:
            return i18n.NEW_TITLES[LANG][n]
        return orig[str(new_to_orig[n])][LANG]["title"]
    rows = []
    for r in parse_original_answers():
        if r["p"] in SKIP_ANS:
            continue
        n = ORIG_TO_NEW.get(r["p"])
        if n is None:
            continue
        rows.append({"p": n, "title": title_of(n), "ans": ov.get(n, r["ans"])})
    have = {r["p"] for r in rows}
    for n, ans in ov.items():
        if n not in have:
            rows.append({"p": n, "title": title_of(n), "ans": ans})
    for n, t, a in new_rows:
        rows.append({"p": n, "title": t, "ans": a})
    rows.sort(key=lambda r: r["p"])
    return rows


def translate_html(doc):
    """Replace every English text node by its FR/NL version (new strings from i18n, unchanged activity text from the originals)."""
    import i18n, json, html as HH
    col = 1 if LANG == "FR" else 2
    tr = {e: row[col] for row in i18n.T for e in [row[0]]}
    orig = json.load(open(f"{R}/build/v2_orig_strings.json"))
    for p, v in orig.items():
        for k in ("title", "ins"):
            e, l = v["EN"][k], v[LANG][k]
            if e and l:
                tr.setdefault(e, l)
                tr.setdefault(e.rstrip(" →").strip(), l.replace("\u202f", " ").rstrip(" →").strip())
    missing = set()
    head, body = doc.split("<body>", 1)
    def sub(m):
        raw = m.group(1)
        u = HH.unescape(raw)
        key = u.strip()
        if not key or re.fullmatch(r"[\d\s.,:→+=–\-·?]+", key) or key in ("Leon", "Luz", "Robert de Farias", "Leon’s Thinking Book", "BANG!"):
            return m.group(0)
        if key not in tr:
            missing.add(key)
            return m.group(0)
        lead = u[: len(u) - len(u.lstrip())]
        trail = u[len(u.rstrip()):]
        return ">" + HH.escape(lead + tr[key] + trail, quote=False) + "<"
    body = re.sub(r">([^<>]+)<", sub, body)
    if missing:
        open(f"{R}/build/v2r/missing_{LANG}.txt", "w").write("\n".join(sorted(missing)))
    body = body.replace("\u202f", "\u00a0")
    if LANG == "FR":   # French typography: non-breaking space before ? ! : ; and inside « »
        body = re.sub(r" ([?!:;»])", "\u00a0\\1", body)
        body = body.replace("« ", "«\u00a0")
    return head.replace('lang="en"', f'lang="{LANG.lower()}"') + "<body>" + body


ARROW = '<svg width="9pt" height="7pt" viewBox="0 0 12 8" style="vertical-align:0"><path d="M0 4h10M7 1l3 3-3 3" stroke="#1E2A5A" stroke-width="1.4" fill="none"/></svg>'


TICK = '<svg width="9pt" height="9pt" viewBox="0 0 12 12" style="vertical-align:-1pt"><path d="M2 6.5l3 3 5-7" stroke="#1E2A5A" stroke-width="1.8" fill="none" stroke-linecap="round"/></svg>'
CROSS = '<svg width="9pt" height="9pt" viewBox="0 0 12 12" style="vertical-align:-1pt"><path d="M2.5 2.5l7 7M9.5 2.5l-7 7" stroke="#1E2A5A" stroke-width="1.8" stroke-linecap="round"/></svg>'


def arrow(t):
    return t.replace("→", ARROW).replace("✓", TICK).replace("✗", CROSS)


def answers_pages():
    rows = answer_rows()
    pages, cur, h = [], [], 0
    first_top, top, limit = 126, 64, 738
    for r in rows:
        lines = max(1, (len(r["ans"]) + 10) // 66 + 1, (len(r["title"]) + 2) // 26 + 1)
        rh = lines * 13.0 + 10
        start = first_top if not pages else top
        if start + h + rh > limit:
            pages.append(cur); cur, h = [], 0
        cur.append((r, rh)); h += rh
    pages.append(cur)
    out = []
    for i, items in enumerate(pages):
        n = ANS_FIRST + i
        x0, x1 = box_x(n)
        y = first_top if i == 0 else top
        body = ""
        if i == 0:
            body += (f'<div class="a t" style="left:{x0}pt;top:52pt">Answers for grown-ups</div>'
                     f'<div class="a ins" style="left:{x0}pt;top:92pt;font-size:12.5pt;color:{GRAY}">Some pages have many good answers. Talk about them together!</div>')
        for r, rh in items:
            isl = island_of(r["p"]) or "m12"
            col, tc = ISLANDS[isl][2], ISLANDS[isl][3]
            body += (f'<div class="a" style="left:{x0}pt;width:{x1 - x0}pt;top:{y}pt;height:{rh}pt;border-top:.8pt solid #E3E7EC;padding-top:5pt;display:flex;gap:10pt;font:400 9.8pt/13pt \'Andika\'">'
                     f'<span class="num" style="background:{col};color:{tc};width:22pt;height:22pt;font-size:8.5pt;flex:none">{r["p"]}</span>'
                     f'<b style="width:150pt;flex:none">{H.escape(r["title"])}</b><span>{arrow(H.escape(r["ans"]))}</span></div>')
            y += rh
        out.append(section(body + footer_plain(n), "#fff"))
    return out


# ----------------------------------------------------------------------------------------------------------- assemble
def html_pages(bottoms):
    STAMPS.clear()
    act = {a[0]: a for a in ACT}
    op = {o[0]: o for o in OPENERS}
    secs = {}
    secs[1] = p_title(); secs[2] = p_credits()
    secs[3] = section("")
    secs[4] = p_hello(4, HELLO1, True); secs[5] = p_hello(5, HELLO2, False)
    secs[6] = p_meet(); secs[7] = p_howto(); secs[8] = p_starchart()
    secs[9] = section(footer_plain(9))
    for n, o in op.items():
        secs[n] = p_opener(*o)
    secs[27] = p27(); secs[45] = p45().replace("transparent_bg", BGC)
    secs[79] = p79(); secs[80] = p80(); secs[87] = p87(); secs[88] = p88()
    for n, a in act.items():
        if n not in secs:
            secs[n] = overlay(n, a, bottoms)
    secs[90] = section("")
    ans = answers_pages()
    assert len(ans) <= 5, f"answers need {len(ans)} pages"
    while len(ans) < 5:
        ans.append(section(footer_plain(91 + len(ans)), "#fff"))
    for i, s in enumerate(ans):
        secs[91 + i] = s
    secs[96] = section("")
    missing = [n for n in range(1, 97) if n not in secs]
    assert not missing, missing
    body = "".join(secs[n] for n in range(1, 97))
    js = "<script>document.fonts.ready.then(()=>{for(const e of document.querySelectorAll('.fitop')){let s=40;while(e.scrollWidth>e.clientWidth&&s>24){s-=1;e.style.fontSize=s+'pt'}}})</script>"
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}{js}</body></html>'
    doc = doc if LANG == "EN" else translate_html(doc)
    return fit_titles(doc)


def fit_titles(doc):
    """Shrink island-opener titles that would overflow (measured with the real Baloo 2 ExtraBold metrics)."""
    import html as HH
    f = fitz.Font(fontfile=f"{R}/fonts/ttf/Baloo2-800.ttf")
    def sub(m):
        w = float(m.group(1)); txt = HH.unescape(m.group(3))
        size = 40.0
        while f.text_length(txt, size) > w - 4 and size > 22:
            size -= 1
        return m.group(0).replace("font:800 40pt/1", f"font:800 {size:.0f}pt/1")
    return re.sub(r'width:([\d.]+)pt;white-space:nowrap;(font:800 40pt/1 \'Baloo 2\';color:[^"]+)" class="fitop">([^<]+)<', sub, doc)


# =========================================================================================================== VOLUME 2 overrides
from spec import MISSIONS, NEW_PAGE


def island_of(n):
    cur = None
    for key, op, a, b in MISSIONS:
        if n >= op:
            cur = key
    return None if n >= 91 else cur


def p_title():
    STAMPS.append((1, "leonluz", (150, 240, 470, 584)))
    return section(f"""
      <div class="a" style="left:0;right:0;top:88pt;text-align:center;font:800 44pt/1 'Baloo 2'">Leon’s Thinking Book</div>
      <div class="a" style="left:0;right:0;top:146pt;text-align:center;font:600 15pt 'Lexend';color:#2E6FD0">Volume 2 · Ages 6–8</div>
      <div class="a" style="left:0;right:0;top:620pt;text-align:center;font:400 16pt 'Andika';color:{NAVY}">Learning to think, not just learning to answer.</div>
      <div class="a" style="left:0;right:0;top:700pt;text-align:center;font:400 12.5pt 'Andika'">Written and illustrated by <b>Robert de Farias</b></div>""", "#fff")


def p_credits():
    t = ("<b>Leon’s Thinking Book — Volume 2 (Ages 6–8)</b><br>Written and illustrated by Robert de Farias<br><br>"
         "Copyright © 2026 Robert de Farias. All rights reserved. Artwork and paintings © Robert de Farias.<br>"
         "No part of this book may be reproduced without written permission from the author, except for copying activity pages "
         "for personal or classroom use.<br><br>First edition. Independently published.<br><br>"
         "<b>Safety:</b> For children aged 6 and up. Use colored pencils or crayons.<br><br>"
         "This book offers playful practice for children. It is not a test, a diagnosis or a substitute for advice "
         "from a teacher or health professional.")
    return section(f'<div class="a" style="left:51pt;width:420pt;bottom:90pt;font:400 10pt/1.45 \'Andika\';color:{GRAY}">{t}</div>', "#fff")


HELLO1 = [
    ("p", "<i>Leon’s Thinking Book, Volume 2</i> is for children aged 6 to 8. Its idea is simple: <b>learning to think, not just learning to answer.</b>"),
    ("p", "The games are a step up from Volume 1: more steps, more rules to keep in mind and more puzzles to plan. Your child goes on 12 missions:"),
    ("ul2", ["<b>Missions 1–3:</b> paying attention, keeping information in mind, remembering what you see.",
             "<b>Missions 4–6:</b> logic, patterns and numbers.",
             "<b>Missions 7–9:</b> words, space and solving problems.",
             "<b>Missions 10–12:</b> planning, feelings and a final big challenge."]),
    ("p", "Each mission opens with a painting by the artist Robert de Farias, the author of this book. Take a moment to look at it together — there are no wrong answers when you talk about art."),
    ("h", "Before you start"),
    ("ul2", ["Most children can read the instructions alone. Stay nearby to help.",
             "Pages with an ear icon need you to read something aloud.",
             "Pages with an eye icon: look, then turn the page.",
             "Keep it short: one or two pages at a time is plenty."]),
]
HELLO2 = [
    ("h", "How to help without giving the answer"),
    ("p", "<b>Ask, don’t tell.</b> Try: “How did you work it out?” “Is there another way?” “What would Leon do?”"),
    ("p", "<b>Give a small clue, not the answer.</b> Point to one row, or cover part of the page: “Look at the top. Is it there?”"),
    ("p", "<b>Mistakes are part of thinking.</b> Leon makes mistakes too — and then he tries again. You can say: “Interesting! Let’s check together.” or “Oops, like Leon! What could we try now?”"),
    ("p", "<b>Praise the effort.</b> Instead of “Clever!”, try: “You looked very carefully!” “You didn’t give up!” “You found a new way!”"),
    ("p", "<b>Three stars mean a real challenge.</b> It is fine to need help or to try twice. Explaining an answer out loud is great thinking practice."),
    ("p", "<b>Look for the little boxes:</b> <i>Parent’s Little Tip</i>, <i>Ask Leon</i>, <i>Talk About It</i> and <i>Try Another Way</i> give you short ideas for each page."),
    ("p", "The answers are at the back of the book (pages 92–95). Some pages have many good answers. Talk about them together!"),
    ("p2", "This book offers playful practice. It is not a test, a diagnosis or a substitute for advice from a teacher or health professional."),
]

OVERRIDE = {}
NEW_ROWS = [(o[0], "Art Detective", a) for o, a in zip(OPENERS, [
    "There are many small circles. Any 3 are right.", "Red.", "It is on the right side of the painting.",
    "Any answer with a reason.", "Any place where the lines turn is right.", "More than 20.",
    "Any invented name is great.", "Any way along the blue lines.", "Count together. Any careful count is fine.",
    "Any path from top to bottom.", "There is no wrong answer. Talk about it.", "Any colors your child finds."])] + [
    (NEW_PAGE, "Remember the order", "1: red, green, blue. 2: black, yellow, red, brown. 3: blue, brown, green, yellow, black. Any order your child repeats correctly is right.")]

SEQ_TILES = [("tile_red", "red"), ("tile_blue", "blue"), ("tile_honey", "yellow"), ("tile_green", "green"), ("tile_black", "black"), ("tile_sepia", "brown")]


def p24():
    n, isl = NEW_PAGE, "m2"
    x0, x1 = box_x(n)
    bw = x1 - x0
    d = 128
    sp = (bw - 3 * d) / 2
    out = []
    for i, (k, name) in enumerate(SEQ_TILES):
        c, r = i % 3, i // 3
        x, y = x0 + c * (d + sp), 180 + r * (d + 60)
        out.append(f'<div class="a" style="left:{x}pt;top:{y}pt;width:{d}pt;height:{d}pt;border-radius:50%;overflow:hidden;'
                   f'box-shadow:0 0 0 3pt #fff,0 0 0 4.2pt {BORDER}"><img src="{ART}/{k}.jpg" style="width:100%;height:100%;object-fit:cover;display:block"></div>'
                   f'<div class="a" style="left:{x}pt;width:{d}pt;top:{y + d + 12}pt;text-align:center;font:700 14pt \'Andika\'">{name}</div>')
    gu = ("Read one line at a time, once. Your child points to the circles in the same order. "
          "1. “Red, green, blue.” 2. “Black, yellow, red, brown.” 3. “Blue, brown, green, yellow, black.”")
    ear = (f'<svg class="a" style="right:{PW - x1}pt;top:84pt" width="26pt" height="26pt" viewBox="0 0 24 24"><path d="M7 9a5 5 0 0 1 10 0c0 3-3 4-3 7a3 3 0 0 1-6 0" '
           f'fill="none" stroke="{NAVY}" stroke-width="2.2" stroke-linecap="round"/><path d="M10 9a2 2 0 0 1 4 0" fill="none" stroke="{NAVY}" stroke-width="2"/></svg>')
    return section(header(n, isl, 3, "Remember the order", "Listen to your grown-up. Then point to the painted circles in the same order.")
                   + ear + "".join(out) + pbox(n, "For grown-ups", gu, 570)
                   + pbox(n, "Try Another Way", "Make up a color order for your grown-up to remember!", 650) + footer(n, isl), BGC)


def html_pages(bottoms):
    STAMPS.clear()
    act = {a[0]: a for a in ACT}
    op = {o[0]: o for o in OPENERS}
    secs = {}
    secs[1] = p_title(); secs[2] = p_credits()
    secs[3] = section("")
    secs[4] = p_hello(4, HELLO1, True); secs[5] = p_hello(5, HELLO2, False)
    secs[6] = p_meet(); secs[7] = p_howto()
    secs[8] = section(footer_plain(8)); secs[9] = section(footer_plain(9))
    for n, o in op.items():
        secs[n] = p_opener(*o)
    secs[NEW_PAGE] = p24()
    for n, a in act.items():
        secs[n] = overlay(n, a, bottoms)
    secs[91] = section("")
    ans = answers_pages()
    assert len(ans) <= 4, f"answers need {len(ans)} pages"
    while len(ans) < 4:
        ans.append(section(footer_plain(ANS_FIRST + len(ans)), "#fff"))
    for i, s in enumerate(ans):
        secs[ANS_FIRST + i] = s
    secs[96] = section("")
    missing = [n for n in range(1, 97) if n not in secs]
    assert not missing, missing
    body = "".join(secs[n] for n in range(1, 97))
    doc = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    doc = doc if LANG == "EN" else translate_html(doc)
    return fit_titles(doc)
