"""Ready-to-paste Facebook captions, one file per language: facebook/LEGENDAS-FACEBOOK-<LANG>.md"""
import os
R = os.path.dirname(os.path.abspath(__file__))

LINKS = {
    "EN": "https://www.amazon.com/s?k=Leon%27s+Thinking+Book+Robert+de+Farias",
    "EN2": "https://www.amazon.co.uk/s?k=Leon%27s+Thinking+Book+Robert+de+Farias",
    "FR": "https://www.amazon.fr/s?k=Leon%27s+Thinking+Book+Robert+de+Farias",
    "NL": "https://www.amazon.nl/s?k=Leon%27s+Thinking+Book+Robert+de+Farias",
    "BE": "https://www.amazon.com.be/s?k=Leon%27s+Thinking+Book+Robert+de+Farias",
}
LINK = {
    "EN": f"🇺🇸 {LINKS['EN']}\n🇬🇧 {LINKS['EN2']}",
    "FR": f"🇫🇷 {LINKS['FR']}\n🇧🇪 {LINKS['BE']}",
    "NL": f"🇳🇱 {LINKS['NL']}\n🇧🇪 {LINKS['BE']}",
}
BOOK = {"v1": ("Volume 1 (ages 4–6)", "Volume 1 (4–6 ans)", "Deel 1 (4–6 jaar)"),
        "v2": ("Volume 2 (ages 6–8)", "Volume 2 (6–8 ans)", "Deel 2 (6–8 jaar)"),
        "s": ("Both volumes", "Les deux volumes", "Beide delen")}
BOOK_PT = {"v1": "Volume 1", "v2": "Volume 2", "s": "Série (os dois)"}
TYPE_PT = {"val": "valor (bom para grupos)", "game": "jogo/interação (ótimo para grupos)", "prod": "produto (com link)"}

# (book, type, link?, EN, FR, NL)
C = [
 ("s", "prod", True,
  "Swap 15 minutes of scrolling for 15 minutes of thinking ✏️\n\nLeon’s Thinking Book is full of short puzzles, memory games and real art for kids aged 4–8. All you need is a pencil — no screen, no charger, no app.",
  "15 minutes d’écran en moins, 15 minutes de réflexion en plus ✏️\n\nLeon’s Thinking Book, ce sont des énigmes courtes, des jeux de mémoire et de vraies œuvres d’art pour les 4–8 ans. Il suffit d’un crayon : ni écran, ni chargeur, ni appli.",
  "Ruil 15 minuten scrollen voor 15 minuten denken ✏️\n\nLeon’s Thinking Book zit vol korte puzzels, geheugenspelletjes en echte kunst voor kinderen van 4–8 jaar. Je hebt alleen een potlood nodig: geen scherm, geen oplader, geen app."),
 ("v1", "val", False,
  "The World Health Organization recommends no more than 1 hour of screen time a day for children aged 2 to 4 — and says less is better.\n\nWhat are your favourite screen-free activities at home? Share them below 👇 We’ll start: a pencil and a puzzle book 💛\n\n(Source: WHO, 2019)",
  "L’Organisation mondiale de la santé recommande au maximum 1 heure d’écran par jour pour les enfants de 2 à 4 ans, et précise que moins, c’est mieux.\n\nQuelles sont vos activités sans écran préférées à la maison ? Partagez-les en commentaire 👇 On commence : un crayon et un cahier d’énigmes 💛\n\n(Source : OMS, 2019)",
  "De Wereldgezondheidsorganisatie raadt maximaal 1 uur schermtijd per dag aan voor kinderen van 2 tot 4 jaar, en minder is beter.\n\nWat zijn jullie favoriete activiteiten zonder scherm thuis? Deel ze hieronder 👇 Wij beginnen: een potlood en een puzzelboek 💛\n\n(Bron: WHO, 2019)"),
 ("v1", "val", False,
  "Pediatricians (American Academy of Pediatrics) suggest no more than 1 hour a day of high-quality screen time for children aged 2–5, ideally watched together.\n\nSo what about the rest of the day? Short, playful pages at the table, on the sofa or in the waiting room work wonders here.",
  "Les pédiatres américains (American Academy of Pediatrics) conseillent au maximum 1 heure d’écran de qualité par jour entre 2 et 5 ans, idéalement regardé ensemble.\n\nEt le reste de la journée ? Chez nous, des pages courtes et ludiques à table, sur le canapé ou en salle d’attente font des merveilles.",
  "Amerikaanse kinderartsen (American Academy of Pediatrics) raden voor kinderen van 2 tot 5 jaar maximaal 1 uur kwaliteitsvolle schermtijd per dag aan, liefst samen.\n\nEn de rest van de dag? Korte, speelse bladzijden aan tafel, in de zetel of in de wachtzaal doen hier wonderen."),
 ("v1", "val", False,
  "In the US, children aged 0–8 spend on average 2 hours and 24 minutes a day with screens (Common Sense Media, 2020).\n\nWhat could 15 of those minutes become? A puzzle, a story, a proud “Look, I did it!” 🙌",
  "Aux États-Unis, les enfants de 0 à 8 ans passent en moyenne 2 h 24 par jour devant les écrans (Common Sense Media, 2020).\n\nEt si 15 de ces minutes devenaient une énigme, une histoire, un grand « Regarde, j’ai réussi ! » 🙌",
  "In de VS zitten kinderen van 0 tot 8 jaar gemiddeld 2 uur en 24 minuten per dag achter een scherm (Common Sense Media, 2020).\n\nWat als 15 van die minuten een puzzel worden, een verhaaltje, een trots ‘Kijk, het is gelukt!’ 🙌"),
 ("s", "val", False,
  "“I’m bored!” is often where thinking starts 💡\n\nNext time, try handing over a pencil and a puzzle instead of the phone. Small challenges, big smiles. Does it work at your house?",
  "« Je m’ennuie ! », c’est souvent là que la réflexion commence 💡\n\nLa prochaine fois, essayez de tendre un crayon et une énigme plutôt que le téléphone. De petits défis, de grands sourires. Ça marche chez vous ?",
  "‘Ik verveel me!’ is vaak waar het denken begint 💡\n\nProbeer de volgende keer een potlood en een puzzel te geven in plaats van de telefoon. Kleine uitdagingen, grote glimlachen. Werkt het bij jullie?"),
 ("v1", "prod", True,
  "Volume 1 (ages 4–6): 9 islands of thinking games 🏝️\nLook Closely · Remember · Shapes & Colors · Patterns · Logic · Numbers · Words · Space · Feelings\n\nPlus a Big Challenge, a star chart, answers for grown-ups and a certificate. 96 pages, no screen needed.",
  "Volume 1 (4–6 ans) : 9 îles de jeux pour réfléchir 🏝️\nBien regarder · Mémoire · Formes et couleurs · Suites · Logique · Nombres · Mots · Espace · Émotions\n\nAvec un Grand défi, un tableau d’étoiles, les réponses pour les adultes et un diplôme. 96 pages, sans écran.",
  "Deel 1 (4–6 jaar): 9 eilanden vol denkspelletjes 🏝️\nGoed kijken · Onthouden · Vormen en kleuren · Reeksen · Logica · Getallen · Woorden · Ruimte · Gevoelens\n\nMet een Grote uitdaging, een sterrenkaart, antwoorden voor volwassenen en een diploma. 96 bladzijden, zonder scherm."),
 ("v2", "prod", True,
  "Volume 2 (ages 6–8): 12 missions for curious minds 🗝️\nSecret codes, picture sudoku, treasure maps, story problems, planning puzzles — and a final mission to open the treasure chest!",
  "Volume 2 (6–8 ans) : 12 missions pour les esprits curieux 🗝️\nCodes secrets, sudoku en images, cartes au trésor, petits problèmes, énigmes à planifier… et une mission finale pour ouvrir le coffre au trésor !",
  "Deel 2 (6–8 jaar): 12 opdrachten voor nieuwsgierige kinderen 🗝️\nGeheime codes, prentjessudoku, schattenkaarten, verhaaltjessommen, planpuzzels… en een laatste opdracht om de schatkist te openen!"),
 ("s", "prod", True,
  "A series that grows with your child 📚\nVolume 1 for ages 4–6, Volume 2 for ages 6–8. Same characters, same art, more challenge.",
  "Une série qui grandit avec votre enfant 📚\nVolume 1 pour les 4–6 ans, volume 2 pour les 6–8 ans. Mêmes personnages, mêmes œuvres, plus de défis.",
  "Een reeks die meegroeit met je kind 📚\nDeel 1 voor 4–6 jaar, deel 2 voor 6–8 jaar. Dezelfde figuren, dezelfde kunst, meer uitdaging."),
 ("v1", "game", False,
  "Quick game for your 4–6 year old 🧩\nIn each row, which one is different?\n\nTell us in the comments how long it took — and which row was the trickiest! 👇",
  "Petit jeu pour votre enfant de 4–6 ans 🧩\nSur chaque ligne, lequel est différent ?\n\nDites-nous en commentaire combien de temps il lui a fallu, et quelle ligne était la plus difficile ! 👇",
  "Snel spelletje voor je kind van 4–6 jaar 🧩\nWelke is anders in elke rij?\n\nLaat in de reacties weten hoe lang het duurde, en welke rij het moeilijkst was! 👇"),
 ("v2", "game", False,
  "Challenge for ages 6–8 👀\nHow many letter b can your child find? Watch out for d, p and q!\n\nWrite your child’s answer below 👇 We’ll post the solution tomorrow.\n\n(Next day, reply in the comments: the answer is 12 ✅)",
  "Défi pour les 6–8 ans 👀\nCombien de lettres b votre enfant trouve-t-il ? Attention aux d, p et q !\n\nÉcrivez sa réponse en commentaire 👇 On donne la solution demain.\n\n(Le lendemain, répondez en commentaire : la réponse est 12 ✅)",
  "Uitdaging voor 6–8 jaar 👀\nHoeveel letters b vindt je kind? Let op de d, p en q!\n\nSchrijf het antwoord van je kind hieronder 👇 Morgen geven we de oplossing.\n\n(De volgende dag antwoorden in de reacties: het antwoord is 12 ✅)"),
 ("v2", "game", False,
  "Weekend puzzle: picture sudoku for kids 6+ 🧠\nEach picture once in every row, column and box. No app, no screen — just thinking.\n\nSave this post for Saturday morning! 📌",
  "Énigme du week-end : sudoku en images dès 6 ans 🧩\nChaque image une fois par ligne, par colonne et par carré. Ni appli ni écran : juste réfléchir.\n\nEnregistrez ce post pour samedi matin ! 📌",
  "Weekendpuzzel: prentjessudoku vanaf 6 jaar 🧩\nElk prentje één keer in elke rij, kolom en vak. Geen app, geen scherm: gewoon denken.\n\nBewaar dit bericht voor zaterdagochtend! 📌"),
 ("s", "val", False,
  "Not your usual activity book 🎨\nEvery chapter opens with a real painting by Robert de Farias, the artist and author.\n\nAsk your child: “How does this painting make you feel?” There are no wrong answers.",
  "Pas un cahier d’activités comme les autres 🎨\nChaque chapitre commence par une vraie peinture de Robert de Farias, l’artiste et auteur.\n\nDemandez à votre enfant : « Que ressens-tu devant cette peinture ? » Il n’y a pas de mauvaise réponse.",
  "Geen gewoon doeboek 🎨\nElk hoofdstuk begint met een echt schilderij van Robert de Farias, de kunstenaar en auteur.\n\nVraag je kind: ‘Hoe voel jij je bij dit schilderij?’ Er is geen fout antwoord."),
 ("s", "val", False,
  "Meet Leon 🦁 He tries. He makes mistakes. He tries again.\nAnd Luz ✨ lights up whenever someone has an idea.\n\nChildren learn that mistakes are part of thinking — not the end of it.",
  "Voici Leon 🦁 Il essaie. Il se trompe. Il recommence.\nEt Luz ✨ s’allume dès que quelqu’un a une idée.\n\nLes enfants apprennent que se tromper fait partie de la réflexion, et que ce n’est pas la fin.",
  "Maak kennis met Leon 🦁 Hij probeert. Hij vergist zich. Hij probeert opnieuw.\nEn Luz ✨ gaat stralen zodra iemand een idee heeft.\n\nKinderen leren dat fouten maken bij denken hoort, en niet het einde is."),
 ("s", "val", False,
  "Parent tip: ask, don’t tell 💬\nWhen your child gets stuck, try: “What do you see?” “How did you find it?” “Is there another way?”\n\nSave this for the next homework moment! 📌",
  "Conseil parent : posez des questions 💬\nQuand votre enfant bloque, essayez : « Qu’est-ce que tu vois ? » « Comment l’as-tu trouvé ? » « Il y a une autre façon ? »\n\nÀ enregistrer pour le prochain moment de devoirs ! 📌",
  "Tip voor ouders: vraag, vertel niet 💬\nZit je kind vast? Probeer: ‘Wat zie je?’ ‘Hoe heb je het gevonden?’ ‘Kan het ook anders?’\n\nBewaar dit voor het volgende huiswerkmoment! 📌"),
 ("s", "val", False,
  "Instead of “You’re so clever!”, try:\n✅ “You looked very carefully!”\n✅ “You didn’t give up!”\n✅ “You found a new way!”\n\nPraise the effort and children keep trying. Which one will you use today?",
  "Au lieu de « Tu es trop fort ! », essayez :\n✅ « Tu as très bien regardé ! »\n✅ « Tu n’as pas abandonné ! »\n✅ « Tu as trouvé une autre façon ! »\n\nFélicitez l’effort : l’enfant continue d’essayer. Laquelle utiliserez-vous aujourd’hui ?",
  "Zeg in plaats van ‘Wat ben je slim!’ eens:\n✅ ‘Je hebt heel goed gekeken!’\n✅ ‘Je gaf niet op!’\n✅ ‘Je vond een nieuwe manier!’\n\nPrijs de inzet, en kinderen blijven proberen. Welke gebruik jij vandaag?"),
 ("v1", "prod", True,
  "Restaurant, car, doctor’s waiting room… 🚗🍝🏥\nPack a pencil and one volume of Leon’s Thinking Book: 10–15 minutes of focus, a star on the chart, and no screen.",
  "Restaurant, voiture, salle d’attente… 🚗🍝🏥\nPrenez un crayon et un volume de Leon’s Thinking Book : 10–15 minutes de concentration, une étoile sur le tableau, et pas d’écran.",
  "Restaurant, auto, wachtzaal bij de dokter… 🚗🍝🏥\nNeem een potlood en een deel van Leon’s Thinking Book mee: 10–15 minuten focus, een ster op de kaart, en geen scherm."),
 ("v1", "val", False,
  "“How might Leon feel?” 💛\nEveryday situations to talk about feelings together — and more than one right answer. How do you talk about feelings at home?",
  "« Comment se sent Leon ? » 💛\nDes situations du quotidien pour parler des émotions ensemble, avec plus d’une bonne réponse. Comment parlez-vous des émotions à la maison ?",
  "‘Hoe zou Leon zich voelen?’ 💛\nSituaties van elke dag om samen over gevoelens te praten, met meer dan één goed antwoord. Hoe praten jullie thuis over gevoelens?"),
 ("s", "prod", True,
  "Bilingual family? 🌍 Leon’s Thinking Book is available in English, French and Dutch.\nSame games, same art, three languages — perfect for home, school or grandma’s house.",
  "Famille bilingue ? 🌍 Leon’s Thinking Book existe en anglais, en français et en néerlandais.\nMêmes jeux, mêmes œuvres, trois langues : idéal à la maison, à l’école ou chez les grands-parents.",
  "Tweetalig gezin? 🌍 Leon’s Thinking Book bestaat in het Engels, Frans en Nederlands.\nDezelfde spelletjes, dezelfde kunst, drie talen: ideaal thuis, op school of bij oma en opa."),
 ("v1", "val", False,
  "Our favourite after-school routine (15 minutes) ⏱️\n1️⃣ Snack & sit down\n2️⃣ Your child picks one page\n3️⃣ 10–15 minutes together\n4️⃣ Color a star on the chart ⭐\n\nSave it and try it this week! 📌",
  "Notre routine préférée après l’école (15 minutes) ⏱️\n1️⃣ Goûter et on s’installe\n2️⃣ L’enfant choisit une page\n3️⃣ 10–15 minutes ensemble\n4️⃣ Une étoile sur le tableau ⭐\n\nEnregistrez-la et testez-la cette semaine ! 📌",
  "Onze favoriete routine na school (15 minuten) ⏱️\n1️⃣ Vieruurtje en gaan zitten\n2️⃣ Je kind kiest een bladzijde\n3️⃣ 10–15 minuten samen\n4️⃣ Een ster op de kaart kleuren ⭐\n\nBewaar het en probeer het deze week! 📌"),
 ("s", "prod", True,
  "Leon’s Thinking Book — learning to think, not just learning to answer 💛\nVolume 1 (ages 4–6) and Volume 2 (ages 6–8) are now on Amazon, in English, French and Dutch.",
  "Leon’s Thinking Book : apprendre à réfléchir, pas seulement à répondre 💛\nLe volume 1 (4–6 ans) et le volume 2 (6–8 ans) sont disponibles sur Amazon, en français, en anglais et en néerlandais.",
  "Leon’s Thinking Book: leren denken, niet alleen leren antwoorden 💛\nDeel 1 (4–6 jaar) en deel 2 (6–8 jaar) zijn nu verkrijgbaar op Amazon, in het Nederlands, Engels en Frans."),
]
TAGS = {"EN": "#screenfree #activitybook #kidsactivities #preschool #learningthroughplay",
        "FR": "#sansécran #cahierdactivités #activitésenfants #maternelle #apprendreenjouant",
        "NL": "#zonderscherm #doeboek #kleuters #activiteitenvoorkinderen #spelenderwijsleren"}
LINE = {"EN": "👉 Find it on Amazon:", "FR": "👉 Disponible sur Amazon :", "NL": "👉 Te koop op Amazon:"}

if __name__ == "__main__":
    os.makedirs(f"{R}/facebook", exist_ok=True)
    for li, L in enumerate(("EN", "FR", "NL")):
        out = [f"# Facebook: 20 posts em {dict(EN='inglês', FR='francês', NL='holandês')[L]}\n",
               f"Imagens na pasta `facebook/{L}/` (post01.jpg … post20.jpg).",
               "**Como usar:** copie o texto entre as linhas `---` e anexe a imagem com o mesmo número.\n",
               "**Nos grupos:** use primeiro os posts de *valor* e de *jogo* (sem link). Se alguém perguntar, responda nos comentários com o link (ver o plano).\n"]
        for n, (bk, ty, lk, *tx) in enumerate(C, 1):
            text = tx[li]
            if lk:
                text += f"\n\n{LINE[L]}\n{LINK[L]}"
            text += f"\n\n{TAGS[L]}"
            out.append(f"## POST {n:02d} · imagem `post{n:02d}.jpg` · livro: {BOOK_PT[bk]} · tipo: {TYPE_PT[ty]}\n\n---\n{text}\n---\n")
        open(f"{R}/facebook/LEGENDAS-FACEBOOK-{L}.md", "w").write("\n".join(out))
    print("ok")
