"""Set 2 — three finished V1 EN pages: p.17 (look) / p.18 (remember) and p.30 (What comes next?)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from samples import CSS, page, A, INK, RED, MUTED, LINE, PW, SAFE_IN, SAFE_OUT, M

EYE = (f'<svg width="34pt" height="22pt" viewBox="0 0 34 22"><path d="M2 11C8 2 26 2 32 11C26 20 8 20 2 11Z" fill="none" stroke="{INK}" stroke-width="2.4"/>'
       f'<circle cx="17" cy="11" r="5" fill="{INK}"/><circle cx="19" cy="9" r="1.6" fill="#fff"/></svg>')


def lens(name, x, y, d, extra=""):
    return f'<div class="lens" style="left:{x}pt;top:{y}pt;width:{d}pt;height:{d}pt;{extra}"><img src="{A}/tile_{name}.png"></div>'


def margins(n):
    recto = n % 2 == 1
    return (SAFE_IN, SAFE_OUT) if recto else (SAFE_OUT, SAFE_IN)


SHOW = ["honey", "blue", "black"]                      # p.17
ASK = ["black", "sepia", "blue", "red", "honey", "green"]  # p.18 -> correct: 1, 3, 5


def p17():
    n = 17
    L, Rr = margins(n)
    bw = PW - L - Rr
    d = 156
    # three big circles in a gentle diagonal, like stepping stones
    pos = [(L, 200), (L + bw / 2 - d / 2, 340), (L + bw - d, 200)]
    body = "".join(lens(k, x, y, d) for k, (x, y) in zip(SHOW, pos))
    body += (f'<div class="abs" style="left:{L}pt;right:{Rr}pt;top:585pt;display:flex;flex-direction:column;align-items:center;gap:8pt">'
             f'{EYE}<div style="font-family:\'Baloo 2\';font-weight:700;font-size:17pt">Count to 10. Now turn the page!</div></div>')
    return page(n, "Look and remember",
                "Look at the three circles for 10 seconds. Try to remember their colors.",
                2, "Memory", body, "Details from paintings by Robert de Farias")


def p18():
    n = 18
    L, Rr = margins(n)
    bw = PW - L - Rr
    d, gx, gy = 132, 0, 52
    cols = 3
    sp = (bw - cols * d) / (cols - 1)
    body = []
    for i, k in enumerate(ASK):
        c, r = i % cols, i // cols
        x = L + c * (d + sp)
        y = 190 + r * (d + gy + 26)
        body.append(lens(k, x, y, d))
    body.append(f'<div class="abs" style="left:{L}pt;right:{Rr}pt;top:600pt;text-align:center;font-size:13pt;color:{MUTED}">'
                f'Not sure? Turn back and look again. That is fine!</div>')
    return page(n, "What did you see?",
                "Three of these circles were on the page before. Circle them.",
                2, "Memory", "".join(body), "Details from paintings by Robert de Farias")


ROWS = [  # sequence, options (A, B), correct index
    (["blue", "red", "blue", "red", "blue"], ["honey", "red"], 1),
    (["black", "black", "sepia", "black", "black"], ["sepia", "black"], 0),
    (["red", "honey", "blue", "red", "honey"], ["blue", "green"], 0),
]


def p30():
    n = 30
    L, Rr = margins(n)
    bw = PW - L - Rr
    d, g = 64, 12
    body = []
    top, band = 168, 142
    for r, (seq, opts, _) in enumerate(ROWS):
        y = top + r * band
        if r:
            body.append(f'<div class="abs" style="left:{L}pt;right:{Rr}pt;top:{y - 22}pt;border-top:1.2pt dashed {LINE}"></div>')
        body.append(f'<div class="abs" style="left:{L}pt;top:{y + d / 2 - 14}pt;font-family:\'Baloo 2\';font-weight:800;font-size:20pt;color:{MUTED}">{r + 1}</div>')
        x = L + 28
        for k in seq:
            body.append(lens(k, x, y, d)); x += d + g
        body.append(f'<div class="abs" style="left:{x}pt;top:{y}pt;width:{d}pt;height:{d}pt;border-radius:50%;border:2.4pt dashed {INK};'
                    f'display:flex;align-items:center;justify-content:center;font-family:\'Baloo 2\';font-weight:800;font-size:26pt;padding-top:4pt">?</div>')
        # options under the "?" side
        ox = L + bw - 2 * 54 - 22
        for i, k in enumerate(opts):
            xx = ox + i * (54 + 22)
            body.append(lens(k, xx, y + d + 14, 54 - 8))
            body.append(f'<div class="abs" style="left:{xx + 46 + 5}pt;top:{y + d + 26}pt;font-family:\'Baloo 2\';font-weight:800;font-size:15pt">{"AB"[i]}</div>')
        body.append(f'<div class="abs" style="left:{ox - 118}pt;top:{y + d + 26}pt;font-size:12pt;color:{MUTED}">Which one is next?</div>')
    return page(n, "What comes next?",
                "Look at the colors in each row. Which circle comes next? Circle <b>A</b> or <b>B</b>.",
                2, "Patterns", "".join(body), "Details from paintings by Robert de Farias")


def answers():
    n = 78
    L, Rr = margins(n)
    seen = [i for i, k in enumerate(ASK) if k in SHOW]
    grid = "".join(
        f'<span style="width:15pt;height:15pt;border-radius:50%;display:inline-block;margin:2pt;'
        f'background:{"#fff" if i in seen else "#C9CED8"};border:{"2.4pt solid " + RED if i in seen else "0"}"></span>'
        + ("<br>" if i == 2 else "") for i in range(6))
    def row(pg, title, ans, extra=""):
        return (f'<div style="display:flex;gap:16pt;padding:13pt 0;border-top:1pt solid {LINE};align-items:center">'
                f'<div class="foot" style="width:34pt;color:{INK};font-weight:600">p. {pg}</div>'
                f'<div style="flex:1"><div style="font-family:\'Baloo 2\';font-weight:700;font-size:13pt">{title}</div>'
                f'<div style="font-size:11.5pt;line-height:1.3">{ans}</div></div>{extra}</div>')
    mini = lambda k, on=False: (f'<span style="display:inline-block;width:26pt;height:26pt;border-radius:50%;overflow:hidden;margin:0 2pt;'
                                f'box-shadow:0 0 0 {"2.6pt " + RED if on else "1pt " + LINE}"><img src="{A}/tile_{k}.png" style="width:100%"></span>')
    pat = "".join(f'<div style="margin:6pt 0">{"".join(mini(k, i == c) for i, k in enumerate(o))} <b>{"AB"[c]}</b></div>' for _, o, c in ROWS)
    body = (f'<div class="abs" style="left:{L}pt;right:{Rr}pt;top:150pt">'
            + row(18, "What did you see?", "The 1st, 3rd and 5th circles (black, blue, yellow-brown).", f"<div>{grid}</div>")
            + row(30, "What comes next?", "Row 1: B · Row 2: A · Row 3: A", f"<div>{pat}</div>")
            + "</div>")
    return page(n, "Answers (continued)", "", 0, "Answers", body, "").replace(
        '<div class="abs stars"', '<div class="abs stars" style="display:none"')


if __name__ == "__main__":
    R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{p17()}{p18()}{p30()}{answers()}</body></html>'
    open(f"{R}/build/samples2-v1-en.html", "w").write(html)
    print("ok")
