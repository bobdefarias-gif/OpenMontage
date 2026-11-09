"""Revised edition V2 (ages 6–8) — 96 pages. Content spec (EN). 12 missions (kept from the original book)."""
import json, os

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# key: (name, small label, colour, text colour)
ISLANDS = {
    "m1": ("Selective Attention", "Mission 1", "#DF533C", "#FFFFFF"),
    "m2": ("Working Memory", "Mission 2", "#2E9EA0", "#FFFFFF"),
    "m3": ("Visual Memory", "Mission 3", "#3B82C4", "#FFFFFF"),
    "m4": ("Logic", "Mission 4", "#9ACB45", "#1E2A5A"),
    "m5": ("Patterns", "Mission 5", "#ED8A33", "#FFFFFF"),
    "m6": ("Mathematics", "Mission 6", "#9CC4F0", "#1E2A5A"),
    "m7": ("Language", "Mission 7", "#F6C6D0", "#1E2A5A"),
    "m8": ("Spatial Reasoning", "Mission 8", "#C8B8F0", "#1E2A5A"),
    "m9": ("Problem Solving", "Mission 9", "#F6C83D", "#1E2A5A"),
    "m10": ("Planning", "Mission 10", "#7FC8A9", "#1E2A5A"),
    "m11": ("Feelings", "Mission 11", "#F9DD83", "#1E2A5A"),
    "m12": ("Final Big Challenge", "Mission 12", "#1E2A5A", "#FFFFFF"),
}

# mission: (opener page, first orig page, last orig page)
MISSIONS = [("m1", 10, 8, 13), ("m2", 17, 14, 19), ("m3", 25, 20, 25), ("m4", 32, 26, 32), ("m5", 40, 33, 37),
            ("m6", 46, 38, 45), ("m7", 55, 46, 52), ("m8", 63, 53, 58), ("m9", 70, 59, 63), ("m10", 76, 64, 68),
            ("m11", 82, 69, 72), ("m12", 87, 73, 75)]
NEW_PAGE = 24          # new Working-Memory activity (keeps look/turn pages on odd pages)

ORIG = json.load(open(f"{R}/build/v2_orig_strings.json"))
LEVEL = {8: 2, 9: 2, 10: 2, 11: 3, 12: 3, 13: 2, 14: 2, 15: 2, 16: 3, 17: 2, 18: 3, 19: 3, 20: 2, 21: 2, 22: 3, 23: 3, 24: 3,
         25: 2, 26: 2, 27: 2, 28: 2, 29: 3, 30: 2, 31: 3, 32: 3, 33: 2, 34: 3, 35: 3, 36: 3, 37: 2, 38: 2, 39: 2, 40: 2, 41: 3,
         42: 2, 43: 2, 44: 2, 45: 3, 46: 2, 47: 2, 48: 3, 49: 3, 50: 2, 51: 2, 52: 3, 53: 2, 54: 3, 55: 3, 56: 3, 57: 2, 58: 3,
         59: 2, 60: 3, 61: 3, 62: 2, 63: 2, 64: 3, 65: 2, 66: 3, 67: 3, 68: 2, 69: 2, 70: 2, 71: 3, 72: 2, 73: 3, 74: 3, 75: 3}

BOX = {   # orig page -> (kind, text)
    8: ("Parent's Little Tip", "Slide a ruler or a strip of paper down the page so your child checks one row at a time."),
    9: ("Ask Leon", "Which difference was the hardest to find?"),
    10: ("Try Another Way", "Now try it again and count out loud as you go!"),
    11: ("Parent's Little Tip", "Ask your child to tick each blue triangle as they count it."),
    12: ("Ask Leon", "Can you say what is different in each row?"),
    13: ("Try Another Way", "Can you find a word that is not an animal?"),
    15: ("Ask Leon", "Can you say the list back in the same order?"),
    17: ("Parent's Little Tip", "Give your child time to learn the code. Saying it aloud helps: “star is 2…”"),
    18: ("Try Another Way", "Make up a new sum with the code for your grown-up!"),
    20: ("Parent's Little Tip", "Let your child look as long as they like, then cover the top grid fully."),
    22: ("Ask Leon", "What else do you remember from the beach?"),
    25: ("Talk About It", "Which part of the robot was easiest to remember? Why?"),
    26: ("Parent's Little Tip", "Read each clue with your child and put a ✗ first. Ticks come at the end."),
    27: ("Ask Leon", "Which clue helped you the most?"),
    28: ("Parent's Little Tip", "Start with the row that has only one empty square."),
    29: ("Try Another Way", "Make your own picture pair for your grown-up!"),
    30: ("Try Another Way", "Write one more true sentence about the picture."),
    31: ("Parent's Little Tip", "Look for a row, column or box with three numbers already there."),
    32: ("Ask Leon", "Can you think of another animal that can fly and swim?"),
    33: ("Talk About It", "How did you find each rule?"),
    34: ("Try Another Way", "How many squares will step 5 have?"),
    35: ("Parent's Little Tip", "Let your child turn the book to follow the arrow."),
    37: ("Ask Leon", "Can your grown-up make a pattern for you to guess?"),
    38: ("Parent's Little Tip", "Fingers and counting on are good strategies. Speed doesn’t matter."),
    39: ("Try Another Way", "Check one answer by adding it back!"),
    40: ("Ask Leon", "Can you find two numbers that make 10 in your home?"),
    41: ("Parent's Little Tip", "Drawing the marbles, birds or apples is a great way to think."),
    42: ("Try Another Way", "Draw tens and ones for the number of your age plus 20."),
    43: ("Talk About It", "What time do you have lunch? Where are the hands then?"),
    44: ("Try Another Way", "Measure something at home with real paper clips!"),
    46: ("Ask Leon", "Can you make a silly rhyme with the words?"),
    47: ("Try Another Way", "Make a new word by changing one letter: cat → hat."),
    49: ("Parent's Little Tip", "The capital letter shows which word comes first."),
    50: ("Talk About It", "Read your drawings back to your grown-up."),
    51: ("Ask Leon", "What is the opposite of “fast”?"),
    52: ("Try Another Way", "Tell the story in a different order. Does it still work?"),
    53: ("Parent's Little Tip", "Count the squares together: “two across, one down…”."),
    54: ("Try Another Way", "Hide a treasure on the map and give a grown-up the code!"),
    56: ("Ask Leon", "Can you make the square another way?"),
    57: ("Parent's Little Tip", "Fold a piece of paper on the red line to check."),
    58: ("Try Another Way", "Build a tower with real blocks and count them!"),
    59: ("Talk About It", "Is the shortest way always the best way?"),
    60: ("Ask Leon", "What if the boat could carry 13 kg?"),
    61: ("Parent's Little Tip", "Go one scale at a time: first pumpkins and apples, then apples and cherries."),
    62: ("Try Another Way", "Share 12 cookies with 4 friends. How many each?"),
    63: ("Try Another Way", "Draw one more silly thing in the picture!"),
    64: ("Parent's Little Tip", "Plan with a finger first, then draw."),
    65: ("Ask Leon", "What would Leon pack for a sunny day?"),
    66: ("Talk About It", "Can you sort them a third way?"),
    68: ("Talk About It", "Is there another good order? Families do things differently."),
    69: ("Talk About It", "The same thing can feel big for one person and small for another."),
    70: ("Talk About It", "Is there another good idea for each story?"),
    71: ("Parent's Little Tip", "There is no wrong answer. Help your child see both points of view."),
    72: ("Talk About It", "Which idea will you try next time you feel upset?"),
    73: ("Parent's Little Tip", "Keep the secret letters on a piece of paper until page 90."),
}

ACT = []   # (new page, orig page, mission, level, title, instruction, box)
for key, op, a, b in MISSIONS:
    n = op + 1
    for o in range(a, b + 1):
        e = ORIG[str(o)]["EN"]
        ACT.append((n, o, key, LEVEL[o], e["title"], e["ins"].replace("page 75!", "page 90!"), BOX.get(o)))
        n += 1
        if key == "m2" and o == b:
            n += 1   # NEW_PAGE
ORIG_TO_NEW = {a[1]: a[0] for a in ACT}

# Openers: page, mission, painting, character, bubble, art-detective question, adult line
OPENERS = [
    (10, "m1", "14", "leon", "Sharp eyes on! Let’s find the tiny things.", "Find 3 little circles in Robert’s face drawing.", "your child practises finding exactly what they are looking for."),
    (17, "m2", "01", "luz", "Keep it in your head — like a secret!", "Look for 5 seconds. Close your eyes. Is the painting red, blue or green?", "your child practises keeping information in mind and using it."),
    (25, "m3", "03", "leon", "Take a photo with your eyes!", "Find the eye of the bird hiding in Robert’s painting.", "your child practises remembering what they see."),
    (32, "m4", "09", "luz", "Clue by clue, we can work it out!", "Which shape is the biggest? How do you know?", "your child uses clues and reasons step by step."),
    (40, "m5", "06", "leon", "What is the rule? Let’s crack it!", "Find a place where the lines change direction.", "your child finds rules and makes new patterns."),
    (46, "m6", "02", "luz", "Numbers are everywhere — even in paintings!", "Guess: are there more than 20 brush strokes or fewer? Count one corner to check.", "your child adds, subtracts, measures and tells the time."),
    (55, "m7", "08", "leon", "Robert writes with shapes. We write with letters!", "Make up a name for one of Robert’s “letters”.", "your child builds words and sentences."),
    (63, "m8", "15", "luz", "Turn it, flip it, map it!", "Put your finger on a blue line. Can you get from one side to the other?", "your child turns, flips and maps shapes in space."),
    (70, "m9", "05", "leon", "Every problem has a way in. Let’s find it!", "This creature has big eyes. How many can you count?", "your child tries different ways to solve a problem."),
    (76, "m10", "10", "luz", "First this, then that — let’s make a plan!", "Find a path from the top of the painting to the bottom.", "your child plans steps and changes the plan when needed."),
    (82, "m11", "11", "leon", "Every feeling is OK. What we do with it matters.", "How might this face feel? What makes you think so?", "your child names feelings and finds kind ways to act."),
    (87, "m12", "12", "both", "Last mission! Use everything you learned.", "Find all the colors of the rainbow in Robert’s painting.", "your child combines all the skills in a final mission."),
]
OPENER_TITLES = {k: v[0] for k, v in ISLANDS.items()}
