"""20 Facebook/Instagram posts x 3 languages (EN, FR, NL), 1080x1350.
Each language uses its own covers and interior pages. Same honesty rules as posts.py (no brain/medical claims, sourced facts).
python posts_i18n.py  ->  html_i18n/<LANG>/postNN.html"""
import os, re
from posts import CSS, NAVY, CORAL, TEAL, GOLD, CREAM, BLUE, A, ART

R = os.path.dirname(os.path.abspath(__file__))
LANGS = ("EN", "FR", "NL")

# key: (EN, FR, NL)   — {x} marks the highlighted part (wrapped in a coloured span by the layout)
TX = {
 "foot": ("Leon’s Thinking Book · ages 4–6 & 6–8", "Leon’s Thinking Book · 4–6 & 6–8 ans", "Leon’s Thinking Book · 4–6 & 6–8 jaar"),
 "by": ("by Robert de Farias", "par Robert de Farias", "door Robert de Farias"),
 # 1
 "k1": ("A simple swap", "Un petit échange", "Een kleine ruil"),
 "h1": ("Swap 15 minutes<br>of scrolling<br>for 15 minutes<br>of {thinking.}", "15 minutes<br>d’écran en moins,<br>15 minutes<br>de {réflexion.}", "Ruil 15 minuten<br>scrollen<br>voor 15 minuten<br>{denken.}"),
 "t1": ("Puzzles, memory games and real art for ages 4–8. Just a pencil — no screen, no charger.",
        "Énigmes, jeux de mémoire et vraies œuvres d’art pour les 4–8 ans. Juste un crayon : ni écran, ni chargeur.",
        "Puzzels, geheugenspelletjes en echte kunst voor kinderen van 4–8 jaar. Alleen een potlood: geen scherm, geen oplader."),
 "p1": ("Look inside ↓", "Regardez dedans ↓", "Kijk binnen ↓"),
 # 2
 "k2": ("What the WHO recommends", "Ce que recommande l’OMS", "Wat de WHO aanraadt"),
 "big2": ("1 h", "1 h", "1 u"),
 "h2": ("or less of screen time a day for children aged 2 to 4.<br>{Less is better.}",
        "d’écran par jour au maximum pour les enfants de 2 à 4 ans.<br>{Moins, c’est mieux.}",
        "of minder schermtijd per dag voor kinderen van 2 tot 4 jaar.<br>{Minder is beter.}"),
 "t2": ("Looking for screen-free activities that still feel like play? Start here.",
        "Envie d’activités sans écran qui restent un vrai jeu ? Commencez ici.",
        "Op zoek naar activiteiten zonder scherm die toch echt spelen zijn? Begin hier."),
 "s2": ("Source: World Health Organization, Guidelines on physical activity, sedentary behaviour and sleep for children under 5 years of age (2019).",
        "Source : Organisation mondiale de la santé, lignes directrices sur l’activité physique, la sédentarité et le sommeil chez l’enfant de moins de 5 ans (2019).",
        "Bron: Wereldgezondheidsorganisatie, richtlijnen over beweging, zittend gedrag en slaap bij kinderen jonger dan 5 jaar (2019)."),
 # 3
 "k3": ("Pediatricians say", "Ce que disent les pédiatres", "Wat kinderartsen zeggen"),
 "h3": ("For children aged 2 to 5: {no more than 1 hour} a day of high-quality screen time — ideally watched together.",
        "De 2 à 5 ans : {pas plus d’une heure} d’écran de qualité par jour, idéalement regardé ensemble.",
        "Voor kinderen van 2 tot 5 jaar: {niet meer dan 1 uur} kwaliteitsvolle schermtijd per dag, liefst samen."),
 "h3b": ("So what about the other hours?", "Et le reste de la journée ?", "En de rest van de dag?"),
 "t3": ("Short, playful pages your child can do at the table, on the sofa or in a waiting room.",
        "Des pages courtes et ludiques, à faire à table, sur le canapé ou dans une salle d’attente.",
        "Korte, speelse bladzijden voor aan tafel, in de zetel of in de wachtzaal."),
 "s3": ("Source: American Academy of Pediatrics, Media and Young Minds (2016).",
        "Source : American Academy of Pediatrics, Media and Young Minds (2016).",
        "Bron: American Academy of Pediatrics, Media and Young Minds (2016)."),
 # 4
 "k4": ("Did you know?", "Le saviez-vous ?", "Wist je dat?"),
 "big4": ("2h 24", "2 h 24", "2 u 24"),
 "h4": ("is the average daily screen time of US children aged 0 to 8.",
        "c’est le temps d’écran moyen par jour des enfants de 0 à 8 ans aux États-Unis.",
        "is de gemiddelde schermtijd per dag van Amerikaanse kinderen van 0 tot 8 jaar."),
 "h4b": ("What could {15} of those minutes become?", "Et si {15} de ces minutes devenaient autre chose ?", "Wat als {15} van die minuten iets anders worden?"),
 "s4": ("Source: Common Sense Media, The Common Sense Census: Media Use by Kids Age Zero to Eight (2020).",
        "Source : Common Sense Media, The Common Sense Census: Media Use by Kids Age Zero to Eight (2020).",
        "Bron: Common Sense Media, The Common Sense Census: Media Use by Kids Age Zero to Eight (2020)."),
 # 5
 "h5": ("“I’m bored!”", "« Je m’ennuie ! »", "‘Ik verveel me!’"),
 "h5b": ("is often where thinking starts.", "c’est souvent là que la réflexion commence.", "is vaak waar het denken begint."),
 "t5": ("Instead of handing over the phone, hand over a pencil and a puzzle. Small challenges, big “I did it!” moments.",
        "Au lieu de tendre le téléphone, tendez un crayon et une énigme. De petits défis, de grands « J’ai réussi ! ».",
        "Geef in plaats van de telefoon een potlood en een puzzel. Kleine uitdagingen, grote ‘Het is gelukt!’-momenten."),
 # 6
 "k6": ("Volume 1 · ages 4–6", "Volume 1 · 4–6 ans", "Deel 1 · 4–6 jaar"),
 "h6": ("9 islands of thinking games", "9 îles de jeux pour réfléchir", "9 eilanden vol denkspelletjes"),
 "isl": (["Look Closely", "Remember", "Shapes & Colors", "Patterns", "Logic", "Numbers", "Words", "Space", "Feelings"],
         ["Bien regarder", "Mémoire", "Formes et couleurs", "Suites", "Logique", "Nombres", "Mots", "Espace", "Émotions"],
         ["Goed kijken", "Onthouden", "Vormen en kleuren", "Reeksen", "Logica", "Getallen", "Woorden", "Ruimte", "Gevoelens"]),
 "t6": ("+ a Big Challenge, a star chart, answers for grown-ups and a certificate.",
        "+ un Grand défi, un tableau d’étoiles, les réponses pour les adultes et un diplôme.",
        "+ een Grote uitdaging, een sterrenkaart, antwoorden voor volwassenen en een diploma."),
 "p6": ("96 pages · no screen needed", "96 pages · sans écran", "96 bladzijden · zonder scherm"),
 # 7
 "k7": ("Volume 2 · ages 6–8", "Volume 2 · 6–8 ans", "Deel 2 · 6–8 jaar"),
 "h7": ("12 missions for curious minds aged 6 to 8", "12 missions pour les esprits curieux de 6 à 8 ans", "12 opdrachten voor nieuwsgierige kinderen van 6 tot 8"),
 "t7": ("Secret codes, picture sudoku, treasure maps, story problems, planning puzzles — and a final mission to open the chest.",
        "Codes secrets, sudoku en images, cartes au trésor, petits problèmes, énigmes à planifier et une mission finale pour ouvrir le coffre.",
        "Geheime codes, prentjessudoku, schattenkaarten, verhaaltjessommen, planpuzzels en een laatste opdracht om de kist te openen."),
 "p7": ("The next step after Volume 1", "La suite du volume 1", "Het vervolg op deel 1"),
 # 8
 "k8": ("The series", "La série", "De reeks"),
 "h8": ("Grows with your child.", "Grandit avec votre enfant.", "Groeit mee met je kind."),
 "t8": ("4–6 years: look, remember, count, feel.<br>6–8 years: codes, logic, plans and big challenges.",
        "4–6 ans : observer, retenir, compter, ressentir.<br>6–8 ans : codes, logique, plans et grands défis.",
        "4–6 jaar: kijken, onthouden, tellen, voelen.<br>6–8 jaar: codes, logica, plannen en grote uitdagingen."),
 # 9
 "k9": ("Try it with your child", "À tester avec votre enfant", "Probeer het met je kind"),
 "h9": ("Which one is different? 🤔", "Lequel est différent ? 🤔", "Welke is anders? 🤔"),
 "t9": ("Ask your 4–6 year old. Then tell us in the comments how long it took!",
        "Demandez à votre enfant de 4–6 ans. Dites-nous en commentaire combien de temps il lui a fallu !",
        "Vraag het aan je kind van 4–6 jaar. Laat in de reacties weten hoe lang het duurde!"),
 # 10
 "k10": ("Challenge · ages 6–8", "Défi · 6–8 ans", "Uitdaging · 6–8 jaar"),
 "h10": ("How many letter {b} can your child find?", "Combien de lettres {b} votre enfant trouve-t-il ?", "Hoeveel letters {b} vindt je kind?"),
 "t10": ("Watch out for d, p and q! Write the answer below 👇", "Attention aux d, p et q ! Écrivez la réponse en commentaire 👇", "Let op de d, p en q! Schrijf het antwoord hieronder 👇"),
 # 11
 "k11": ("Weekend puzzle", "Énigme du week-end", "Weekendpuzzel"),
 "h11": ("Picture sudoku for kids 6+", "Sudoku en images dès 6 ans", "Prentjessudoku vanaf 6 jaar"),
 "t11": ("Each picture once in every row, column and box. No app, no screen — just thinking.",
         "Chaque image une fois par ligne, par colonne et par carré. Ni appli ni écran : juste réfléchir.",
         "Elk prentje één keer in elke rij, kolom en vak. Geen app, geen scherm: gewoon denken."),
 # 12
 "k12": ("Not your usual activity book", "Pas un cahier d’activités comme les autres", "Geen gewoon doeboek"),
 "h12": ("Every chapter opens with a real painting by the artist who made the book.",
         "Chaque chapitre commence par une vraie peinture de l’artiste qui a créé le livre.",
         "Elk hoofdstuk begint met een echt schilderij van de kunstenaar die het boek maakte."),
 "t12": ("“How does this painting make you feel?” — there are no wrong answers.",
         "« Que ressens-tu devant cette peinture ? » Il n’y a pas de mauvaise réponse.",
         "‘Hoe voel jij je bij dit schilderij?’ Er is geen fout antwoord."),
 # 13
 "k13": ("Meet the characters", "Les personnages", "Maak kennis"),
 "h13": ("Leon tries. Leon makes mistakes. {Leon tries again.}", "Leon essaie. Leon se trompe. {Leon recommence.}", "Leon probeert. Leon vergist zich. {Leon probeert opnieuw.}"),
 "t13": ("Children learn that mistakes are part of thinking — not the end of it.",
         "Les enfants apprennent que se tromper fait partie de la réflexion, ce n’est pas la fin.",
         "Kinderen leren dat fouten maken bij denken hoort, en niet het einde is."),
 # 14
 "k14": ("Parent tip #1", "Conseil parent n° 1", "Tip voor ouders #1"),
 "h14": ("Ask,<br>don’t tell.", "Posez des<br>questions.", "Vraag,<br>vertel niet."),
 "t14": ("When your child gets stuck, try:", "Quand votre enfant bloque, essayez :", "Zit je kind vast? Probeer:"),
 "q14": ("“What do you see?”<br>“How did you find it?”<br>“Is there another way?”<br>“What would Leon do?”",
         "« Qu’est-ce que tu vois ? »<br>« Comment l’as-tu trouvé ? »<br>« Il y a une autre façon ? »<br>« Que ferait Leon ? »",
         "‘Wat zie je?’<br>‘Hoe heb je het gevonden?’<br>‘Kan het ook anders?’<br>‘Wat zou Leon doen?’"),
 "t14b": ("More tips like this throughout Leon’s Thinking Book.", "D’autres conseils comme celui-ci dans tout le livre.", "Meer tips zoals deze vind je in het hele boek."),
 # 15
 "k15": ("Parent tip #2", "Conseil parent n° 2", "Tip voor ouders #2"),
 "h15": ("Instead of “You’re so clever!” try:", "Au lieu de « Tu es trop fort ! », essayez :", "Zeg in plaats van ‘Wat ben je slim!’:"),
 "q15": (["“You looked very carefully!”", "“You didn’t give up!”", "“You found a new way!”"],
         ["« Tu as très bien regardé ! »", "« Tu n’as pas abandonné ! »", "« Tu as trouvé une autre façon ! »"],
         ["‘Je hebt heel goed gekeken!’", "‘Je gaf niet op!’", "‘Je vond een nieuwe manier!’"]),
 "t15": ("Praise the effort and children keep trying.", "Félicitez l’effort : l’enfant continue d’essayer.", "Prijs de inzet, en kinderen blijven proberen."),
 # 16
 "k16": ("Restaurant · car · waiting room", "Restaurant · voiture · salle d’attente", "Restaurant · auto · wachtzaal"),
 "h16": ("Phone-free waiting? Pack a pencil.", "Attendre sans téléphone ? Prenez un crayon.", "Wachten zonder telefoon? Neem een potlood mee."),
 "l16": ("✏️ A pencil or crayons<br>📖 One volume of Leon’s Thinking Book<br>⏱️ 10–15 minutes of focus<br>🎉 A star on the chart",
         "✏️ Un crayon ou des feutres<br>📖 Un volume de Leon’s Thinking Book<br>⏱️ 10–15 minutes de concentration<br>🎉 Une étoile sur le tableau",
         "✏️ Een potlood of kleurpotloden<br>📖 Eén deel van Leon’s Thinking Book<br>⏱️ 10–15 minuten focus<br>🎉 Een ster op de kaart"),
 # 17
 "k17": ("Feelings island", "L’île des Émotions", "Het eiland Gevoelens"),
 "h17": ("“How might Leon feel?”", "« Comment se sent Leon ? »", "‘Hoe zou Leon zich voelen?’"),
 "t17": ("Everyday situations to talk about feelings together — and there is more than one right answer.",
         "Des situations du quotidien pour parler des émotions ensemble, avec plus d’une bonne réponse.",
         "Situaties van elke dag om samen over gevoelens te praten, met meer dan één goed antwoord."),
 # 18
 "k18": ("Bilingual families 💛", "Familles bilingues 💛", "Tweetalige gezinnen 💛"),
 "h18": ("Available in English, French and Dutch.", "Disponible en anglais, en français et en néerlandais.", "Verkrijgbaar in het Engels, Frans en Nederlands."),
 "t18": ("Same games, same art, three languages. Perfect for home, school or grandma’s house.",
         "Mêmes jeux, mêmes œuvres, trois langues. Idéal à la maison, à l’école ou chez les grands-parents.",
         "Dezelfde spelletjes, dezelfde kunst, drie talen. Ideaal thuis, op school of bij oma en opa."),
 # 19
 "k19": ("After-school ritual", "Le rituel après l’école", "Na schooltijd"),
 "h19": ("The 15-minute screen-free routine", "La routine de 15 minutes sans écran", "De routine van 15 minuten zonder scherm"),
 "st19": (["Snack & sit down", "Pick one page (child chooses!)", "10–15 minutes, together", "Color a star on the chart"],
          ["Goûter et on s’installe", "Une page (l’enfant choisit !)", "10–15 minutes, ensemble", "Une étoile sur le tableau"],
          ["Vieruurtje en gaan zitten", "Eén bladzijde (je kind kiest!)", "10–15 minuten, samen", "Een ster op de kaart kleuren"]),
 # 20
 "k20": ("Now available", "Disponible maintenant", "Nu verkrijgbaar"),
 "h20": ("Learning to think, not just learning to answer.", "Apprendre à réfléchir, pas seulement à répondre.", "Leren denken, niet alleen leren antwoorden."),
 "p20": ("On Amazon · search “Leon’s Thinking Book”", "Sur Amazon · cherchez « Leon’s Thinking Book »", "Op Amazon · zoek ‘Leon’s Thinking Book’"),
}


def fr_typo(s):
    """French spacing: non-breaking space before ? ! : ; » and after «"""
    s = re.sub(r" ([?!:;»])", " \\1", s)
    return s.replace("« ", "« ")


def build(lang):
    i = LANGS.index(lang)

    def T(k, hl=CORAL):
        v = TX[k][i]
        if isinstance(v, str):
            v = re.sub(r"\{(.+?)\}", lambda m: f'<span style="color:{hl}">{m.group(1)}</span>', v)
            if lang == "FR":
                v = fr_typo(v)
        elif lang == "FR":
            v = [fr_typo(x) for x in v]
        return v

    def book(v, x, y, w, rot=0, z=1):
        h = w * 2200 / 1701
        return (f'<div class="book" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;transform:rotate({rot}deg);z-index:{z}">'
                f'<img src="{A}/cover_v{v}_{lang}.png"></div>')

    def page(name, x, y, w, rot=0, crop=None, h=None, z=1):
        name = f"{name}_{lang}"
        style = f"left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z}"
        inner = f'<img src="{A}/{name}.png">'
        if crop is not None:
            full = w * 1340 / 1024
            style += f";height:{h}px"
            inner = f'<img src="{A}/{name}.png" style="margin-top:-{crop * full:.0f}px">'
        return f'<div class="pg" style="{style}">{inner}</div>'

    def post(bg, body, col=NAVY):
        foot = (f'<div class="foot" style="color:{col}"><span>{T("foot")}</span>'
                f'<span style="display:flex;align-items:center;gap:12px"><img src="{ART}/leon.svg" style="width:58px;height:62px">'
                f'<span>{T("by")}</span></span></div>')
        return f'<div class="p" style="background:{bg}">{body}{foot}</div>'

    P = []
    P.append(post(CREAM, f"""
<div class="blob" style="left:620px;top:-160px;width:620px;height:620px;background:{GOLD};opacity:.35"></div>
<div class="a k" style="left:70px;top:90px;color:{CORAL}">{T('k1')}</div>
<div class="a h" style="left:70px;top:140px;width:950px">{T('h1')}</div>
<div class="a t" style="left:70px;top:620px;width:440px">{T('t1')}</div>
{book(1, 560, 560, 420, 6)}
<div class="a pill" style="left:70px;top:1000px;background:{NAVY};color:#fff">{T('p1')}</div>"""))

    P.append(post(TEAL, f"""
<div class="a k" style="left:70px;top:90px;color:#fff">{T('k2')}</div>
<div class="a" style="left:60px;top:150px;font:800 330px/0.9 'Baloo 2';color:#fff">{T('big2')}</div>
<div class="a h2" style="left:70px;top:470px;width:920px;color:#fff">{T('h2', GOLD)}</div>
<div class="a t" style="left:70px;top:790px;width:520px;color:#fff">{T('t2')}</div>
{book(1, 620, 780, 360, -5)}
<div class="a src" style="left:70px;top:1100px;width:520px;color:#fff">{T('s2')}</div>""", "#fff"))

    P.append(post("#FFF1E6", f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">{T('k3')}</div>
<div class="a h2" style="left:70px;top:150px;width:930px">{T('h3')}</div>
<div class="a" style="left:70px;top:520px;width:940px;height:3px;background:{NAVY};opacity:.15"></div>
<div class="a h2" style="left:70px;top:560px;width:540px;font-size:52px">{T('h3b')}</div>
<div class="a t" style="left:70px;top:720px;width:500px">{T('t3')}</div>
{book(1, 600, 640, 400, 4)}
<div class="a src" style="left:70px;top:1130px;width:500px">{T('s3')}</div>"""))

    P.append(post(NAVY, f"""
<div class="a k" style="left:70px;top:90px;color:{GOLD}">{T('k4')}</div>
<div class="a" style="left:60px;top:140px;font:800 250px/0.9 'Baloo 2';color:{GOLD}">{T('big4')}</div>
<div class="a h2" style="left:70px;top:390px;width:930px;color:#fff">{T('h4')}</div>
<div class="a h2" style="left:70px;top:620px;width:540px;font-size:50px;color:#fff">{T('h4b', GOLD)}</div>
{page('v1_p13', 640, 610, 360, 5)}
<div class="a src" style="left:70px;top:1110px;width:520px;color:#fff">{T('s4')}</div>""", "#fff"))

    P.append(post(CREAM, f"""
<div class="blob" style="left:-200px;top:820px;width:620px;height:620px;background:{TEAL};opacity:.18"></div>
<div class="a h" style="left:70px;top:110px;width:950px">{T('h5')}</div>
<div class="a h2" style="left:70px;top:230px;width:940px;color:{CORAL}">{T('h5b')}</div>
<div class="a t" style="left:70px;top:380px;width:900px">{T('t5')}</div>
{page('v1_p11', 110, 580, 400, -5)}
{page('v2_p11', 560, 620, 400, 4)}"""))

    cols = ["#DF533C", "#2E9EA0", "#F6C83D", "#ED8A33", "#9ACB45", "#9CC4F0", "#F6C6D0", "#C8B8F0", "#F9DD83"]
    chips = "".join(f'<div style="display:flex;align-items:center;gap:14px;margin:4px 0;font:700 30px Andika"><span style="width:26px;height:26px;border-radius:50%;background:{c}"></span>{n}</div>'
                    for n, c in zip(T("isl"), cols))
    P.append(post("#fff", f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">{T('k6')}</div>
<div class="a h2" style="left:70px;top:140px;width:520px">{T('h6')}</div>
<div class="a" style="left:70px;top:330px">{chips}</div>
<div class="a t" style="left:70px;top:870px;width:470px;font-size:30px">{T('t6')}</div>
{book(1, 590, 300, 420, 3)}
<div class="a pill" style="left:70px;top:1100px;background:{CORAL};color:#fff">{T('p6')}</div>"""))

    P.append(post("#EEF4FF", f"""
<div class="a k" style="left:70px;top:90px;color:{BLUE}">{T('k7')}</div>
<div class="a h2" style="left:70px;top:140px;width:940px;font-size:54px">{T('h7')}</div>
<div class="a t" style="left:70px;top:340px;width:470px;font-size:32px">{T('t7')}</div>
{book(2, 590, 340, 420, -3)}
{page('v2_p35', 90, 640, 380, -4)}
<div class="a pill" style="left:560px;top:1000px;background:{BLUE};color:#fff">{T('p7')}</div>"""))

    P.append(post(GOLD, f"""
<div class="a k" style="left:70px;top:90px">{T('k8')}</div>
<div class="a h" style="left:70px;top:140px;width:950px;font-size:84px">{T('h8')}</div>
{book(1, 110, 400, 400, -6, 2)}
{book(2, 560, 420, 400, 5, 1)}
<div class="a t" style="left:70px;top:1000px;width:940px;text-align:center">{T('t8')}</div>"""))

    P.append(post("#fff", f"""
<div class="a k" style="left:70px;top:90px;color:{TEAL}">{T('k9')}</div>
<div class="a h2" style="left:70px;top:140px;width:940px">{T('h9')}</div>
<div class="a t" style="left:70px;top:240px;width:940px">{T('t9')}</div>
{page('v1_p13', 190, 380, 700, 0, 0.17, 700)}"""))

    P.append(post(CREAM, f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">{T('k10')}</div>
<div class="a h2" style="left:70px;top:140px;width:940px">{T('h10')}</div>
<div class="a t" style="left:70px;top:310px;width:940px">{T('t10')}</div>
{page('v2_p11', 190, 420, 700, 0, 0.165, 680)}"""))

    P.append(post("#EAF7F5", f"""
<div class="a k" style="left:70px;top:90px;color:{TEAL}">{T('k11')}</div>
<div class="a h2" style="left:70px;top:140px;width:940px">{T('h11')}</div>
<div class="a t" style="left:70px;top:240px;width:940px">{T('t11')}</div>
{page('v2_p35', 190, 400, 700, 0, 0.165, 720)}"""))

    P.append(post("#1E2A5A", f"""
<img class="a" src="{ART}/open_12.jpg" style="left:0;top:0;width:1080px;height:740px;object-fit:cover">
<div class="a" style="left:0;top:0;width:1080px;height:740px;background:linear-gradient(180deg,rgba(30,42,90,0) 50%,rgba(30,42,90,1) 100%)"></div>
<div class="a k" style="left:70px;top:780px;color:{GOLD}">{T('k12')}</div>
<div class="a h2" style="left:70px;top:830px;width:940px;color:#fff;font-size:58px">{T('h12')}</div>
<div class="a t" style="left:70px;top:1090px;width:940px;color:#fff;font-size:30px">{T('t12')}</div>""", "#fff"))

    P.append(post(CREAM, f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">{T('k13')}</div>
<div class="a h2" style="left:70px;top:140px;width:940px">{T('h13')}</div>
<img class="a" src="{ART}/leon_luz.svg" style="left:230px;top:400px;width:620px;height:670px">
<div class="a t" style="left:70px;top:1090px;width:940px;text-align:center;font-size:32px">{T('t13')}</div>"""))

    P.append(post("#FFF1E6", f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">{T('k14')}</div>
<div class="a h" style="left:70px;top:150px;width:940px">{T('h14')}</div>
<div class="a t" style="left:70px;top:420px;width:620px">{T('t14')}</div>
<div class="a" style="left:70px;top:500px;width:660px;font:700 38px/1.45 Andika">{T('q14')}</div>
<img class="a" src="{ART}/leon.svg" style="left:720px;top:520px;width:310px;height:340px">
<div class="a t" style="left:70px;top:980px;width:940px;font-size:30px">{T('t14b')}</div>"""))

    P.append(post(TEAL, f"""
<div class="a k" style="left:70px;top:90px;color:#fff">{T('k15')}</div>
<div class="a h2" style="left:70px;top:150px;width:940px;color:#fff">{T('h15')}</div>
<div class="a" style="left:70px;top:400px;width:940px">
 {''.join(f'<div style="background:#fff;border-radius:24px;padding:26px 34px;margin:0 0 22px;font:700 40px Andika;color:{NAVY}">{t}</div>' for t in T('q15'))}
</div>
<div class="a t" style="left:70px;top:1030px;width:940px;color:#fff;font-size:32px">{T('t15')}</div>""", "#fff"))

    P.append(post(CREAM, f"""
<div class="a k" style="left:70px;top:90px;color:{TEAL}">{T('k16')}</div>
<div class="a h2" style="left:70px;top:140px;width:940px">{T('h16')}</div>
<div class="a" style="left:70px;top:360px;font:700 36px/1.7 Andika">{T('l16')}</div>
{book(1, 600, 640, 340, 8)}
{page('v1_p11', 110, 660, 340, -6)}"""))

    P.append(post("#FFF8DC", f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">{T('k17')}</div>
<div class="a h2" style="left:70px;top:140px;width:940px">{T('h17')}</div>
<div class="a t" style="left:70px;top:250px;width:940px">{T('t17')}</div>
{page('v1_p79', 190, 440, 700, 0, 0.165, 650)}"""))

    P.append(post("#fff", f"""
<div class="a k" style="left:70px;top:90px;color:{BLUE}">{T('k18')}</div>
<div class="a h2" style="left:70px;top:140px;width:940px">{T('h18')}</div>
<div class="a" style="left:70px;top:360px;display:flex;gap:26px">
 {''.join(f'<span class="pill" style="font-size:40px;padding:22px 44px;background:{c};color:#fff">{l}</span>' for l, c in [('EN', CORAL), ('FR', BLUE), ('NL', TEAL)])}</div>
<div class="a t" style="left:70px;top:520px;width:450px">{T('t18')}</div>
{book(1, 560, 500, 400, 4)}"""))

    steps = list(zip("1234", T("st19"), [CORAL, TEAL, BLUE, GOLD]))
    st = "".join(f'<div style="display:flex;align-items:center;gap:26px;margin:0 0 30px"><span style="width:84px;height:84px;flex:none;border-radius:50%;background:{c};color:#fff;font:800 48px Baloo\\ 2;display:flex;align-items:center;justify-content:center">{n}</span><span style="font:700 40px Andika">{t}</span></div>' for n, t, c in steps)
    P.append(post(CREAM, f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">{T('k19')}</div>
<div class="a h2" style="left:70px;top:140px;width:940px">{T('h19')}</div>
<div class="a" style="left:70px;top:360px;width:940px">{st}</div>
{page('v1_p6', 380, 830, 320, 3)}"""))

    P.append(post(CORAL, f"""
<div class="a k" style="left:70px;top:90px;color:#fff">{T('k20')}</div>
<div class="a h" style="left:70px;top:140px;width:950px;color:#fff;font-size:80px">{T('h20')}</div>
{book(1, 120, 520, 380, -5, 2)}
{book(2, 560, 540, 380, 5, 1)}
<div class="a pill" style="left:50%;transform:translateX(-50%);top:1080px;background:#fff;color:{CORAL};font-size:30px;padding:20px 44px;white-space:nowrap">{T('p20')}</div>""", "#fff"))
    return P


if __name__ == "__main__":
    for lang in LANGS:
        os.makedirs(f"{R}/html_i18n/{lang}", exist_ok=True)
        for n, body in enumerate(build(lang), 1):
            open(f"{R}/html_i18n/{lang}/post{n:02d}.html", "w").write(
                f'<!doctype html><html lang="{lang.lower()}"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
    print("ok")
