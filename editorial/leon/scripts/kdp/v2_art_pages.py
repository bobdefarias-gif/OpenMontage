"""Volume 2 (ages 6–8) — the 20 'art map' pages in EN / FR / NL. Same template rules as v1_art_pages.
Faces (works 11, 14, 05) are allowed in Volume 2 only. IMG_0403 is never used."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from v1_art_pages import (MAN, A, NAVY, GRAY, RED, BORDER, PW, PH, box, lens, img, fit, letter, card, text, dot,
                          empty_circle, EYE, UI)
import v1_art_pages as V1

T = {
 8: {"EN": ("Detail detective", "Three circles come from this face. One does not. Circle it."),
     "FR": ("Détective des détails", "Trois ronds viennent de ce visage. Un seul n’en vient pas. Entoure-le."),
     "NL": ("Detailspeurder", "Drie rondjes komen uit dit gezicht. Eén niet. Omcirkel dat rondje.")},
 11: {"EN": ("Only blue circles", "Count only the blue circles. Write how many."),
      "FR": ("Seulement les ronds bleus", "Compte seulement les ronds bleus. Écris combien."),
      "NL": ("Alleen blauwe rondjes", "Tel alleen de blauwe rondjes. Schrijf hoeveel.")},
 12: {"EN": ("Odd one out PRO", "In each row, one circle comes from a different painting. Circle it."),
      "FR": ("L’intrus PRO", "Dans chaque ligne, un rond vient d’un autre tableau. Entoure-le."),
      "NL": ("Wie hoort er niet bij? PRO", "In elke rij komt één rondje uit een ander schilderij. Omcirkel het.")},
 15: {"EN": ("Shopping list", "Listen to the list only once. Circle the 5 colors."),
      "FR": ("La liste de courses", "Écoute la liste une seule fois. Entoure les 5 couleurs."),
      "NL": ("Boodschappenlijstje", "Luister maar één keer naar het lijstje. Omcirkel de 5 kleuren.")},
 19: {"EN": ("Leon’s secret path", "Put your finger on the bird. Listen to the steps. On which circle do you stop?"),
      "FR": ("Le chemin secret de Leon", "Mets ton doigt sur l’oiseau. Écoute les pas. Sur quel rond t’arrêtes-tu ?"),
      "NL": ("Leons geheime pad", "Zet je vinger op de vogel. Luister naar de stappen. Op welk rondje stop je?")},
 20: {"EN": ("Copy the grid", "Look at the top grid. Draw a dot of the same color in the same squares below."),
      "FR": ("Recopie la grille", "Regarde la grille du haut. Dessine un point de la même couleur dans les mêmes cases en bas."),
      "NL": ("Teken het rooster na", "Kijk naar het bovenste rooster. Zet een stip in dezelfde kleur in dezelfde vakjes onderaan.")},
 21: {"EN": ("In Robert’s studio", "Look at the picture for 30 seconds. Then turn the page."),
      "FR": ("Dans l’atelier de Robert", "Regarde l’image pendant 30 secondes. Puis tourne la page."),
      "NL": ("In het atelier van Robert", "Kijk 30 tellen naar het prentje. Sla dan de bladzijde om.")},
 22: {"EN": ("What do you remember?", "Answer from memory. Circle the right answer."),
      "FR": ("De quoi te souviens-tu ?", "Réponds de mémoire. Entoure la bonne réponse."),
      "NL": ("Wat weet je nog?", "Antwoord uit je geheugen. Omcirkel het juiste antwoord.")},
 23: {"EN": ("Color squares", "Remember which squares have a circle, and which color. Then turn the page."),
      "FR": ("Les cases de couleur", "Retiens quelles cases ont un rond, et de quelle couleur. Puis tourne la page."),
      "NL": ("Gekleurde vakjes", "Onthoud welke vakjes een rondje hebben, en welke kleur. Sla dan de bladzijde om.")},
 24: {"EN": ("Build it again", "Color the same squares with the same colors."),
      "FR": ("Reconstruis-la", "Colorie les mêmes cases avec les mêmes couleurs."),
      "NL": ("Bouw het opnieuw", "Kleur dezelfde vakjes met dezelfde kleuren.")},
 27: {"EN": ("Who is who?", "Read the clues. Write each name under the right picture."),
      "FR": ("Qui est qui ?", "Lis les indices. Écris chaque prénom sous la bonne image."),
      "NL": ("Wie is wie?", "Lees de aanwijzingen. Schrijf elke naam onder het juiste prentje.")},
 28: {"EN": ("Picture sudoku", "Each color once in every row, every column and every thick box. Draw a dot of the missing color."),
      "FR": ("Sudoku en images", "Chaque couleur une fois par ligne, par colonne et par grand carré. Dessine un point de la couleur qui manque."),
      "NL": ("Prentjessudoku", "Elke kleur één keer in elke rij, kolom en dik vak. Zet een stip in de kleur die ontbreekt.")},
 29: {"EN": ("Picture pairs", "Each circle comes from one painting. Draw a line from each circle to its painting."),
      "FR": ("Les paires", "Chaque rond vient d’un tableau. Relie chaque rond à son tableau."),
      "NL": ("Prentjesparen", "Elk rondje komt uit een schilderij. Verbind elk rondje met zijn schilderij.")},
 30: {"EN": ("True or false?", "Look at the bird. Read each sentence. Circle T if it is true or F if it is false."),
      "FR": ("Vrai ou faux ?", "Regarde l’oiseau. Lis chaque phrase. Entoure V si c’est vrai ou F si c’est faux."),
      "NL": ("Waar of niet waar?", "Kijk naar de vogel. Lees elke zin. Omcirkel W als het waar is of N als het niet waar is.")},
 32: {"EN": ("Blue, red or both?", "Write each number in the right place. Some go in the middle. Some go outside!"),
      "FR": ("Bleu, rouge ou les deux ?", "Écris chaque numéro au bon endroit. Certains vont au milieu. D’autres dehors !"),
      "NL": ("Blauw, rood of allebei?", "Schrijf elk nummer op de juiste plek. Sommige horen in het midden. Sommige erbuiten!")},
 34: {"EN": ("Growing circles", "Look how the picture grows. How many circles will step 4 have? Draw them."),
      "FR": ("Les ronds qui grandissent", "Regarde comment l’image grandit. Combien de ronds à l’étape 4 ? Dessine-les."),
      "NL": ("Groeiende rondjes", "Kijk hoe het prentje groeit. Hoeveel rondjes heeft stap 4? Teken ze.")},
 53: {"EN": ("Grid drawing", "Copy Robert’s lines square by square into the empty grid."),
      "FR": ("Dessin quadrillé", "Recopie les lignes de Robert case par case dans la grille vide."),
      "NL": ("Tekenen op een rooster", "Teken de lijnen van Robert vakje per vakje na in het lege rooster.")},
 55: {"EN": ("Turned around", "Which circle is the target, only turned? Circle it."),
      "FR": ("Retourné", "Quel rond est la cible, seulement tournée ? Entoure-le."),
      "NL": ("Gedraaid", "Welk rondje is het doel, alleen gedraaid? Omcirkel het.")},
 62: {"EN": ("Fair share", "Share the 12 circles fairly between Leon, Luz and you. How many does each get?"),
      "FR": ("Partage juste", "Partage les 12 ronds entre Leon, Luz et toi. Combien chacun en a-t-il ?"),
      "NL": ("Eerlijk delen", "Verdeel de 12 rondjes eerlijk tussen Leon, Luz en jou. Hoeveel krijgt ieder?")},
 66: {"EN": ("Sort it twice", "Write each letter in the right box of the table."),
      "FR": ("Trie deux fois", "Écris chaque lettre dans la bonne case du tableau."),
      "NL": ("Twee keer sorteren", "Schrijf elke letter in het juiste vak van de tabel.")},
}
X = {  # extra UI strings
 "grown": {"EN": "For grown-ups: read once:", "FR": "Pour l’adulte : lire une fois :", "NL": "Voor volwassenen: lees één keer voor:"},
 "list": {"EN": "red, black, green, blue, yellow", "FR": "rouge, noir, vert, bleu, jaune", "NL": "rood, zwart, groen, blauw, geel"},
 "steps": {"EN": "2 squares right, 1 square up, 1 square right.", "FR": "2 cases à droite, 1 case en haut, 1 case à droite.",
           "NL": "2 vakjes naar rechts, 1 vakje omhoog, 1 vakje naar rechts."},
 "q1": {"EN": "How many circles were there?", "FR": "Combien y avait-il de ronds ?", "NL": "Hoeveel rondjes waren er?"},
 "q2": {"EN": "Where was the bird looking?", "FR": "De quel côté regardait l’oiseau ?", "NL": "Naar waar keek de vogel?"},
 "q3": {"EN": "What color was the top circle?", "FR": "De quelle couleur était le rond du haut ?", "NL": "Welke kleur had het bovenste rondje?"},
 "red": {"EN": "red", "FR": "rouge", "NL": "rood"}, "blue": {"EN": "blue", "FR": "bleu", "NL": "blauw"},
 "green": {"EN": "green", "FR": "vert", "NL": "groen"},
 "clues": {"EN": ["Mo has a green background.", "Lia is made of triangles.", "Tom is made of stripes."],
           "FR": ["Mo a un fond vert.", "Lia est faite de triangles.", "Tom est fait de rayures."],
           "NL": ["Mo heeft een groene achtergrond.", "Lia is gemaakt van driehoekjes.", "Tom is gemaakt van strepen."]},
 "tf": {"EN": ["The bird has two black legs.", "The bird is only red.", "The bird has yellow on its body.", "The bird stands on a tree."],
        "FR": ["L’oiseau a deux pattes noires.", "L’oiseau est tout rouge.", "L’oiseau a du jaune sur le corps.", "L’oiseau est sur un arbre."],
        "NL": ["De vogel heeft twee zwarte poten.", "De vogel is helemaal rood.", "De vogel heeft geel op zijn lijf.", "De vogel staat op een boom."]},
 "TF": {"EN": ("T", "F"), "FR": ("V", "F"), "NL": ("W", "N")},
 "venn": {"EN": ("Blue", "Red"), "FR": ("Bleu", "Rouge"), "NL": ("Blauw", "Rood")},
 "step": {"EN": "Step", "FR": "Étape", "NL": "Stap"},
 "each": {"EN": "Each one gets:", "FR": "Chacun reçoit :", "NL": "Ieder krijgt:"},
 "you": {"EN": "You", "FR": "Toi", "NL": "Jij"},
 "target": {"EN": "Target", "FR": "Cible", "NL": "Doel"},
 "cols": {"EN": ("One color", "Many colors"), "FR": ("Une couleur", "Plusieurs couleurs"), "NL": ("Eén kleur", "Veel kleuren")},
 "rows": {"EN": ("A face", "No face"), "FR": ("Un visage", "Pas de visage"), "NL": ("Een gezicht", "Geen gezicht")},
}

ANSWERS = {
 8: {"EN": "C (it comes from another painting).", "FR": "C (il vient d’un autre tableau).", "NL": "C (komt uit een ander schilderij)."},
 11: {"EN": "7 blue circles.", "FR": "7 ronds bleus.", "NL": "7 blauwe rondjes."},
 12: {"EN": "Row 1: 4th. Row 2: 2nd. Row 3: 5th. Row 4: 1st.", "FR": "Ligne 1 : 4e. Ligne 2 : 2e. Ligne 3 : 5e. Ligne 4 : 1er.",
      "NL": "Rij 1: 4de. Rij 2: 2de. Rij 3: 5de. Rij 4: 1ste."},
 15: {"EN": "Red, black, green, blue, yellow (not the brown circle, not the bird).",
      "FR": "Rouge, noir, vert, bleu, jaune (pas le rond brun, pas l’oiseau).",
      "NL": "Rood, zwart, groen, blauw, geel (niet het bruine rondje, niet de vogel)."},
 19: {"EN": "The red circle.", "FR": "Le rond rouge.", "NL": "Het rode rondje."},
 20: {"EN": "Same squares and colors as the top grid.", "FR": "Mêmes cases et mêmes couleurs que la grille du haut.",
      "NL": "Dezelfde vakjes en kleuren als het bovenste rooster."},
 22: {"EN": "1: 3 circles. 2: to the right →. 3: blue.", "FR": "1 : 3 ronds. 2 : à droite →. 3 : bleu.", "NL": "1: 3 rondjes. 2: naar rechts →. 3: blauw."},
 24: {"EN": "Top left red, top right blue, middle yellow, bottom left green.", "FR": "En haut à gauche rouge, en haut à droite bleu, au milieu jaune, en bas à gauche vert.",
      "NL": "Linksboven rood, rechtsboven blauw, midden geel, linksonder groen."},
 27: {"EN": "1 Tom, 2 Lia, 3 Mo.", "FR": "1 Tom, 2 Lia, 3 Mo.", "NL": "1 Tom, 2 Lia, 3 Mo."},
 28: {"EN": "Row 1: yellow (3rd). Row 2: black (2nd). Row 3: blue (1st), yellow (4th). Row 4: yellow (2nd), blue (3rd).",
      "FR": "Ligne 1 : jaune (3e). Ligne 2 : noir (2e). Ligne 3 : bleu (1er), jaune (4e). Ligne 4 : jaune (2e), bleu (3e).",
      "NL": "Rij 1: geel (3de). Rij 2: zwart (2de). Rij 3: blauw (1ste), geel (4de). Rij 4: geel (2de), blauw (3de)."},
 29: {"EN": "Circle 1 → painting 2. Circle 2 → painting 3. Circle 3 → painting 1.",
      "FR": "Rond 1 → tableau 2. Rond 2 → tableau 3. Rond 3 → tableau 1.", "NL": "Rondje 1 → schilderij 2. Rondje 2 → schilderij 3. Rondje 3 → schilderij 1."},
 30: {"EN": "1 T, 2 F, 3 T, 4 F.", "FR": "1 V, 2 F, 3 V, 4 F.", "NL": "1 W, 2 N, 3 W, 4 N."},
 32: {"EN": "Blue: 1. Red: 2. Middle: 3. Outside: 4 and 5.", "FR": "Bleu : 1. Rouge : 2. Milieu : 3. Dehors : 4 et 5.",
      "NL": "Blauw: 1. Rood: 2. Midden: 3. Erbuiten: 4 en 5."},
 34: {"EN": "7 circles (2 more each step).", "FR": "7 ronds (2 de plus à chaque étape).", "NL": "7 rondjes (elke stap 2 meer)."},
 53: {"EN": "A drawing that follows the lines square by square.", "FR": "Un dessin qui suit les lignes case par case.",
      "NL": "Een tekening die de lijnen vakje per vakje volgt."},
 55: {"EN": "B.", "FR": "B.", "NL": "B."},
 62: {"EN": "4 each.", "FR": "4 chacun.", "NL": "4 voor ieder."},
 66: {"EN": "A face + one color: A, B. A face + many colors: C. No face + one color: D, F. No face + many colors: E.",
      "FR": "Visage + une couleur : A, B. Visage + plusieurs couleurs : C. Sans visage + une couleur : D, F. Sans visage + plusieurs couleurs : E.",
      "NL": "Gezicht + één kleur: A, B. Gezicht + veel kleuren: C. Geen gezicht + één kleur: D, F. Geen gezicht + veel kleuren: E."},
}


def note(n, lang, body, y=690):
    x0, x1 = box(n)
    return (f'<div style="position:absolute;left:{x0}pt;width:{x1 - x0}pt;top:{y}pt;background:#FFF8E1;border:1.5pt solid #F7C93E;border-radius:10pt;'
            f'padding:8pt 12pt;font:11pt/1.35 \'DejaVu Sans\';color:{NAVY}"><b>{X["grown"][lang]}</b> {body}</div>')


def p8(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    out = [card(x0, 160, bw, 380)]
    w, h = fit("face14", bw - 40, 340)
    out.append(img("face14", x0 + (bw - w) / 2, 180 + (340 - h) / 2, w=w)[0])
    d = 100; sp = (bw - 4 * d) / 3
    for i, (k, lab) in enumerate([("det_0", "A"), ("det_1", "B"), ("det_x", "C"), ("det_2", "D")]):
        x = x0 + i * (d + sp)
        out.append(lens(k, x, 562, d)); out.append(letter(lab, x + d / 2 - 15, 562 + d + 12))
    return "".join(out)


GRID11 = ["blue", "red", "honey", "blue", "black", "green", "sepia", "blue", "red", "honey", "black", "blue", "green",
          "red", "sepia", "honey", "blue", "black", "green", "red", "blue", "sepia", "honey", "black", "blue"]


def p11(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    d = 74; gap = (bw - 5 * d - 20) / 4
    out = [card(x0, 160, bw, 5 * (d + 14) + 30)]
    for i, k in enumerate(GRID11):
        c, r = i % 5, i // 5
        out.append(lens(f"tile_{k}", x0 + 10 + c * (d + gap), 178 + r * (d + 14), d))
    out.append(f'<div style="position:absolute;left:{x1 - 90}pt;top:670pt;width:90pt;height:56pt;border:2.2pt solid {NAVY};border-radius:10pt;background:#fff"></div>')
    return "".join(out)


ROWS12 = [["pro_a06", "pro_b06", "pro_c06", "pro_x10", "pro_d06"], ["pro_a07", "pro_x09", "pro_b07", "pro_c07", "pro_d07"],
          ["pro_a15", "pro_b15", "pro_c15", "pro_d15", "pro_x03"], ["pro_x12", "pro_a08", "pro_b08", "pro_c08", "pro_d08"]]


def p12(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    d, top, rowh = 82, 172, 138
    gap = (bw - 40 - 5 * d) / 4
    out = []
    for r, row in enumerate(ROWS12):
        y = top + r * rowh
        out.append(card(x0, y - 14, bw, d + 28)); out.append(text(str(r + 1), x0 + 10, y + d / 2 - 12, 18, color=GRAY))
        for c, k in enumerate(row):
            out.append(lens(k, x0 + 34 + c * (d + gap), y, d))
    return "".join(out)


SHOP = ["red", "sepia", "black", "multi", "green", "blue", "honey", "green_light"]


def p15(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    d = 106; sp = (bw - 4 * d) / 3
    out = []
    tiles = ["tile_red", "tile_sepia", "tile_black", "bird", "tile_green", "tile_blue", "tile_honey"]
    for i, k in enumerate(tiles):
        c, r = i % 4, i // 4
        x, y = x0 + c * (d + sp) + (r * (d + sp) / 2), 200 + r * (d + 70)
        if k == "bird":
            w, h = fit(k, d + 10, d)
            out.append(img(k, x - 5, y + (d - h) / 2, w=w)[0])
        else:
            out.append(lens(k, x, y, d))
    out.append(note(n, lang, X["list"][lang], 560))
    return "".join(out)


def _grid(x, y, cols, rows, cell, labels=False):
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(f'<div style="position:absolute;left:{x + c * cell}pt;top:{y + r * cell}pt;width:{cell}pt;height:{cell}pt;border:1.6pt solid {BORDER};background:#fff"></div>')
    if labels:
        for c in range(cols):
            out.append(text("ABCDE"[c], x + c * cell, y - 22, 13, w=cell, align="center", color=GRAY))
        for r in range(rows):
            out.append(text(str(r + 1), x - 22, y + r * cell + cell / 2 - 9, 13, color=GRAY))
    return out


def p19(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    cell = 88; gx = x0 + (bw - 5 * cell) / 2 + 10; gy = 190
    out = _grid(gx, gy, 5, 4, cell, labels=True)
    w, h = fit("bird", cell - 10, cell - 16)
    out.append(img("bird", gx + 5, gy + 3 * cell + (cell - h) / 2, w=w)[0])            # A4
    for (c, r, k) in [(3, 2, "tile_red"), (2, 2, "tile_blue"), (4, 3, "tile_green"), (2, 0, "tile_honey"), (4, 1, "tile_black"), (1, 1, "tile_sepia")]:
        out.append(lens(k, gx + c * cell + 12, gy + r * cell + 12, cell - 24))
    out.append(note(n, lang, X["steps"][lang], 560))
    return "".join(out)


TOP20 = {(0, 0): "red", (1, 2): "blue", (2, 1): "honey", (3, 3): "green", (0, 3): "black"}


def p20(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    cell = 60; gx = x0 + (bw - 4 * cell) / 2
    out = _grid(gx, 168, 4, 4, cell) + _grid(gx, 450, 4, 4, cell)
    for (r, c), k in TOP20.items():
        out.append(lens(f"tile_{k}", gx + c * cell + 6, 168 + r * cell + 6, cell - 12, ring=1.5))
    return "".join(out)


def p21(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    out = [card(x0, 170, bw, 470)]
    w, h = fit("bird", 300, 160)
    out.append(img("bird", x0 + 30, 440, w=w)[0])
    out.append(lens("tile_blue", x0 + bw - 170, 200, 120))
    out.append(lens("tile_red", x0 + 60, 270, 110))
    out.append(lens("tile_green", x0 + bw - 150, 400, 100))
    return "".join(out) + V1.turn(lang, n)


def p22(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    out = []
    qs = [(X["q1"][lang], ["2", "3", "4"]), (X["q2"][lang], ["←", "→"]),
          (X["q3"][lang], [X["red"][lang], X["blue"][lang], X["green"][lang]])]
    for i, (q, opts) in enumerate(qs):
        y = 175 + i * 180
        out.append(card(x0, y, bw, 150))
        out.append(text(f"{i + 1}. {q}", x0 + 20, y + 20, 16))
        ow = (bw - 40) / len(opts)
        for j, o in enumerate(opts):
            out.append(f'<div style="position:absolute;left:{x0 + 20 + j * ow + ow / 2 - 55}pt;top:{y + 70}pt;width:110pt;height:50pt;border:2pt solid {BORDER};'
                       f'border-radius:25pt;background:#fff;display:flex;align-items:center;justify-content:center;font:bold 18pt \'DejaVu Sans\';color:{NAVY}">{o}</div>')
    return "".join(out)


POS23 = {(0, 0): "red", (0, 2): "blue", (1, 1): "honey", (2, 0): "green"}


def p23(n, lang, fill=True):
    x0, x1 = box(n); bw = x1 - x0
    cell = 130; gx = x0 + (bw - 3 * cell) / 2
    out = _grid(gx, 190, 3, 3, cell)
    if fill:
        for (r, c), k in POS23.items():
            out.append(lens(f"tile_{k}", gx + c * cell + 14, 190 + r * cell + 14, cell - 28))
        out.append(V1.turn(lang, n))
    return "".join(out)


def p24(n, lang):
    return p23(n, lang, fill=False)


def p27(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    cw = (bw - 28) / 3
    out = []
    for i, k in enumerate(["work11", "work14", "work05"]):
        x = x0 + i * (cw + 14)
        out.append(card(x, 168, cw, 290))
        w, h = fit(k, cw - 20, 200)
        out.append(img(k, x + (cw - w) / 2, 180 + (200 - h) / 2, w=w)[0])
        out.append(text(str(i + 1), x + 10, 392, 13, color=GRAY))
        out.append(f'<div style="position:absolute;left:{x + 16}pt;top:430pt;width:{cw - 32}pt;border-bottom:2pt solid {NAVY}"></div>')
    for j, c in enumerate(X["clues"][lang]):
        out.append(text("• " + c, x0 + 10, 500 + j * 34, 15, weight="normal"))
    return "".join(out)


SUDO = [["red", "blue", None, "black"], ["honey", None, "red", "blue"], [None, "red", "black", None], ["black", None, None, "red"]]


def p28(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    cell = 108; gx = x0 + (bw - 4 * cell) / 2
    out = _grid(gx, 172, 4, 4, cell)
    out.append(f'<div style="position:absolute;left:{gx}pt;top:172pt;width:{4 * cell}pt;height:{4 * cell}pt;border:4pt solid {NAVY}"></div>')
    out.append(f'<div style="position:absolute;left:{gx + 2 * cell - 2}pt;top:172pt;width:4pt;height:{4 * cell}pt;background:{NAVY}"></div>')
    out.append(f'<div style="position:absolute;left:{gx}pt;top:{172 + 2 * cell - 2}pt;width:{4 * cell}pt;height:4pt;background:{NAVY}"></div>')
    for r in range(4):
        for c in range(4):
            k = SUDO[r][c]
            x, y = gx + c * cell + 14, 172 + r * cell + 14
            out.append(lens(f"tile_{k}", x, y, cell - 28) if k else empty_circle(x, y, cell - 28))
    return "".join(out)


def p29(n, lang):
    x0, x1 = box(n)
    out = []
    for i, k in enumerate(["painting12", "painting15", "painting02"]):
        y = 175 + i * 185
        out.append(card(x1 - 250, y, 250, 160))
        w, h = fit(k, 220, 132)
        out.append(img(k, x1 - 235 + (220 - w) / 2, y + 14 + (132 - h) / 2, w=w)[0])
        out.append(text(str(i + 1), x1 - 250 + 10, y + 130, 13, color=GRAY))
        out.append(dot(x1 - 250 - 22, y + 80))
    for i, k in enumerate(["tile_blue", "tile_honey", "tile_multi"]):
        y = 175 + i * 185 + 15
        out.append(lens(k, x0, y, 130)); out.append(text(str(i + 1), x0 - 2, y - 6, 13, color=GRAY))
        out.append(dot(x0 + 150, y + 65))
    return "".join(out)


def p30(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    out = [card(x0, 165, bw, 230)]
    w, h = fit("bird", bw - 40, 200)
    out.append(img("bird", x0 + (bw - w) / 2, 180 + (200 - h) / 2, w=w)[0])
    t, f = X["TF"][lang]
    for i, s in enumerate(X["tf"][lang]):
        y = 420 + i * 72
        out.append(card(x0, y, bw, 60))
        out.append(text(f"{i + 1}. {s}", x0 + 18, y + 18, 15, weight="normal"))
        for j, ch in enumerate((t, f)):
            out.append(letter(ch, x1 - 90 + j * 42, y + 14, 32))
    return "".join(out)


def p32(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    cx = x0 + bw / 2
    out = [f'<svg style="position:absolute;left:0;top:0" width="{PW}pt" height="{PH}pt" viewBox="0 0 {PW} {PH}">'
           f'<rect x="{x0}" y="160" width="{bw}" height="330" rx="14" fill="#fff" stroke="{BORDER}" stroke-width="2"/>'
           f'<circle cx="{cx - 80}" cy="330" r="140" fill="rgba(60,90,200,.08)" stroke="#3B5BC8" stroke-width="3"/>'
           f'<circle cx="{cx + 80}" cy="330" r="140" fill="rgba(224,83,61,.08)" stroke="{RED}" stroke-width="3"/></svg>']
    a, b = X["venn"][lang]
    out.append(text(a, cx - 220, 178, 16, color="#3B5BC8")); out.append(text(b, cx + 150, 178, 16, color=RED))
    tiles = ["tile_blue", "tile_red", "odd_r2_c3", "tile_honey", "tile_black"]
    d = 84; sp = (bw - 5 * d) / 4
    for i, k in enumerate(tiles):
        x = x0 + i * (d + sp)
        out.append(lens(k, x, 540, d)); out.append(text(str(i + 1), x, 540 + d + 10, 18, w=d, align="center"))
    return "".join(out)


def p34(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    cw = (bw - 3 * 12) / 4
    out = []
    counts = [1, 3, 5, None]
    for i, cnt in enumerate(counts):
        x = x0 + i * (cw + 12)
        out.append(card(x, 200, cw, 380, extra="" if cnt else f"border:2.4pt dashed {NAVY}"))
        out.append(text(f'{X["step"][lang]} {i + 1}', x, 215, 14, w=cw, align="center", color=GRAY))
        if cnt:
            for j in range(cnt):
                out.append(lens("tile_red" if j % 2 == 0 else "tile_blue", x + cw / 2 - 22, 250 + j * 46, 44, ring=1.5))
    out.append(f'<div style="position:absolute;left:{x1 - 90}pt;top:620pt;width:90pt;height:56pt;border:2.2pt solid {NAVY};border-radius:10pt;background:#fff"></div>')
    return "".join(out)


def p53(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    size = 240; gx = x0 + (bw - size) / 2
    out = [f'<div style="position:absolute;left:{gx}pt;top:165pt;width:{size}pt;height:{size}pt;overflow:hidden;border:2pt solid {NAVY}">'
           f'<img src="{A}/griddraw.jpg" style="position:absolute;left:-{size * .207:.1f}pt;top:-{size * .207:.1f}pt;width:{size * 1.414:.1f}pt"></div>']
    for y0 in (165, 440):
        for i in range(1, 4):
            out.append(f'<div style="position:absolute;left:{gx + i * size / 4}pt;top:{y0}pt;width:1.4pt;height:{size}pt;background:{RED};opacity:.7"></div>')
            out.append(f'<div style="position:absolute;left:{gx}pt;top:{y0 + i * size / 4}pt;width:{size}pt;height:1.4pt;background:{RED};opacity:.7"></div>')
    out.append(f'<div style="position:absolute;left:{gx}pt;top:440pt;width:{size}pt;height:{size}pt;border:2pt solid {NAVY};background:#fff"></div>')
    for i in range(1, 4):
        out.append(f'<div style="position:absolute;left:{gx + i * size / 4}pt;top:440pt;width:1.4pt;height:{size}pt;background:{RED};opacity:.7"></div>')
        out.append(f'<div style="position:absolute;left:{gx}pt;top:{440 + i * size / 4}pt;width:{size}pt;height:1.4pt;background:{RED};opacity:.7"></div>')
    return "".join(out)


def p55(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    out = [card(x0 + bw / 2 - 110, 165, 220, 250)]
    out.append(lens("turn_target", x0 + bw / 2 - 80, 185, 160))
    out.append(text(X["target"][lang], x0, 380, 16, w=bw, align="center"))
    d = 130; sp = (bw - 3 * d) / 2
    for i, (k, lab) in enumerate([("turn_other_rot", "A"), ("turn_rot", "B"), ("turn_x", "C")]):
        x = x0 + i * (d + sp)
        out.append(lens(k, x, 470, d)); out.append(letter(lab, x + d / 2 - 15, 470 + d + 14))
    return "".join(out)


def p62(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    out = [card(x0, 165, bw, 210)]
    for i in range(12):
        c, r = i % 6, i // 6
        out.append(lens(["tile_red", "tile_blue", "tile_honey"][i % 3], x0 + 22 + c * ((bw - 44) / 6) + 4, 185 + r * 92, 72, ring=1.5))
    pw = (bw - 28) / 3
    for j, name in enumerate(["Leon", "Luz", X["you"][lang]]):
        x = x0 + j * (pw + 14)
        out.append(f'<div style="position:absolute;left:{x}pt;top:410pt;width:{pw}pt;height:{pw}pt;border-radius:50%;border:3pt solid {BORDER};background:#fff"></div>')
        out.append(text(name, x, 410 + pw + 10, 16, w=pw, align="center"))
    out.append(text(X["each"][lang], x0, 680, 16))
    out.append(f'<div style="position:absolute;left:{x0 + 170}pt;top:668pt;width:80pt;height:46pt;border:2.2pt solid {NAVY};border-radius:10pt;background:#fff"></div>')
    return "".join(out)


def p66(n, lang):
    x0, x1 = box(n); bw = x1 - x0
    cw = (bw - 5 * 10) / 6
    out = []
    for i, k in enumerate(["work11", "work14", "work05", "work07", "work12", "work15"]):
        x = x0 + i * (cw + 10)
        out.append(card(x, 165, cw, 120))
        w, h = fit(k, cw - 12, 80)
        out.append(img(k, x + (cw - w) / 2, 172 + (80 - h) / 2, w=w)[0])
        out.append(text("ABCDEF"[i], x, 258, 15, w=cw, align="center"))
    c1, c2 = X["cols"][lang]; r1, r2 = X["rows"][lang]
    tx, ty, hw, rh = x0 + 120, 330, (bw - 120) / 2, 160
    out.append(text(c1, tx, ty, 15, w=hw, align="center")); out.append(text(c2, tx + hw, ty, 15, w=hw, align="center"))
    for r, lab in enumerate((r1, r2)):
        y = ty + 34 + r * rh
        out.append(text(lab, x0, y + rh / 2 - 12, 15, w=110))
        for c in range(2):
            out.append(f'<div style="position:absolute;left:{tx + c * hw}pt;top:{y}pt;width:{hw}pt;height:{rh}pt;border:2pt solid {NAVY};background:#fff"></div>')
    return "".join(out)


PAGES = {8: p8, 11: p11, 12: p12, 15: p15, 19: p19, 20: p20, 21: p21, 22: p22, 23: p23, 24: p24, 27: p27, 28: p28, 29: p29,
         30: p30, 32: p32, 34: p34, 53: p53, 55: p55, 62: p62, 66: p66}


def header(n, lang):
    saved = V1.T
    V1.T = T
    try:
        return V1.header(n, lang)
    finally:
        V1.T = saved


def html(lang):
    pages = [f'<section class="page">{header(n, lang)}{fn(n, lang)}{V1.credit(n, lang)}</section>' for n, fn in PAGES.items()]
    css = (f"@page{{size:{PW}pt {PH}pt;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}"
           f"html,body{{background:transparent}}.page{{width:{PW}pt;height:{PH}pt;position:relative;overflow:hidden;page-break-after:always}}")
    js = """<script>for(const e of document.querySelectorAll('.fit')){let s=33;while(e.scrollWidth>e.clientWidth&&s>20){s-=1;e.style.fontSize=s+'pt'}}</script>"""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{"".join(pages)}{js}</body></html>'
