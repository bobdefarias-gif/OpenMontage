"""Volume 1 — the 19 'art map' pages, in EN / FR / NL.

Each page is rendered as a TRANSPARENT overlay (HTML -> PDF) and later stamped on top of the original
interior page, whose header stars and footer are kept. Styling reproduces the original template exactly:
title Liberation Sans Bold 33 pt, instruction DejaVu Sans Bold 18 pt, navy #1E2A5A, light border #D5DAE0.

Content rules: real artworks only (crop / scale / separate from paper / compose — never redrawn),
no IMG_0403, no faces in V1, every answer checkable in 10 seconds (see ANSWERS).
"""
import json, os

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(R, "art")
MAN = json.load(open(f"{ART}/manifest.json"))
NAVY, GRAY, RED, GOLD, BORDER, BG = "#1E2A5A", "#5F6B78", "#E0533D", "#F7C93E", "#D5DAE0", "#F4F7FA"
SHADOW = "#6B7280"
PW, PH = 621, 810


def box(n):
    """content box (x0, x1) like the original: even pages 51..578, odd pages 42..569"""
    return (51, 578) if n % 2 == 0 else (42, 569)


# ----------------------------------------------------------------------------- strings
T = {
 10: {"EN": ("Odd one out", "Three circles in each row come from the same painting. Circle the one with different colors."),
      "FR": ("L’intrus", "Dans chaque ligne, trois ronds viennent du même tableau. Entoure celui qui a d’autres couleurs."),
      "NL": ("Wie hoort er niet bij?", "In elke rij komen drie rondjes uit hetzelfde schilderij. Omcirkel het rondje met andere kleuren.")},
 14: {"EN": ("Find the shadow", "This is Robert’s bird. Which shadow belongs to it? Circle the letter."),
      "FR": ("Trouve l’ombre", "Voici l’oiseau de Robert. Quelle ombre est la sienne ? Entoure la lettre."),
      "NL": ("Zoek de schaduw", "Dit is de vogel van Robert. Welke schaduw hoort bij hem? Omcirkel de letter.")},
 17: {"EN": ("Look and remember", "Look at the three circles for 10 seconds. Then turn the page."),
      "FR": ("Regarde et retiens", "Regarde les trois ronds pendant 10 secondes. Puis tourne la page."),
      "NL": ("Kijk en onthoud", "Kijk 10 tellen naar de drie rondjes. Sla dan de bladzijde om.")},
 18: {"EN": ("What did you see?", "Three of these circles were on the page before. Circle them."),
      "FR": ("Qu’as-tu vu ?", "Trois de ces ronds étaient sur la page d’avant. Entoure-les."),
      "NL": ("Wat heb je gezien?", "Drie van deze rondjes stonden op de vorige bladzijde. Omcirkel ze.")},
 19: {"EN": ("Three colors", "Remember the colors of the circles, from 1 to 3. Then turn the page."),
      "FR": ("Trois couleurs", "Retiens les couleurs des ronds, de 1 à 3. Puis tourne la page."),
      "NL": ("Drie kleuren", "Onthoud de kleuren van de rondjes, van 1 tot 3. Sla dan de bladzijde om.")},
 20: {"EN": ("Color the circles", "Color the circles in the same order you saw."),
      "FR": ("Colorie les ronds", "Colorie les ronds dans le même ordre que tu as vu."),
      "NL": ("Kleur de rondjes", "Kleur de rondjes in dezelfde volgorde als je zag.")},
 21: {"EN": ("Robert’s window", "Look at the four circles for 10 seconds. Then turn the page."),
      "FR": ("La fenêtre de Robert", "Regarde les quatre ronds pendant 10 secondes. Puis tourne la page."),
      "NL": ("Het raam van Robert", "Kijk 10 tellen naar de vier rondjes. Sla dan de bladzijde om.")},
 22: {"EN": ("What is missing?", "One circle is missing. Which one? Circle the letter."),
      "FR": ("Qu’est-ce qui manque ?", "Il manque un rond. Lequel ? Entoure la lettre."),
      "NL": ("Wat ontbreekt er?", "Er ontbreekt een rondje. Welk? Omcirkel de letter.")},
 28: {"EN": ("Big and small", "Circle the biggest one. Draw a line under the smallest one."),
      "FR": ("Grand et petit", "Entoure le plus grand. Souligne le plus petit."),
      "NL": ("Groot en klein", "Omcirkel de grootste. Zet een streep onder de kleinste.")},
 30: {"EN": ("What comes next?", "Look at the colors in each row. Which circle comes next? Circle A or B."),
      "FR": ("Et après ?", "Regarde les couleurs de chaque ligne. Quel rond vient ensuite ? Entoure A ou B."),
      "NL": ("Wat komt er nu?", "Kijk naar de kleuren in elke rij. Welk rondje komt nu? Omcirkel A of B.")},
 31: {"EN": ("Bead necklace", "Finish the necklace. Color the white beads to keep the pattern."),
      "FR": ("Le collier de perles", "Termine le collier. Colorie les perles blanches pour continuer le motif."),
      "NL": ("Kralenketting", "Maak de ketting af. Kleur de witte kralen zodat het patroon klopt.")},
 33: {"EN": ("Big, small, big", "Look at the sizes. Which one comes next? Circle A or B."),
      "FR": ("Grand, petit, grand", "Regarde les tailles. Lequel vient ensuite ? Entoure A ou B."),
      "NL": ("Groot, klein, groot", "Kijk naar de groottes. Welke komt nu? Omcirkel A of B.")},
 36: {"EN": ("What goes together?", "Draw a line from each circle to the painting it comes from."),
      "FR": ("Ce qui va ensemble", "Relie chaque rond au tableau d’où il vient."),
      "NL": ("Wat hoort bij elkaar?", "Trek een lijn van elk rondje naar het schilderij waar het uit komt.")},
 37: {"EN": ("One color or many?", "Draw a line from each picture to the right box."),
      "FR": ("Une couleur ou plusieurs ?", "Relie chaque image à la bonne boîte."),
      "NL": ("Eén kleur of veel?", "Trek een lijn van elk prentje naar het juiste vak.")},
 42: {"EN": ("Leon’s color grid", "Each color goes once in every row and every column. Color the 3 empty squares."),
      "FR": ("La grille de Leon", "Chaque couleur va une fois dans chaque ligne et chaque colonne. Colorie les 3 cases vides."),
      "NL": ("Leons kleurenrooster", "Elke kleur staat één keer in elke rij en elke kolom. Kleur de 3 lege vakjes.")},
 43: {"EN": ("How many?", "Count the pictures in each row. Circle the number."),
      "FR": ("Combien ?", "Compte les images de chaque ligne. Entoure le nombre."),
      "NL": ("Hoeveel?", "Tel de prentjes in elke rij. Omcirkel het getal.")},
 45: {"EN": ("Which has more?", "In each row, circle the box with more."),
      "FR": ("Où y en a-t-il plus ?", "Dans chaque ligne, entoure la boîte qui en a le plus."),
      "NL": ("Waar zijn er meer?", "Omcirkel in elke rij het vak met de meeste.")},
 60: {"EN": ("Top shelf", "Circle the things on the top shelf."),
      "FR": ("L’étagère du haut", "Entoure les choses sur l’étagère du haut."),
      "NL": ("Het bovenste rek", "Omcirkel de dingen op het bovenste rek.")},
 64: {"EN": ("Where is this piece?", "Only one circle comes from this painting. Which one? Circle the letter."),
      "FR": ("D’où vient ce morceau ?", "Un seul rond vient de ce tableau. Lequel ? Entoure la lettre."),
      "NL": ("Waar komt dit stukje vandaan?", "Maar één rondje komt uit dit schilderij. Welk? Omcirkel de letter.")},
}
UI = {
 "turn": {"EN": "Now turn the page!", "FR": "Maintenant, tourne la page !", "NL": "Sla nu de bladzijde om!"},
 "next": {"EN": "Which one is next?", "FR": "Lequel vient ensuite ?", "NL": "Welke komt nu?"},
 "one": {"EN": "One color", "FR": "Une couleur", "NL": "Eén kleur"},
 "many": {"EN": "Many colors", "FR": "Plusieurs couleurs", "NL": "Veel kleuren"},
 "credit": {"EN": "Artwork: Robert de Farias", "FR": "Œuvres : Robert de Farias", "NL": "Kunstwerken: Robert de Farias"},
}

# ----------------------------------------------------------------------------- answers (page -> text per language)
ANSWERS = {
 10: {"EN": "Row 1: 3rd. Row 2: 1st. Row 3: 4th. Row 4: 2nd.", "FR": "Ligne 1 : 3e. Ligne 2 : 1er. Ligne 3 : 4e. Ligne 4 : 2e.",
      "NL": "Rij 1: 3de. Rij 2: 1ste. Rij 3: 4de. Rij 4: 2de."},
 14: {"EN": "C (the bird the right way up).", "FR": "C (l’oiseau à l’endroit).", "NL": "C (de vogel rechtop)."},
 18: {"EN": "1st, 3rd and 5th circles (black, blue, yellow-brown).", "FR": "1er, 3e et 5e ronds (noir, bleu, jaune-brun).",
      "NL": "1ste, 3de en 5de rondje (zwart, blauw, geelbruin)."},
 20: {"EN": "1 red, 2 blue, 3 green.", "FR": "1 rouge, 2 bleu, 3 vert.", "NL": "1 rood, 2 blauw, 3 groen."},
 22: {"EN": "B (the red circle).", "FR": "B (le rond rouge).", "NL": "B (het rode rondje)."},
 28: {"EN": "Biggest: row 1 → 2nd, row 2 → 3rd, row 3 → 1st. Smallest: row 1 → 3rd, row 2 → 1st, row 3 → 2nd.",
      "FR": "Le plus grand : ligne 1 → 2e, ligne 2 → 3e, ligne 3 → 1er. Le plus petit : ligne 1 → 3e, ligne 2 → 1er, ligne 3 → 2e.",
      "NL": "Grootste: rij 1 → 2de, rij 2 → 3de, rij 3 → 1ste. Kleinste: rij 1 → 3de, rij 2 → 1ste, rij 3 → 2de."},
 30: {"EN": "Row 1: B. Row 2: A. Row 3: A.", "FR": "Ligne 1 : B. Ligne 2 : A. Ligne 3 : A.", "NL": "Rij 1: B. Rij 2: A. Rij 3: A."},
 31: {"EN": "Red, blue, red, blue.", "FR": "Rouge, bleu, rouge, bleu.", "NL": "Rood, blauw, rood, blauw."},
 33: {"EN": "Row 1: A (small). Row 2: B (big). Row 3: A (small).", "FR": "Ligne 1 : A (petit). Ligne 2 : B (grand). Ligne 3 : A (petit).",
      "NL": "Rij 1: A (klein). Rij 2: B (groot). Rij 3: A (klein)."},
 36: {"EN": "Circle 1 → painting 3. Circle 2 → painting 1. Circle 3 → painting 2.",
      "FR": "Rond 1 → tableau 3. Rond 2 → tableau 1. Rond 3 → tableau 2.",
      "NL": "Rondje 1 → schilderij 3. Rondje 2 → schilderij 1. Rondje 3 → schilderij 2."},
 37: {"EN": "One color: 1, 3, 5. Many colors: 2, 4, 6.", "FR": "Une couleur : 1, 3, 5. Plusieurs couleurs : 2, 4, 6.",
      "NL": "Eén kleur: 1, 3, 5. Veel kleuren: 2, 4, 6."},
 42: {"EN": "Top right: yellow. Middle left: blue. Bottom middle: red.", "FR": "En haut à droite : jaune. Au milieu à gauche : bleu. En bas au milieu : rouge.",
      "NL": "Rechtsboven: geel. Links in het midden: blauw. Onderaan in het midden: rood."},
 43: {"EN": "3, 2, 5, 4.", "FR": "3, 2, 5, 4.", "NL": "3, 2, 5, 4."},
 45: {"EN": "Row 1: right box. Row 2: left box. Row 3: right box.", "FR": "Ligne 1 : boîte de droite. Ligne 2 : boîte de gauche. Ligne 3 : boîte de droite.",
      "NL": "Rij 1: rechter vak. Rij 2: linker vak. Rij 3: rechter vak."},
 60: {"EN": "The bird and the blue circle.", "FR": "L’oiseau et le rond bleu.", "NL": "De vogel en het blauwe rondje."},
 64: {"EN": "B (top right of the painting).", "FR": "B (en haut à droite du tableau).", "NL": "B (rechtsboven in het schilderij)."},
}
THUMB_ANSWER = {64}   # answers that are a position in the art -> thumbnail with a red circle in the key

# ----------------------------------------------------------------------------- building blocks
A = "file://" + ART


def lens(tile, x, y, d, ring=3.0):
    return (f'<div style="position:absolute;left:{x:.1f}pt;top:{y:.1f}pt;width:{d}pt;height:{d}pt;border-radius:50%;'
            f'box-shadow:0 0 0 {ring}pt #fff,0 0 0 {ring + 1.2}pt {BORDER},0 3pt 8pt rgba(30,42,90,.10)">'
            f'<img src="{A}/{tile}.jpg" style="width:100%;height:100%;border-radius:50%;display:block;object-fit:cover"></div>')


def img(name, x, y, w=None, h=None, extra=""):
    m = MAN[name]
    if w and not h: h = w * m["h"] / m["w"]
    if h and not w: w = h * m["w"] / m["h"]
    ext = "jpg" if os.path.exists(f"{ART}/{name}.jpg") else "png"
    return f'<img src="{A}/{name}.{ext}" style="position:absolute;left:{x:.1f}pt;top:{y:.1f}pt;width:{w:.1f}pt;height:{h:.1f}pt;{extra}">', w, h


def fit(name, bw, bh):
    m = MAN[name]; a = m["w"] / m["h"]
    return (bw, bw / a) if bw / a <= bh else (bh * a, bh)


def letter(ch, x, y, s=30):
    return (f'<div style="position:absolute;left:{x:.1f}pt;top:{y:.1f}pt;width:{s}pt;height:{s}pt;border-radius:50%;border:2.2pt solid {NAVY};'
            f'background:#fff;display:flex;align-items:center;justify-content:center;font:bold {s * .55:.1f}pt \'DejaVu Sans\';color:{NAVY}">{ch}</div>')


def card(x, y, w, h, extra=""):
    return (f'<div style="position:absolute;left:{x:.1f}pt;top:{y:.1f}pt;width:{w:.1f}pt;height:{h:.1f}pt;background:#fff;'
            f'border:2pt solid {BORDER};border-radius:14pt;{extra}"></div>')


def text(s, x, y, size=16.5, w=None, align="left", color=NAVY, weight="bold"):
    ww = f"width:{w}pt;" if w else ""
    return (f'<div style="position:absolute;left:{x:.1f}pt;top:{y:.1f}pt;{ww}text-align:{align};font:{weight} {size}pt/1.25 \'DejaVu Sans\';color:{color}">{s}</div>')


def dot(x, y, r=4.5):
    return f'<div style="position:absolute;left:{x - r:.1f}pt;top:{y - r:.1f}pt;width:{2 * r}pt;height:{2 * r}pt;border-radius:50%;background:{NAVY}"></div>'


def empty_circle(x, y, d, dashed=True, mark=""):
    st = "dashed" if dashed else "solid"
    return (f'<div style="position:absolute;left:{x:.1f}pt;top:{y:.1f}pt;width:{d}pt;height:{d}pt;border-radius:50%;background:#fff;'
            f'border:2.4pt {st} {NAVY};display:flex;align-items:center;justify-content:center;font:bold {d * .38:.0f}pt \'DejaVu Sans\';color:{NAVY}">{mark}</div>')


EYE = (f'<svg width="40pt" height="26pt" viewBox="0 0 34 22"><path d="M2 11C8 2 26 2 32 11C26 20 8 20 2 11Z" fill="#fff" stroke="{NAVY}" stroke-width="2.4"/>'
       f'<circle cx="17" cy="11" r="5" fill="{NAVY}"/><circle cx="19" cy="9" r="1.6" fill="#fff"/></svg>')


def turn(lang, n, y=690):
    x0, x1 = box(n)
    return (f'<div style="position:absolute;left:{x0}pt;width:{x1 - x0}pt;top:{y}pt;display:flex;flex-direction:column;align-items:center;gap:6pt">'
            f'{EYE}<div style="font:bold 16.5pt \'DejaVu Sans\';color:{NAVY}">{UI["turn"][lang]}</div></div>')


def header(n, lang):
    x0, _ = box(n)
    title, ins = T[n][lang]
    star_x = 468 if n % 2 else 477
    return (f'<div style="position:absolute;left:{x0}pt;top:41.5pt;width:{star_x - x0 - 10}pt;font:bold 33pt/1.15 \'Liberation Sans\';color:{NAVY};white-space:nowrap;'
            f'overflow:visible" class="fit">{title}</div>'
            f'<div style="position:absolute;left:{x0}pt;top:87pt;width:{star_x - x0 + 20}pt;font:bold 18pt/23.3pt \'DejaVu Sans\';color:{NAVY}" class="ins">{ins}</div>')


def credit(n, lang):
    x0, x1 = box(n)
    return f'<div style="position:absolute;left:{x0}pt;top:738pt;font:9pt \'DejaVu Sans\';color:{GRAY}">{UI["credit"][lang]}</div>'


# ----------------------------------------------------------------------------- pages
def p10(n, lang):
    x0, x1 = box(n)
    d, gap, top, rowh = 100, 24, 175, 138
    total = 4 * d + 3 * gap
    xs = x0 + 34 + ((x1 - x0 - 34) - total) / 2
    out = []
    for r in range(4):
        y = top + r * rowh
        out.append(card(x0, y - 16, x1 - x0, d + 32))
        out.append(text(str(r + 1), x0 + 14, y + d / 2 - 13, 20, color=GRAY))
        for c in range(4):
            out.append(lens(f"odd_r{r}_c{c}", xs + c * (d + gap), y, d))
    return "".join(out)


def p14(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    out = []
    out.append(card(x0, 160, bw, 250))
    b, w, h = img("bird", x0 + 24, 0, w=bw - 48)
    out.append(b.replace("top:0.0pt", f"top:{160 + (250 - h) / 2:.1f}pt"))
    cw = (bw - 2 * 14) / 3
    for i, (k, lab) in enumerate([("sh_creature", "A"), ("sh_bird_flip", "B"), ("sh_bird", "C")]):
        x = x0 + i * (cw + 14)
        out.append(card(x, 440, cw, 200))
        sw, sh = fit(k, cw - 26, 120)
        out.append(img(k, x + (cw - sw) / 2, 440 + 20 + (120 - sh) / 2, w=sw)[0])
        out.append(letter(lab, x + cw / 2 - 16, 440 + 152, 32))
    return "".join(out)


SHOW17 = ["tile_honey", "tile_blue", "tile_black"]
ASK18 = ["tile_black", "tile_sepia", "tile_blue", "tile_red", "tile_honey", "tile_green"]


def p17(n, lang):
    x0, x1 = box(n)
    bw, d = x1 - x0, 160
    out = [card(x0, 170, bw, 470)]
    pos = [(x0 + 24, 200), (x0 + bw / 2 - d / 2, 420 - 30), (x1 - 24 - d, 200)]
    out += [lens(k, x, y, d) for k, (x, y) in zip(SHOW17, pos)]
    return "".join(out) + turn(lang, n)


def p18(n, lang):
    x0, x1 = box(n)
    bw, d = x1 - x0, 136
    sp = (bw - 3 * d) / 2
    out = []
    for i, k in enumerate(ASK18):
        c, r = i % 3, i // 3
        out.append(lens(k, x0 + c * (d + sp), 200 + r * (d + 90), d))
    return "".join(out)


SEQ19 = ["tile_red", "tile_blue", "tile_green"]


def p19(n, lang):
    x0, x1 = box(n)
    bw, d = x1 - x0, 140
    sp = (bw - 3 * d - 40) / 2
    out = [card(x0, 220, bw, 300)]
    for i, k in enumerate(SEQ19):
        x = x0 + 20 + i * (d + sp)
        out.append(lens(k, x, 260, d))
        out.append(text(str(i + 1), x, 260 + d + 22, 22, w=d, align="center"))
    return "".join(out) + turn(lang, n)


def p20(n, lang):
    x0, x1 = box(n)
    bw, d = x1 - x0, 140
    sp = (bw - 3 * d - 40) / 2
    out = [card(x0, 220, bw, 300)]
    for i in range(3):
        x = x0 + 20 + i * (d + sp)
        out.append(empty_circle(x, 260, d, dashed=False))
        out.append(text(str(i + 1), x, 260 + d + 22, 22, w=d, align="center"))
    return "".join(out)


GRID21 = ["tile_honey", "tile_black", "tile_red", "tile_green"]


def _grid4(n, tiles, missing=None):
    x0, x1 = box(n)
    bw, d = x1 - x0, 140 if missing is None else 118
    gx = 46
    left = x0 + (bw - 2 * d - gx) / 2
    out = [card(left - 34, 172, 2 * d + gx + 68, 2 * d + 92,
                extra=f"border:7pt solid {NAVY};border-radius:10pt")]
    for i, k in enumerate(tiles):
        c, r = i % 2, i // 2
        x, y = left + c * (d + gx), 200 + r * (d + 36)
        out.append(empty_circle(x, y, d, mark="?") if i == missing else lens(k, x, y, d))
    return out


def p21(n, lang):
    return "".join(_grid4(n, GRID21)) + turn(lang, n)


def p22(n, lang):
    x0, x1 = box(n)
    out = _grid4(n, GRID21, missing=2)
    d = 96
    sp = ((x1 - x0) - 3 * d) / 2
    for i, (k, lab) in enumerate([("tile_blue", "A"), ("tile_red", "B"), ("tile_sepia", "C")]):
        x = x0 + i * (d + sp)
        out.append(lens(k, x, 548, d))
        out.append(letter(lab, x + d / 2 - 15, 548 + d + 14))
    return "".join(out)


ROWS28 = [("bird", [.62, 1.0, .36]), ("creature", [.38, .66, 1.0]), ("tile_multi", [1.0, .40, .66])]


def p28(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    out = []
    for r, (k, sizes) in enumerate(ROWS28):
        y = 168 + r * 190
        out.append(card(x0, y, bw, 172))
        cw = bw / 3
        for i, s in enumerate(sizes):
            if k.startswith("tile"):
                d = 140 * s
                out.append(lens(k, x0 + i * cw + (cw - d) / 2, y + 86 - d / 2, d))
            else:
                w, h = fit(k, (cw - 16) * s, 140 * s)
                out.append(img(k, x0 + i * cw + (cw - w) / 2, y + 86 - h / 2, w=w)[0])
    return "".join(out)


ROWS30 = [(["tile_blue", "tile_red", "tile_blue", "tile_red", "tile_blue"], ["tile_honey", "tile_red"]),
          (["tile_black", "tile_black", "tile_sepia", "tile_black", "tile_black"], ["tile_sepia", "tile_black"]),
          (["tile_red", "tile_honey", "tile_blue", "tile_red", "tile_honey"], ["tile_blue", "tile_green"])]


def p30(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    d, g = 64, 11
    out = []
    for r, (seq, opts) in enumerate(ROWS30):
        y = 168 + r * 186
        out.append(card(x0, y, bw, 170))
        x = x0 + 20
        for k in seq:
            out.append(lens(k, x, y + 18, d)); x += d + g
        out.append(empty_circle(x, y + 18, d, mark="?"))
        out.append(text(UI["next"][lang], x0 + 20, y + 118, 13, color=GRAY, weight="normal"))
        for i, k in enumerate(opts):
            xx = x1 - 20 - (2 - i) * 98 + 4
            out.append(lens(k, xx, y + 100, 54))
            out.append(letter("AB"[i], xx + 60, y + 112, 28))
    return "".join(out)


NECK = ["tile_red", "tile_blue"] * 3


def p31(n, lang):
    import math
    x0, x1 = box(n)
    cx, cy, rx, ry = (x0 + x1) / 2, 215, (x1 - x0) / 2 - 48, 440
    beads, d = 10, 70
    pts = []
    for i in range(beads):
        t = math.pi * (1 - i / (beads - 1))
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    import itertools
    fine = [(cx + rx * math.cos(math.pi * (1 - j / 120)), cy + ry * math.sin(math.pi * (1 - j / 120))) for j in range(121)]
    path = " ".join(f"{'M' if j == 0 else 'L'}{x:.1f} {y:.1f}" for j, (x, y) in enumerate(fine))
    out = [f'<svg style="position:absolute;left:0;top:0" width="{PW}pt" height="{PH}pt" viewBox="0 0 {PW} {PH}">'
           f'<path d="{path}" fill="none" stroke="{GRAY}" stroke-width="2.5"/></svg>']
    for i in range(beads):
        x, y = pts[i][0] - d / 2, pts[i][1] - d / 2
        out.append(lens(NECK[i], x, y, d) if i < 6 else empty_circle(x, y, d, dashed=False))
    return "".join(out)


ROWS33 = [("bird", [1, 0, 1, 0, 1], ("big", "small"), 0),         # next = small? -> pattern B S B S B -> next small
          ("creature", [0, 0, 1, 0, 0], ("small", "big"), 1),
          ("tile_multi", [1, 0, 0, 1, 0], ("small", "big"), 0)]
# NB row 1: B S B S B -> next is SMALL; option order (small, big) so answer A — keep ANSWERS in sync
ROWS33[0] = ("bird", [1, 0, 1, 0, 1], ("small", "big"), 0)


def p33(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    out = []
    for r, (k, seq, opts, _) in enumerate(ROWS33):
        y = 168 + r * 186
        out.append(card(x0, y, bw, 170))
        slot = 66
        x = x0 + 16
        for s in seq + [None]:
            if s is None:
                out.append(empty_circle(x + 4, y + 22, slot - 8, mark="?"))
            elif k.startswith("tile"):
                dd = 58 if s else 30
                out.append(lens(k, x + (slot - dd) / 2, y + 22 + (slot - 8 - dd) / 2 + 4, dd))
            else:
                w, h = fit(k, (slot - 4) * (1 if s else .55), 60 * (1 if s else .55))
                out.append(img(k, x + (slot - w) / 2, y + 22 + (slot - h) / 2, w=w)[0])
            x += slot + 6
        out.append(text(UI["next"][lang], x0 + 20, y + 118, 13, color=GRAY, weight="normal"))
        for i, o in enumerate(opts):
            xx = x1 - 20 - (2 - i) * 104 + 4
            sz = 1 if o == "big" else .55
            if k.startswith("tile"):
                dd = 58 * sz
                out.append(lens(k, xx + (60 - dd) / 2, y + 96 + (60 - dd) / 2, dd))
            else:
                w, h = fit(k, 60 * sz, 56 * sz)
                out.append(img(k, xx + (60 - w) / 2, y + 96 + (60 - h) / 2, w=w)[0])
            out.append(letter("AB"[i], xx + 66, y + 112, 28))
    return "".join(out)


PAINT36 = ["painting12", "painting15", "painting02"]          # left, numbered 1-3
LENS36 = ["tile_honey", "tile_multi", "tile_blue"]            # right, numbered 1-3 -> 3, 1, 2


def p36(n, lang):
    x0, x1 = box(n)
    out = []
    for i, k in enumerate(PAINT36):
        y = 175 + i * 185
        out.append(card(x0, y, 250, 160))
        w, h = fit(k, 220, 132)
        out.append(img(k, x0 + 15 + (220 - w) / 2, y + 14 + (132 - h) / 2, w=w)[0])
        out.append(text(str(i + 1), x0 - 4 + 262, y + 66, 14, color=GRAY))
        out.append(dot(x0 + 250 + 22, y + 80))
    for i, k in enumerate(LENS36):
        y = 175 + i * 185 + 15
        out.append(dot(x1 - 150, y + 65))
        out.append(lens(k, x1 - 132, y, 130))
    return "".join(out)


SORT37 = ["work07", "work12", "work15", "work13", "work01", "work04"]   # one, many, one, many, one, many


def p37(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    cw = (bw - 2 * 14) / 3
    out = []
    for i, k in enumerate(SORT37):
        c, r = i % 3, i // 3
        x, y = x0 + c * (cw + 14), 170 + r * 205
        out.append(card(x, y, cw, 175))
        w, h = fit(k, cw - 24, 120)
        out.append(img(k, x + (cw - w) / 2, y + 14 + (120 - h) / 2, w=w)[0])
        out.append(text(str(i + 1), x + 12, y + 145, 13, color=GRAY))
        out.append(dot(x + cw / 2, y + 158))
    bx = (bw - 30) / 2
    for j, key in enumerate(["one", "many"]):
        x = x0 + j * (bx + 30)
        out.append(card(x, 600, bx, 110, extra=f"border:3pt solid {NAVY}"))
        out.append(dot(x + bx / 2, 616))
        out.append(text(UI[key][lang], x, 660, 17, w=bx, align="center"))
    return "".join(out)


GRID42 = [["tile_red", "tile_blue", None], [None, "tile_honey", "tile_red"], ["tile_honey", None, "tile_blue"]]


def p42(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    cell = 150
    gx = x0 + (bw - 3 * cell) / 2
    out = [card(gx - 14, 176, 3 * cell + 28, 3 * cell + 28)]
    for r in range(3):
        for c in range(3):
            x, y = gx + c * cell, 190 + r * cell
            out.append(f'<div style="position:absolute;left:{x}pt;top:{y}pt;width:{cell}pt;height:{cell}pt;border:2pt solid {BORDER};background:#fff"></div>')
            k = GRID42[r][c]
            out.append(lens(k, x + 20, y + 20, cell - 40) if k else empty_circle(x + 20, y + 20, cell - 40, dashed=True))
    return "".join(out)


ROWS43 = [("bird", 3), ("creature", 2), ("tile_green", 5), ("bird", 4)]


def p43(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    out = []
    for r, (k, cnt) in enumerate(ROWS43):
        y = 168 + r * 140
        out.append(card(x0, y, bw, 124))
        for i in range(cnt):
            x = x0 + 14 + i * 64
            if k.startswith("tile"):
                out.append(lens(k, x + 4, y + 34, 54))
            else:
                w, h = fit(k, 60, 56)
                out.append(img(k, x, y + 62 - h / 2, w=w)[0])
        for j in range(5):
            xx = x1 - 14 - (5 - j) * 34
            out.append(f'<div style="position:absolute;left:{xx}pt;top:{y + 47}pt;width:30pt;height:30pt;border-radius:50%;'
                       f'border:2pt solid {BORDER};background:#fff;display:flex;align-items:center;justify-content:center;font:bold 16pt \'DejaVu Sans\';color:{NAVY}">{j + 1}</div>')
    return "".join(out)


ROWS45 = [("bird", 2, 4), ("tile_red", 5, 3), ("creature", 1, 3)]


def p45(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    half = (bw - 24) / 2
    out = []
    for r, (k, a, b) in enumerate(ROWS45):
        y = 168 + r * 185
        for side, cnt in enumerate((a, b)):
            x = x0 + side * (half + 24)
            out.append(card(x, y, half, 165))
            cols = 3
            for i in range(cnt):
                c, rr = i % cols, i // cols
                cx = x + 18 + c * ((half - 36) / cols)
                cy = y + 18 + rr * 70
                if k.startswith("tile"):
                    out.append(lens(k, cx + 10, cy + 4, 56))
                else:
                    w, h = fit(k, (half - 36) / cols - 8, 60)
                    out.append(img(k, cx + 4, cy + (64 - h) / 2, w=w)[0])
    return "".join(out)


def p60(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    out = []
    # a simple shelf: navy uprights + 3 boards (like the original's furniture)
    out.append(f'<div style="position:absolute;left:{x0 + 30}pt;top:170pt;width:{bw - 60}pt;height:560pt;border:6pt solid {NAVY};border-bottom:none;border-radius:8pt 8pt 0 0;background:#fff"></div>')
    for i in range(3):
        yb = 340 + i * 180
        out.append(f'<div style="position:absolute;left:{x0 + 20}pt;top:{yb}pt;width:{bw - 40}pt;height:9pt;background:{NAVY};border-radius:3pt"></div>')
    items = [  # (shelf, kind, name, size)
        (0, "img", "bird", 190), (0, "lens", "tile_blue", 120),
        (1, "img", "creature", 200), (1, "lens", "tile_honey", 120),
        (2, "lens", "tile_green", 120), (2, "lens", "tile_black", 120)]
    for idx, (s, kind, k, size) in enumerate(items):
        yb = 340 + s * 180
        slot = idx % 2
        cx = x0 + 60 + slot * ((bw - 120) / 2) + ((bw - 120) / 2) / 2
        if kind == "lens":
            out.append(lens(k, cx - size / 2, yb - size - 8, size))
        else:
            w, h = fit(k, size, 140)
            out.append(img(k, cx - w / 2, yb - h - 4, w=w)[0])
    return "".join(out)


def p64(n, lang):
    x0, x1 = box(n)
    bw = x1 - x0
    out = [card(x0, 160, bw, 360)]
    w, h = fit("painting12", bw - 40, 320)
    out.append(img("painting12", x0 + (bw - w) / 2, 180 + (320 - h) / 2, w=w)[0])
    d = 112
    sp = (bw - 3 * d) / 2
    for i, (k, lab) in enumerate([("piece_d1", "A"), ("piece_true", "B"), ("piece_d2", "C")]):
        x = x0 + i * (d + sp)
        out.append(lens(k, x, 548, d))
        out.append(letter(lab, x + d / 2 - 16, 548 + d + 14, 32))
    return "".join(out)


PAGES = {10: p10, 14: p14, 17: p17, 18: p18, 19: p19, 20: p20, 21: p21, 22: p22, 28: p28, 30: p30, 31: p31,
         33: p33, 36: p36, 37: p37, 42: p42, 43: p43, 45: p45, 60: p60, 64: p64}


def html(lang, only=None):
    pages = []
    for n, fn in PAGES.items():
        if only and n not in only: continue
        body = header(n, lang) + fn(n, lang) + credit(n, lang)
        pages.append(f'<section class="page" data-n="{n}">{body}</section>')
    css = (f"@page{{size:{PW}pt {PH}pt;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}"
           f"html,body{{background:transparent}}.page{{width:{PW}pt;height:{PH}pt;position:relative;overflow:hidden;page-break-after:always}}")
    # shrink long titles to fit the space left of the stars
    js = """<script>for(const e of document.querySelectorAll('.fit')){let s=33;while(e.scrollWidth>e.clientWidth&&s>20){s-=1;e.style.fontSize=s+'pt'}}</script>"""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(pages)}{js}</body></html>'


if __name__ == "__main__":
    os.makedirs(f"{R}/build/kdp", exist_ok=True)
    for lang in ("EN", "FR", "NL"):
        open(f"{R}/build/kdp/v1-art-{lang}.html", "w").write(html(lang))
    print("ok", list(PAGES))
