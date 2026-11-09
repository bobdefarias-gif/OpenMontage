"""20 social posts (1080x1350, 4:5) for Leon's Thinking Book — Facebook + Instagram.
Facts used (keep exactly as worded; sources on the art):
  - WHO 2019 guideline: children 2–4 years — sedentary screen time no more than 1 hour a day; less is better.
  - AAP 2016 policy: children 2–5 years — limit screen use to 1 hour a day of high-quality programs, watched together.
  - Common Sense Media census 2020: children 0–8 average about 2 h 24 min of screen media a day.
No medical / brain claims (project rule + platform ad policies)."""
import os, html as H

R = os.path.dirname(os.path.abspath(__file__))
A = f"file://{R}/assets"
ART = f"file://{os.path.dirname(R)}/art_b"
F = f"file://{os.path.dirname(R)}/fonts/ttf/"
NAVY, CORAL, TEAL, GOLD, CREAM, BLUE, GREEN = "#1E2A5A", "#DF533C", "#2E9EA0", "#F7C93E", "#FBF6EE", "#2E6FD0", "#9ACB45"

CSS = "".join(f"@font-face{{font-family:'{a}';font-weight:{w};src:url({F}{f})}}" for a, w, f in [
    ("Andika", 400, "Andika-Regular.ttf"), ("Andika", 700, "Andika-Bold.ttf"), ("Baloo 2", 800, "Baloo2-800.ttf"),
    ("Baloo 2", 600, "Baloo2-600.ttf"), ("Lexend", 400, "Lexend-400.ttf"), ("Lexend", 600, "Lexend-600.ttf")]) + f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;font-family:'Andika';color:{NAVY}}}
.p{{position:relative;width:1080px;height:1350px;overflow:hidden}}
.a{{position:absolute}}
.h{{font:800 92px/0.98 'Baloo 2';letter-spacing:-1.5px}}
.h2{{font:800 64px/1.02 'Baloo 2';letter-spacing:-.8px}}
.t{{font:400 36px/1.35 'Andika'}}
.k{{font:600 24px 'Lexend';letter-spacing:3px;text-transform:uppercase}}
.src{{font:400 21px/1.35 'Lexend';opacity:.75}}
.pill{{display:inline-block;font:600 26px 'Lexend';padding:14px 28px;border-radius:60px}}
.book{{position:absolute;border-radius:6px 12px 12px 6px;box-shadow:0 3px 6px rgba(20,20,40,.25),0 30px 60px rgba(20,20,40,.28);overflow:hidden}}
.book:before{{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(90deg,rgba(0,0,0,.30) 0,rgba(255,255,255,.22) 9px,rgba(0,0,0,.06) 18px,rgba(0,0,0,0) 34px)}}
.book img{{width:100%;height:100%;display:block}}
.pg{{position:absolute;background:#fff;border-radius:10px;box-shadow:0 2px 4px rgba(0,0,0,.12),0 24px 50px rgba(20,20,40,.22);overflow:hidden}}
.pg img{{width:100%;display:block}}
.foot{{position:absolute;left:70px;right:70px;bottom:52px;display:flex;justify-content:space-between;align-items:center;font:600 24px 'Lexend'}}
.blob{{position:absolute;border-radius:50%}}
"""


def book(v, x, y, w, rot=0, z=1):
    h = w * 2200 / 1701
    return f'<div class="book" style="left:{x}px;top:{y}px;width:{w}px;height:{h:.0f}px;transform:rotate({rot}deg);z-index:{z}"><img src="{A}/cover_v{v}.png"></div>'


def page(name, x, y, w, rot=0, crop=None, h=None, z=1):
    """crop = (top fraction) to show part of a page; h = visible height"""
    style = f"left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z}"
    inner = f'<img src="{A}/{name}.png">'
    if crop is not None:
        full = w * 1340 / 1024
        style += f";height:{h}px"
        inner = f'<img src="{A}/{name}.png" style="margin-top:-{crop * full:.0f}px">'
    return f'<div class="pg" style="{style}">{inner}</div>'


def foot(col=NAVY, cta="Leon’s Thinking Book · ages 4–6 & 6–8"):
    return (f'<div class="foot" style="color:{col}"><span>{cta}</span>'
            f'<span style="display:flex;align-items:center;gap:12px"><img src="{ART}/leon.svg" style="width:58px;height:62px">'
            f'<span>by Robert de Farias</span></span></div>')


def post(bg, body, col=NAVY):
    return f'<div class="p" style="background:{bg}">{body}{foot(col)}</div>'


P = []

# 1 — hook
P.append(post(CREAM, f"""
<div class="blob" style="left:620px;top:-160px;width:620px;height:620px;background:{GOLD};opacity:.35"></div>
<div class="a k" style="left:70px;top:90px;color:{CORAL}">A simple swap</div>
<div class="a h" style="left:70px;top:140px;width:900px">Swap 15 minutes<br>of scrolling<br>for 15 minutes<br>of <span style="color:{CORAL}">thinking.</span></div>
<div class="a t" style="left:70px;top:620px;width:440px">Puzzles, memory games and real art for ages 4–8. Just a pencil — no screen, no charger.</div>
{book(1, 560, 560, 420, 6)}
<div class="a pill" style="left:70px;top:960px;background:{NAVY};color:#fff">Look inside ↓</div>"""))

# 2 — WHO fact
P.append(post(TEAL, f"""
<div class="a k" style="left:70px;top:90px;color:#fff">What the WHO recommends</div>
<div class="a" style="left:60px;top:150px;font:800 330px/0.9 'Baloo 2';color:#fff">1 h</div>
<div class="a h2" style="left:70px;top:470px;width:900px;color:#fff">or less of screen time a day for children aged 2 to 4.<br><span style="color:{GOLD}">Less is better.</span></div>
<div class="a t" style="left:70px;top:760px;width:520px;color:#fff">Looking for screen-free activities that still feel like play? Start here.</div>
{book(1, 620, 760, 360, -5)}
<div class="a src" style="left:70px;top:1110px;width:520px;color:#fff">Source: World Health Organization, Guidelines on physical activity, sedentary behaviour and sleep for children under 5 years of age (2019).</div>""", "#fff"))

# 3 — AAP fact
P.append(post("#FFF1E6", f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">Pediatricians say</div>
<div class="a h2" style="left:70px;top:150px;width:930px">For children aged 2 to 5: <span style="color:{CORAL}">no more than 1 hour</span> a day of high-quality screen time — ideally watched together.</div>
<div class="a" style="left:70px;top:520px;width:940px;height:3px;background:{NAVY};opacity:.15"></div>
<div class="a h2" style="left:70px;top:560px;width:560px;font-size:52px">So what about the other hours?</div>
<div class="a t" style="left:70px;top:720px;width:500px">Short, playful pages your child can do at the table, on the sofa or in a waiting room.</div>
{book(1, 600, 640, 400, 4)}
<div class="a src" style="left:70px;top:1130px;width:500px">Source: American Academy of Pediatrics, Media and Young Minds (2016).</div>"""))

# 4 — Common Sense stat
P.append(post(NAVY, f"""
<div class="a k" style="left:70px;top:90px;color:{GOLD}">Did you know?</div>
<div class="a" style="left:60px;top:140px;font:800 250px/0.9 'Baloo 2';color:{GOLD}">2h 24</div>
<div class="a h2" style="left:70px;top:390px;width:920px;color:#fff">is the average daily screen time of children aged 0 to 8.</div>
<div class="a h2" style="left:70px;top:610px;width:520px;font-size:54px;color:#fff">What could <span style="color:{GOLD}">15</span> of those minutes become?</div>
{page('v1_p13', 640, 610, 360, 5)}
<div class="a src" style="left:70px;top:1110px;width:520px;color:#fff">Source: Common Sense Media, The Common Sense Census: Media Use by Kids Age Zero to Eight (2020).</div>""", "#fff"))

# 5 — boredom
P.append(post(CREAM, f"""
<div class="blob" style="left:-200px;top:820px;width:620px;height:620px;background:{TEAL};opacity:.18"></div>
<div class="a h" style="left:70px;top:110px;width:950px">“I’m bored!”</div>
<div class="a h2" style="left:70px;top:230px;width:900px;color:{CORAL}">is often where thinking starts.</div>
<div class="a t" style="left:70px;top:360px;width:900px">Instead of handing over the phone, hand over a pencil and a puzzle. Small challenges, big “I did it!” moments.</div>
{page('v1_p11', 110, 560, 400, -5)}
{page('v2_p11', 560, 600, 400, 4)}"""))

# 6 — Volume 1 what's inside
isl = ["Look Closely", "Remember", "Shapes & Colors", "Patterns", "Logic", "Numbers", "Words", "Space", "Feelings"]
cols = ["#DF533C", "#2E9EA0", "#F6C83D", "#ED8A33", "#9ACB45", "#9CC4F0", "#F6C6D0", "#C8B8F0", "#F9DD83"]
chips = "".join(f'<div style="display:flex;align-items:center;gap:14px;margin:4px 0;font:700 30px Andika"><span style="width:26px;height:26px;border-radius:50%;background:{c}"></span>{n}</div>' for n, c in zip(isl, cols))
P.append(post("#fff", f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">Volume 1 · ages 4–6</div>
<div class="a h2" style="left:70px;top:140px;width:520px">9 islands of thinking games</div>
<div class="a" style="left:70px;top:330px">{chips}</div>
<div class="a t" style="left:70px;top:870px;width:470px;font-size:30px">+ a Big Challenge, a star chart, answers for grown-ups and a certificate.</div>
{book(1, 590, 300, 420, 3)}
<div class="a pill" style="left:70px;top:1090px;background:{CORAL};color:#fff">96 pages · no screen needed</div>"""))

# 7 — Volume 2
P.append(post("#EEF4FF", f"""
<div class="a k" style="left:70px;top:90px;color:{BLUE}">Volume 2 · ages 6–8</div>
<div class="a h2" style="left:70px;top:140px;width:900px">12 missions for curious minds aged 6 to 8</div>
<div class="a t" style="left:70px;top:330px;width:470px">Secret codes, picture sudoku, treasure maps, story problems, planning puzzles — and a final mission to open the chest.</div>
{book(2, 590, 330, 420, -3)}
{page('v2_p35', 90, 600, 380, -4)}
<div class="a pill" style="left:560px;top:1000px;background:{BLUE};color:#fff">The next step after Volume 1</div>"""))

# 8 — the series
P.append(post(GOLD, f"""
<div class="a k" style="left:70px;top:90px">The series</div>
<div class="a h" style="left:70px;top:140px;width:950px;font-size:84px">Grows with your child.</div>
{book(1, 110, 400, 400, -6, 2)}
{book(2, 560, 420, 400, 5, 1)}
<div class="a t" style="left:70px;top:1000px;width:940px;text-align:center">4–6 years: look, remember, count, feel.<br>6–8 years: codes, logic, plans and big challenges.</div>"""))

# 9 — try it: odd one out
P.append(post("#fff", f"""
<div class="a k" style="left:70px;top:90px;color:{TEAL}">Try it with your child</div>
<div class="a h2" style="left:70px;top:140px;width:900px">Which one is different? 🤔</div>
<div class="a t" style="left:70px;top:240px;width:900px">Ask your 4–6 year old. Then tell us in the comments how long it took!</div>
{page('v1_p13', 190, 360, 700, 0, 0.17, 720)}"""))

# 10 — try it: letter detective
P.append(post(CREAM, f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">Challenge · ages 6–8</div>
<div class="a h2" style="left:70px;top:140px;width:900px">How many letter <span style="color:{CORAL}">b</span> can your child find?</div>
<div class="a t" style="left:70px;top:310px;width:900px">Watch out for d, p and q! Write the answer below 👇</div>
{page('v2_p11', 190, 420, 700, 0, 0.165, 680)}"""))

# 11 — try it: picture sudoku
P.append(post("#EAF7F5", f"""
<div class="a k" style="left:70px;top:90px;color:{TEAL}">Weekend puzzle</div>
<div class="a h2" style="left:70px;top:140px;width:900px">Picture sudoku for kids 6+</div>
<div class="a t" style="left:70px;top:240px;width:900px">Each picture once in every row, column and box. No app, no screen — just thinking.</div>
{page('v2_p35', 190, 380, 700, 0, 0.165, 740)}"""))

# 12 — real art
P.append(post("#1E2A5A", f"""
<img class="a" src="{ART}/open_12.jpg" style="left:0;top:0;width:1080px;height:740px;object-fit:cover">
<div class="a" style="left:0;top:0;width:1080px;height:740px;background:linear-gradient(180deg,rgba(30,42,90,0) 50%,rgba(30,42,90,1) 100%)"></div>
<div class="a k" style="left:70px;top:780px;color:{GOLD}">Not your usual activity book</div>
<div class="a h2" style="left:70px;top:830px;width:940px;color:#fff">Every chapter opens with a real painting by the artist who made the book.</div>
<div class="a t" style="left:70px;top:1080px;width:940px;color:#fff;font-size:30px">“How does this painting make you feel?” — there are no wrong answers.</div>""", "#fff"))

# 13 — meet Leon & Luz
P.append(post(CREAM, f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">Meet the characters</div>
<div class="a h2" style="left:70px;top:140px;width:940px">Leon tries. Leon makes mistakes. <span style="color:{CORAL}">Leon tries again.</span></div>
<img class="a" src="{ART}/leon_luz.svg" style="left:220px;top:400px;width:640px;height:690px">
<div class="a t" style="left:70px;top:1090px;width:940px;text-align:center;font-size:32px">Children learn that mistakes are part of thinking — not the end of it.</div>"""))

# 14 — parent tip: ask don't tell
P.append(post("#FFF1E6", f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">Parent tip #1</div>
<div class="a h" style="left:70px;top:150px;width:940px">Ask,<br>don’t tell.</div>
<div class="a t" style="left:70px;top:420px;width:620px">When your child gets stuck, try:</div>
<div class="a" style="left:70px;top:500px;width:640px;font:700 40px/1.45 Andika">“What do you see?”<br>“How did you find it?”<br>“Is there another way?”<br>“What would Leon do?”</div>
<img class="a" src="{ART}/leon.svg" style="left:700px;top:520px;width:330px;height:360px">
<div class="a t" style="left:70px;top:960px;width:940px;font-size:30px">More tips like this are inside every page of Leon’s Thinking Book.</div>"""))

# 15 — parent tip: praise effort
P.append(post(TEAL, f"""
<div class="a k" style="left:70px;top:90px;color:#fff">Parent tip #2</div>
<div class="a h2" style="left:70px;top:150px;width:940px;color:#fff">Instead of “You’re so clever!” try:</div>
<div class="a" style="left:70px;top:390px;width:940px">
 {''.join(f'<div style="background:#fff;border-radius:24px;padding:26px 34px;margin:0 0 22px;font:700 44px Andika;color:{NAVY}">{t}</div>' for t in ['“You looked very carefully!”', '“You didn’t give up!”', '“You found a new way!”'])}
</div>
<div class="a t" style="left:70px;top:1020px;width:940px;color:#fff;font-size:32px">Praise the effort and children keep trying.</div>""", "#fff"))

# 16 — waiting room / travel
P.append(post(CREAM, f"""
<div class="a k" style="left:70px;top:90px;color:{TEAL}">Restaurant · car · waiting room</div>
<div class="a h2" style="left:70px;top:140px;width:940px">Phone-free waiting? Pack a pencil.</div>
<div class="a" style="left:70px;top:340px;font:700 38px/1.7 Andika">
 ✏️ A pencil or crayons<br>📖 One volume of Leon’s Thinking Book<br>⏱️ 10–15 minutes of focus<br>🎉 A star on the chart</div>
{book(1, 600, 600, 360, 8)}
{page('v1_p11', 110, 640, 360, -6)}"""))

# 17 — feelings
P.append(post("#FFF8DC", f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">Feelings island</div>
<div class="a h2" style="left:70px;top:140px;width:940px">“How might Leon feel?”</div>
<div class="a t" style="left:70px;top:250px;width:940px">Everyday situations to talk about feelings together — and there is more than one right answer.</div>
{page('v1_p79', 190, 420, 700, 0, 0.165, 670)}"""))

# 18 — three languages
P.append(post("#fff", f"""
<div class="a k" style="left:70px;top:90px;color:{BLUE}">Bilingual families 💛</div>
<div class="a h2" style="left:70px;top:140px;width:940px">Available in English, French and Dutch.</div>
<div class="a" style="left:70px;top:340px;display:flex;gap:26px">
 {''.join(f'<span class="pill" style="font-size:40px;padding:22px 44px;background:{c};color:#fff">{l}</span>' for l, c in [('EN', CORAL), ('FR', BLUE), ('NL', TEAL)])}</div>
<div class="a t" style="left:70px;top:500px;width:450px">Same games, same art, three languages. Perfect for home, school or grandma’s house.</div>
{book(1, 560, 480, 400, 4)}"""))

# 19 — 15 minute ritual
steps = [("1", "Snack & sit down", CORAL), ("2", "Pick one page (child chooses!)", TEAL), ("3", "10–15 minutes, together", BLUE), ("4", "Color a star on the chart", GOLD)]
st = "".join(f'<div style="display:flex;align-items:center;gap:26px;margin:0 0 30px"><span style="width:84px;height:84px;border-radius:50%;background:{c};color:#fff;font:800 48px Baloo\\ 2;display:flex;align-items:center;justify-content:center">{n}</span><span style="font:700 42px Andika">{t}</span></div>' for n, t, c in steps)
P.append(post(CREAM, f"""
<div class="a k" style="left:70px;top:90px;color:{CORAL}">After-school ritual</div>
<div class="a h2" style="left:70px;top:140px;width:940px">The 15-minute screen-free routine</div>
<div class="a" style="left:70px;top:360px">{st}</div>
{page('v1_p6', 380, 830, 320, 3)}"""))

# 20 — CTA
P.append(post(CORAL, f"""
<div class="a k" style="left:70px;top:90px;color:#fff">Now available</div>
<div class="a h" style="left:70px;top:140px;width:950px;color:#fff;font-size:84px">Learning to think, not just learning to answer.</div>
{book(1, 120, 520, 380, -5, 2)}
{book(2, 560, 540, 380, 5, 1)}
<div class="a pill" style="left:50%;transform:translateX(-50%);top:1080px;background:#fff;color:{CORAL};font-size:34px;padding:20px 50px;white-space:nowrap">Find it on Amazon · link in bio</div>""", "#fff"))

if __name__ == "__main__":
    os.makedirs(f"{R}/html", exist_ok=True)
    for i, body in enumerate(P, 1):
        open(f"{R}/html/post{i:02d}.html", "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>')
    print(len(P))
