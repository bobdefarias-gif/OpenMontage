"""Revised edition V1 (EN) — 96 pages. Content spec (child/adult text in English).

Page kinds:
  orig    : original activity page restyled (vector art kept, text re-set in Andika) + new header/footer/box
  full    : original full page restyled with text replacements (no new header)
  html    : new page built in HTML (may get vector stamps)
"""

ISLANDS = {
    "look": ("Look Closely", "Attention & Observation", "#DF533C", "#FFFFFF"),
    "remember": ("Remember", "Memory", "#2E9EA0", "#FFFFFF"),
    "shapes": ("Shapes & Colors", "Colors & Shapes", "#F6C83D", "#1E2A5A"),
    "patterns": ("Patterns", "Patterns", "#ED8A33", "#FFFFFF"),
    "logic": ("Logic", "Logic", "#9ACB45", "#1E2A5A"),
    "numbers": ("Numbers", "Early Math", "#9CC4F0", "#1E2A5A"),
    "words": ("Words", "Language", "#F6C6D0", "#1E2A5A"),
    "space": ("Space", "Spatial Thinking", "#C8B8F0", "#1E2A5A"),
    "feelings": ("Feelings", "Emotions & Self-Control", "#F9DD83", "#1E2A5A"),
    "big": ("Big Challenge", "Mixed skills", "#1E2A5A", "#FFFFFF"),
}

# (new page, orig page, island, level, title, instruction, box)  box = (kind, text) | None
ACT = [
    (11, 8, "look", 1, "Find the stars", "Circle all the stars.", ("Ask Leon", "How many hearts can you find?")),
    (12, 9, "look", 1, "Sock pairs", "Draw a line between the socks that are the same.", None),
    (13, 10, "look", 2, "Odd one out", "Circle the one that is different in each row.", ("Parent's Little Tip", "Ask your child to say why one is different. The reason matters more than the circle.")),
    (14, 11, "look", 2, "3 little differences", "Look at both pictures. Find 3 differences in the bottom picture and circle them.", None),
    (15, 12, "look", 1, "Hidden fish", "5 fish are hiding in the waves. Find them and color them.", ("Try Another Way", "Draw one more fish hiding in the waves!")),
    (16, 13, "look", 2, "Balloon strings", "Follow the strings. Who has the red balloon?", ("Parent's Little Tip", "Let your child follow each string with a finger before deciding.")),
    (17, 14, "look", 2, "Find the shadow", "Draw a line from each sculpture to its shadow.", ("Ask Leon", "Which sculpture would you like to make?")),
    (18, 15, "look", 2, "Ladybug spots", "Circle the ladybugs with 3 spots.", None),
    (20, 16, "remember", 1, "Luz goes to the market", "Luz is going to the market. Listen to the story. Circle the 3 things Luz buys.", ("For grown-ups", "Read once, slowly: “Luz walks to the market. First she buys a shiny red apple. Then she buys a blue cup for her tea. Last, she finds a little yellow star for Leon!”")),
    (21, 17, "remember", 1, "Look and remember", "Look at Leon’s shelf for 10 seconds. Then turn the page.", None),
    (22, 18, "remember", 1, "What did you see?", "Circle the 4 things you saw on Leon’s shelf.", ("Parent's Little Tip", "No peeking! If your child wants to check, turn back together afterwards.")),
    (23, 19, "remember", 2, "Three cups", "Remember the colors of the cups. Then turn the page.", None),
    (24, 20, "remember", 2, "Color the cups", "Color the cups in the same order you saw.", ("Try Another Way", "Can you say the colors backwards?")),
    (25, 21, "remember", 2, "Leon’s room", "Look at Leon’s room for 10 seconds. Then turn the page.", None),
    (26, 22, "remember", 2, "What is missing?", "Something is missing from Leon’s room. Draw it.", ("Ask Leon", "What else could Leon put in his room?")),
    (29, 24, "shapes", 1, "Shape robot", "Color the circles red. Color the squares blue.", ("Try Another Way", "Draw your own shape robot on a piece of paper!")),
    (30, 25, "shapes", 2, "Castle triangles", "How many triangles can you find? Color them and count.", ("Parent's Little Tip", "Count together, touching each triangle once.")),
    (31, 26, "shapes", 1, "Shapes around us", "Draw a line from each shape to a thing with the same shape.", ("Ask Leon", "Can you find a circle in your room?")),
    (32, 27, "shapes", 1, "Color by number", "Color each part with the color of its number.", None),
    (33, 28, "shapes", 1, "Big and small", "Circle the biggest one. Draw a line under the smallest one.", ("Try Another Way", "Draw something even smaller!")),
    (34, 29, "shapes", 1, "Trace the shapes", "Trace the dotted lines. Start at the green dot.", None),
    (36, 30, "patterns", 1, "What comes next?", "Look at the pattern. Draw what comes next.", ("Try Another Way", "Make the pattern longer!")),
    (37, 31, "patterns", 1, "Bead necklace", "Finish the necklace. Color the white beads to keep the pattern.", None),
    (38, 32, "patterns", 2, "Sun and moon", "Look at the pattern. Draw what comes next.", ("Parent's Little Tip", "Say the pattern aloud together: “sun, moon, moon, sun…”. Hearing it helps.")),
    (39, 33, "patterns", 2, "Big, small, big", "Look at the sizes. Draw what comes next in each row.", None),
    (40, 34, "patterns", 1, "My own pattern", "Look at Leon’s and Luz’s patterns. Now make your own! Color the beads. Then tell a grown-up your rule.", None),
    (41, 35, "patterns", 2, "Pattern train", "One wagon is empty. Draw the missing shape.", ("Try Another Way", "Clap the pattern: clap, clap, stomp, stomp!")),
    (43, 36, "logic", 1, "What goes together?", "Draw a line between things that go together.", ("Ask Leon", "Can you find another pair at home?")),
    (44, 37, "logic", 1, "Animals or fruit?", "Draw a line from each picture to the right box.", None),
    (45, 38, "logic", 2, "Who am I?", "Listen to each riddle. Circle the answer.", None),
    (46, 39, "logic", 2, "First, next, last", "What happens first? Write 1, 2 and 3 in the boxes.", ("Ask Leon", "What happens after the flower?")),
    (47, 40, "logic", 2, "Which does not belong?", "Circle the one that does not belong with the others.", ("Ask Leon", "Can you explain why?")),
    (48, 41, "logic", 2, "Dry feet", "Help Leon get home without stepping in a puddle. Which path: A, B or C?", None),
    (49, 42, "logic", 3, "Leon’s picture grid", "Each picture goes once in every row and every column. Draw the 2 missing pictures.", ("Parent's Little Tip", "Point to one row at a time and ask: “Which picture is missing here?”")),
    (51, 43, "numbers", 1, "How many balls?", "Count the balls. Circle the number.", None),
    (52, 44, "numbers", 1, "Count to 10", "Count. Write the number in the box.", ("Ask Leon", "Which row has the most?")),
    (53, 45, "numbers", 1, "Which has more?", "In each row, circle the box with more.", ("Ask Leon", "How many more?")),
    (54, 46, "numbers", 2, "Number path", "Help Leon reach Luz. Follow the numbers 1, 2, 3 … 9 in order. Color the path.", None),
    (55, 47, "numbers", 2, "Dot to dot", "Connect the dots from 1 to 15. Who is hiding?", ("Try Another Way", "Draw a friend for the one who is hiding!")),
    (56, 48, "numbers", 2, "Adding apples", "Count all the apples. Write how many in the box.", ("Parent's Little Tip", "Use real objects, like spoons or toys, to check the answer together.")),
    (57, 49, "numbers", 2, "Flying away", "Some birds fly away (look at the arrows). How many birds stay?", ("Parent's Little Tip", "Zero is a real answer! “No birds stay” is correct.")),
    (58, 50, "numbers", 2, "Missing numbers", "Write the missing number.", ("Try Another Way", "Count backwards from 10!")),
    (59, 51, "numbers", 2, "Make 5", "Draw more dots so each row has 5. How many did you add?", ("Ask Leon", "How many ways can you make 5?")),
    (61, 52, "words", 2, "Letter hunt", "Circle every A and every a.", None),
    (62, 53, "words", 1, "First letters", "Say the name of each picture. Draw a line to its first letter.", ("Ask Leon", "What else starts with B?")),
    (63, 54, "words", 2, "Same first sound", "Say “sun”. Circle the pictures that start with the same sound.", ("Parent's Little Tip", "Stretch the first sound: “sssun”, “sssock”…")),
    (64, 55, "words", 2, "Rhyme time", "Say the words. Draw a line between the words that rhyme.", ("Parent's Little Tip", "Say the words slowly and stretch the ending: “c-at… h-at”.")),
    (65, 56, "words", 1, "Trace LUZ", "Trace Luz’s name. Start at the green dots.", None),
    (66, 57, "words", 2, "Word and picture", "Read the word with a grown-up. Draw a line to the picture.", ("Try Another Way", "Draw a picture for the word HAT.")),
    (67, 58, "words", 2, "Listen and do", "Listen to your grown-up. Do what they say — one step, two steps, three steps!", ("For grown-ups", "Read one at a time: 1. “Color the hat blue.” 2. “Draw a sun in the sky, then color the tree green.” 3. “Put an X on the fish, draw a cloud, then circle the hat.”")),
    (68, 59, "words", 2, "Tell the story", "Leon grows a flower. Write 1, 2, 3 in the right order. Then tell the story!", ("Ask Leon", "What happens next?")),
    (70, 60, "space", 1, "Top shelf", "Circle the things on the top shelf.", ("Ask Leon", "What is on the bottom shelf?")),
    (71, 61, "space", 1, "Where is the cat?", "One cat is on the table. One cat is under the table. One cat is in the box. Color the cat under the table.", None),
    (72, 62, "space", 2, "This way!", "Circle the fish that swim this way →", ("Ask Leon", "Which way do the other fish swim?")),
    (73, 63, "space", 2, "Mirror butterfly", "Trace the other half of the butterfly. Make both sides the same. Then color it.", None),
    (74, 64, "space", 1, "Which piece fits?", "Which piece fits in the hole? Circle it.", ("Try Another Way", "Draw a shape that fits a circle hole.")),
    (75, 65, "space", 2, "Help Leon find Luz", "Find the way through the lines to Luz in the middle.", ("Parent's Little Tip", "If your child hits a wall, ask: “Where else could Leon go?”")),
    (77, 66, "feelings", 1, "How does Leon feel?", "Draw a line from each Leon to the face that feels the same.", ("Talk About It", "Read the words aloud. Ask: “When do you feel like this?”")),
    (78, 67, "feelings", 1, "What happened?", "Look at what happened to Leon. How might he feel? Circle a face. You can choose more than one!", ("Talk About It", "Would you feel the same? There is no wrong answer.")),
    (81, 68, "feelings", 1, "Star breathing", "Trace the star slowly with your finger. Breathe in as you go up. Breathe out as you go down.", None),
    (82, 69, "feelings", 1, "Stop and go", "Color a circle only when you hear “Go!” Stop when you hear “Stop!”", ("For grown-ups", "Say “Go!” and let your child color. Say “Stop!” and the pencil goes down. Mix short and long turns. Laugh together when someone moves on “Stop!”")),
    (83, 70, "feelings", 1, "Kind choices", "A grown-up reads each story. Color the heart next to the kind thing to do.", ("Talk About It", "Tell about a kind thing you did today.")),
    (84, 71, "feelings", 1, "My face today", "How do you feel today? Draw your face.", ("Talk About It", "How would you like to feel tomorrow?")),
    (86, 72, "big", 3, "Star maze", "Help Leon reach Luz. Count the stars on your way.", ("Parent's Little Tip", "Let your child try more than one path. Wrong turns are part of mazes!")),
    (89, 74, "big", 3, "Super mix", "1. Draw what comes next.  2. Circle the odd one out.  3. Count the stars.", ("Parent's Little Tip", "Do one part at a time. A short break between parts is fine.")),
]

# Openers: page, island, painting key, character, bubble, art-detective question, adult line
OPENERS = [
    (10, "look", "10", "leon", "Let’s look very, very carefully!", "Can you find a spiral in Robert’s painting?", "your child practises looking carefully and noticing small details."),
    (19, "remember", "02", "luz", "Look, close your eyes… what do you remember?", "Look for 5 seconds. Close your eyes. Name one color you saw.", "your child practises remembering what they see and hear."),
    (28, "shapes", "09", "leon", "Shapes are everywhere!", "Point to a shape with 3 corners.", "your child explores shapes, colors and sizes."),
    (35, "patterns", "06", "luz", "What comes next? Let’s find out!", "Find lines that go the same way.", "your child spots and makes patterns."),
    (42, "logic", "13", "leon", "Hmm… why? Let’s think!", "Is it a bird or a fish? Why do you think so?", "your child sorts, matches and explains ideas."),
    (50, "numbers", "04", "luz", "1, 2, 3… let’s count!", "How many round circles can you find in Robert’s painting?", "your child counts, compares and adds small numbers."),
    (60, "words", "08", "leon", "Robert writes with shapes!", "Robert’s “letters” are not real. Make up a word for this painting!", "your child plays with sounds, letters and first words."),
    (69, "space", "15", "luz", "Up, down, left, right — where shall we go?", "Put your finger at the top. Can you get to the bottom on the blue lines?", "your child thinks about where things are and how they fit."),
    (76, "feelings", "12", "leon", "Feelings are like colors — there are lots!", "How does this painting make you feel? There is no wrong answer.", "your child names feelings and practises calming down."),
    (85, "big", "07", "both", "You visited every island. Ready for a Big Challenge?", "Follow one black stripe from one side to the other.", "your child combines everything practised so far."),
]
OPENER_TITLES = {"look": "Look Closely Island", "remember": "Remember Island", "shapes": "Shapes & Colors Island",
                 "patterns": "Patterns Island", "logic": "Logic Island", "numbers": "Numbers Island", "words": "Words Island",
                 "space": "Space Island", "feelings": "Feelings Island", "big": "Big Challenge Island"}

ORIG_TO_NEW = {a[1]: a[0] for a in ACT}
ORIG_TO_NEW.update({23: 27, 73: 87})
