"""KDP full covers (back | spine | front), 17.4378 x 11.25 in, matte, Standard Color white, 80 pages.

Spine = 80 x 0.002347 in = 0.1878 in -> colour only, no text. Barcode zone 2 x 1.2 in, bottom right of the back cover,
left empty (white). Leon (the lion) is stamped as VECTOR from the interior's page 1.
"""
import fitz, os, sys, subprocess, html as H

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import v1_art_pages as V1

IN = 72
PAGES = int(os.environ.get('PAGES', 80))
BLEED, TRIM_W, TRIM_H, SPINE = .125 * IN, 8.5 * IN, 11 * IN, PAGES * 0.002347 * IN
CW, CH = 2 * BLEED + 2 * TRIM_W + SPINE, 2 * BLEED + TRIM_H          # 1255.52 x 810 pt
FX = BLEED + TRIM_W + SPINE                                         # front trim x
NAVY, RED, GOLD, GRAY = "#1E2A5A", "#E0533D", "#F7C93E", "#5F6B78"
A = V1.A

TXT = {
 ("V1", "EN"): dict(sub="Volume 1 · Ages 4–6", tag="Look, remember, count and think — with real art!", by="Written and illustrated by",
                    blurb=["Learning to think, not just learning to answer. Leon the lion and his friend Luz invite children aged 4 to 6 on a playful trip through 9 islands of games: looking closely, remembering, shapes, patterns, logic, numbers, words, space and feelings.",
                           "Each island opens with a real painting by the artist and author Robert de Farias. Leon tries, makes mistakes and tries again; Luz asks questions and celebrates new ideas.",
                           "Short activities, clear instructions to read aloud, and answers at the back that a grown-up can check in seconds."],
                    inside=["More than 60 playful activities", "Real artworks by the author", "Answers for grown-ups", "A certificate at the end"]),
 ("V1", "FR"): dict(sub="Volume 1 · 4–6 ans", tag="Regarder, retenir, compter, réfléchir… avec de l’art !", by="Texte et illustrations de",
                    blurb=["Apprendre à réfléchir, pas seulement à répondre. Leon le lion et son amie Luz invitent les enfants de 4 à 6 ans à un voyage ludique à travers 9 îles de jeux : bien regarder, retenir, les formes, les suites, la logique, les nombres, les mots, l’espace et les émotions.",
                           "Chaque île commence par une vraie peinture de l’artiste et auteur Robert de Farias. Leon essaie, se trompe et recommence ; Luz pose des questions et fête les nouvelles idées.",
                           "Des activités courtes, des consignes claires à lire à voix haute, et des réponses à la fin qu’un adulte vérifie en quelques secondes."],
                    inside=["Plus de 60 activités ludiques", "De vraies œuvres de l’auteur", "Réponses pour les adultes", "Un diplôme à la fin"]),
 ("V1", "NL"): dict(sub="Deel 1 · 4–6 jaar", tag="Kijken, onthouden, tellen en denken — met echte kunst!", by="Tekst en tekeningen:",
                    blurb=["Leren denken, niet alleen leren antwoorden. Leon de leeuw en zijn vriendin Luz nemen kinderen van 4 tot 6 jaar mee op een speelse reis langs 9 eilanden vol spelletjes: goed kijken, onthouden, vormen, reeksen, logica, getallen, woorden, ruimte en gevoelens.",
                           "Elk eiland begint met een echt schilderij van kunstenaar en auteur Robert de Farias. Leon probeert, vergist zich en probeert opnieuw; Luz stelt vragen en viert nieuwe ideeën.",
                           "Korte opdrachten, duidelijke instructies om voor te lezen en achteraan antwoorden die een volwassene in enkele seconden controleert."],
                    inside=["Meer dan 60 speelse opdrachten", "Echte kunstwerken van de auteur", "Antwoorden voor volwassenen", "Een diploma op het einde"]),
 ("V2", "EN"): dict(sub="Volume 2 · Ages 6–8", tag="Bigger puzzles, real art, more thinking!", by="Written and illustrated by",
                    blurb=["Volume 2 takes children aged 6 to 8 one step further: more steps, more rules to keep in mind and more puzzles to plan — from detail detectives and picture sudoku to codes, maps and the Final Big Challenge.",
                           "Many of the games are made with real artworks by Robert de Farias: children search his paintings, compare his lines and sort his pictures while they practise attention, memory and logic.",
                           "Clear instructions, a mission map to follow and answers at the back that a grown-up can check in seconds."],
                    inside=["More than 60 missions and puzzles", "Real artworks by the author", "Answers for grown-ups", "A certificate at the end"]),
 ("V2", "FR"): dict(sub="Volume 2 · 6–8 ans", tag="Plus d’énigmes, de vraies œuvres, encore plus de réflexion !", by="Texte et illustrations de",
                    blurb=["Le volume 2 emmène les enfants de 6 à 8 ans un cran plus loin : plus d’étapes, plus de règles à garder en tête et plus d’énigmes à planifier — du détective des détails au sudoku en images, en passant par les codes, les cartes et le Grand Défi final.",
                           "Beaucoup de jeux sont faits avec de vraies œuvres de Robert de Farias : l’enfant fouille ses tableaux, compare ses lignes et trie ses images tout en exerçant l’attention, la mémoire et la logique.",
                           "Des consignes claires, une carte de missions à suivre et des réponses à la fin qu’un adulte vérifie en quelques secondes."],
                    inside=["Plus de 60 missions et énigmes", "De vraies œuvres de l’auteur", "Réponses pour les adultes", "Un diplôme à la fin"]),
 ("V2", "NL"): dict(sub="Deel 2 · 6–8 jaar", tag="Grotere puzzels, echte kunst, nog meer denken!", by="Tekst en tekeningen:",
                    blurb=["Deel 2 neemt kinderen van 6 tot 8 jaar een stap verder: meer stappen, meer regels om te onthouden en meer puzzels om te plannen — van detailspeurder en prentjessudoku tot codes, kaarten en de Grote Eindopdracht.",
                           "Veel spelletjes zijn gemaakt met echte kunstwerken van Robert de Farias: kinderen zoeken in zijn schilderijen, vergelijken zijn lijnen en sorteren zijn prenten terwijl ze oefenen in opletten, onthouden en logisch denken.",
                           "Duidelijke instructies, een opdrachtenkaart en achteraan antwoorden die een volwassene in enkele seconden controleert."],
                    inside=["Meer dan 60 opdrachten en puzzels", "Echte kunstwerken van de auteur", "Antwoorden voor volwassenen", "Een diploma op het einde"]),
}
STYLE = {"V1": dict(accent=RED, art="bird", lenses=["cov_red", "cov_honey", "cov_blue", "cov_green", "cov_black"]),
         "V2": dict(accent="#2E6FD0", art="creature", lenses=["cov_blue", "cov_black", "cov_multi", "cov_sepia", "cov_red"])}


def cover_html(vol, lang):
    t, st = TXT[(vol, lang)], STYLE[vol]
    acc = st["accent"]
    b0 = BLEED
    # front: title block, lion (stamped later), art around it
    front = f"""
    <div style="position:absolute;left:{FX}pt;top:0;width:{TRIM_W + BLEED}pt;height:{CH}pt;background:#fff"></div>
    <div style="position:absolute;left:{FX}pt;top:0;width:{TRIM_W + BLEED}pt;height:{b0 + 150}pt;background:{acc}"></div>
    <div style="position:absolute;left:{FX + 36}pt;top:{b0 + 40}pt;width:{TRIM_W - 72}pt;text-align:center;font:bold 46pt/1.05 'Liberation Sans';color:#fff">Leon’s Thinking Book</div>
    <div style="position:absolute;left:{FX + 36}pt;top:{b0 + 102}pt;width:{TRIM_W - 72}pt;text-align:center;font:bold 19pt 'DejaVu Sans';color:#fff;opacity:.95">{H.escape(t['sub'])}</div>
    <div style="position:absolute;left:{FX + 40}pt;top:{b0 + 168}pt;width:{TRIM_W - 80}pt;text-align:center;font:bold 15.5pt/1.3 'DejaVu Sans';color:{NAVY}">{H.escape(t['tag'])}</div>
    """
    # ring of artwork circles around where the lion goes
    import math
    cx, cy, rr = FX + TRIM_W / 2, b0 + 475, 225
    ring = []
    for i, k in enumerate(st["lenses"]):
        a = math.radians(200 + i * 35)
        d = 96 if i % 2 == 0 else 78
        x, y = cx + rr * 1.12 * math.cos(a) - d / 2, cy + rr * math.sin(a) - d / 2
        ring.append(V1.lens(k, x, y, d, ring=3.5))
    art = st["art"]
    m = V1.MAN[art]
    aw = 250; ah = aw * m["h"] / m["w"]
    ring.append(f'<img src="{A}/{art}.png" style="position:absolute;left:{FX + TRIM_W - aw - 10}pt;top:{b0 + TRIM_H - 40 - ah}pt;width:{aw}pt;height:{ah}pt">')
    front += "".join(ring)
    front += (f'<div style="position:absolute;left:{FX + 36}pt;top:{b0 + TRIM_H - 58}pt;width:{TRIM_W - 72}pt;text-align:left;font:13pt \'DejaVu Sans\';color:{NAVY}">'
              f'{H.escape(t["by"])} <b>Robert de Farias</b></div>')
    # spine: colour only
    spine = f'<div style="position:absolute;left:{b0 + TRIM_W}pt;top:0;width:{SPINE}pt;height:{CH}pt;background:{NAVY}"></div>'
    # back
    bx = b0 + 48
    blurb = "".join(f'<p style="margin:0 0 11pt">{H.escape(p)}</p>' for p in t["blurb"])
    inside = "".join(f'<div style="display:flex;gap:8pt;align-items:center;margin:5pt 0"><span style="width:10pt;height:10pt;border-radius:50%;background:{acc};display:inline-block"></span>{H.escape(s)}</div>' for s in t["inside"])
    strip = "".join(V1.lens(k, bx + i * 86, b0 + 500, 70, ring=3) for i, k in enumerate(["cov_honey", "cov_blue", "cov_red", "cov_green"]))
    back = f"""
    <div style="position:absolute;left:0;top:0;width:{b0 + TRIM_W}pt;height:{CH}pt;background:#F4F7FA"></div>
    <div style="position:absolute;left:0;top:0;width:{b0 + TRIM_W}pt;height:{b0 + 14}pt;background:{acc}"></div>
    <div style="position:absolute;left:{bx}pt;top:{b0 + 54}pt;font:bold 26pt 'Liberation Sans';color:{NAVY}">Leon’s Thinking Book</div>
    <div style="position:absolute;left:{bx}pt;top:{b0 + 90}pt;font:bold 13pt 'DejaVu Sans';color:{acc}">{H.escape(t['sub'])}</div>
    <div style="position:absolute;left:{bx}pt;top:{b0 + 130}pt;width:{TRIM_W - 96}pt;font:12.5pt/1.45 'DejaVu Sans';color:{NAVY}">{blurb}</div>
    <div style="position:absolute;left:{bx}pt;top:{b0 + 380}pt;font:bold 12.5pt/1.3 'DejaVu Sans';color:{NAVY}">{inside}</div>
    {strip}
    <div style="position:absolute;left:{bx}pt;top:{b0 + 600}pt;width:300pt;font:9.5pt/1.4 'DejaVu Sans';color:{GRAY}">© 2026 Robert de Farias</div>
    <!-- barcode zone 2 x 1.2 in, kept empty (white) -->
    <div style="position:absolute;left:{b0 + TRIM_W - .25 * IN - 2 * IN}pt;top:{b0 + TRIM_H - .25 * IN - 1.2 * IN}pt;width:{2 * IN}pt;height:{1.2 * IN}pt;background:#fff"></div>
    """
    css = (f"@page{{size:{CW:.3f}pt {CH}pt;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}"
           f".page{{width:{CW:.3f}pt;height:{CH}pt;position:relative;overflow:hidden;background:#fff}}")
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><section class="page">{back}{spine}{front}</section></body></html>'


def build(vol, lang):
    out = f"{R}/build/kdp"
    hp = f"{out}/cover-{vol}-{lang}.html"
    open(hp, "w").write(cover_html(vol, lang))
    pdf = f"{out}/cover-{vol}-{lang}.raw.pdf"
    subprocess.run(["node", f"{R}/scripts/render.js", hp, pdf], check=True)
    doc = fitz.open(pdf)
    src = fitz.open(f"{R}/ref/leons-thinking-book-vol{vol[1]}-{lang}-interior.pdf")
    clip = fitz.Rect(112, 186, 526, 634)                    # Leon (+ Luz) on interior page 1, vector
    h = 300; w = h * clip.width / clip.height
    cx, cy = FX + TRIM_W / 2, BLEED + 475
    doc[0].show_pdf_page(fitz.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), src, 0, clip=clip)
    dst = os.environ.get("COVER_OUT") or f"{out}/leons-thinking-book-vol{vol[1]}-{lang}-cover.pdf"
    doc.save(dst, garbage=4, deflate=True)
    os.remove(pdf)
    return dst


if __name__ == "__main__":
    vols = sys.argv[1:] or ["V1", "V2"]
    for v in vols:
        for lang in ("EN", "FR", "NL"):
            print(build(v, lang))
