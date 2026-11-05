"""Generate print HTML for the three volumes + covers.

Trim 300 x 240 mm (landscape), 3 mm bleed -> page box 306 x 246 mm.
All coordinates below are in mm relative to the TRIM box; `T()` adds the bleed.
"""
import json, os, html

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f"{R}/works.json"))
META = json.load(open(f"{R}/plates/meta.json"))
DET = json.load(open(f"{R}/plates/details.json"))
B = 3.0                     # bleed
W, H = 300.0, 240.0          # trim
PW, PH = W + 2 * B, H + 2 * B
SPINE = 10.0
PAGE_BG = "#EEEAE2"          # uncoated stock tone; plates carry their own sheet tone (#F7F3EC)
INK = "#1B1A17"
MUTED = "#6F6A61"
M = dict(top=20, bottom=24, outer=20, inner=26)
IMG = "../plates"            # html lives in build/

e = html.escape


def T(v):
    return v + B


def aspect(k):
    return META[k]["w"] / META[k]["h"]


def crop_box(k, crop, x, y, w, h, extra=""):
    """Absolutely positioned box (mm, page coords incl. bleed) showing a normalized crop of plate k (cover-fit)."""
    cx, cy, cw, ch = crop
    iw, ih = META[k]["w"], META[k]["h"]
    # scale so that crop covers the box
    s = max(w / (cw * iw), h / (ch * ih))           # mm per px
    dw, dh = iw * s, ih * s
    # center the crop in the box
    ox = -(cx * iw * s) - ((cw * iw * s) - w) / 2
    oy = -(cy * ih * s) - ((ch * ih * s) - h) / 2
    return (f'<div class="crop" style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm;{extra}">'
            f'<img src="{IMG}/{k}.jpg" style="width:{dw:.2f}mm;height:{dh:.2f}mm;left:{ox:.2f}mm;top:{oy:.2f}mm"></div>')


def fit(k, bw, bh):
    a = aspect(k)
    return (bw, bw / a) if bw / a <= bh else (bh * a, bh)


CSS = open(f"{R}/fonts/fonts.css").read() + f"""
@page {{ size: {PW}mm {PH}mm; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
html, body {{ background: #888; -webkit-print-color-adjust: exact; print-color-adjust: exact }}
.page {{ width: {PW}mm; height: {PH}mm; position: relative; overflow: hidden; background: {PAGE_BG};
        page-break-after: always; color: {INK}; font-family: 'Newsreader', serif; font-optical-sizing: auto }}
.abs {{ position: absolute }}
.crop {{ position: absolute; overflow: hidden }}
.crop img {{ position: absolute; max-width: none; display: block }}
.plate {{ position: absolute; display: block; box-shadow: 0 .35mm .9mm rgba(40,30,20,.16), 0 2.2mm 6mm rgba(40,30,20,.10) }}
.caps {{ font-family: 'Inter Tight', sans-serif; text-transform: uppercase; letter-spacing: .22em; font-weight: 600; font-size: 6.6pt }}
.mono {{ font-family: 'IBM Plex Mono', monospace; font-size: 6.6pt; letter-spacing: .02em }}
.display {{ font-family: 'Instrument Serif', serif; font-weight: 400; line-height: .86; letter-spacing: -.01em }}
.folio {{ position: absolute; bottom: {T(11)}mm; font-family: 'IBM Plex Mono', monospace; font-size: 6.6pt; color: {MUTED} }}
.cap {{ font-family: 'Inter Tight', sans-serif; font-size: 7.4pt; line-height: 1.45; color: {INK} }}
.cap b {{ font-weight: 600 }}
.cap i {{ font-family: 'Newsreader', serif; font-style: italic; font-size: 8.6pt }}
.cap .n {{ font-family: 'IBM Plex Mono', monospace; font-size: 6.6pt; color: {MUTED}; display:block; margin-bottom: 1.2mm }}
.essay p {{ font-size: 12.6pt; line-height: 1.6; text-align: left; hyphens: auto; margin-bottom: 0; text-indent: 6mm }}
.essay p:first-child {{ text-indent: 0 }}
.essay p:first-child::first-letter {{ font-family: 'Instrument Serif'; float: left; font-size: 46pt; line-height: .78; padding: 1.6mm 2.2mm 0 0 }}
.toc td {{ font-family: 'Inter Tight', sans-serif; font-size: 7.6pt; padding: 1.1mm 0; border-top: .15mm solid #CFC9BE }}
.toc td.n, .toc td.p {{ font-family: 'IBM Plex Mono', monospace; font-size: 6.6pt; color: {MUTED} }}
.toc td.p {{ text-align: right }}
"""


class Book:
    def __init__(self, vol):
        self.v = vol
        self.pages = []           # list of (kind, html)
        self.plate_page = {}      # work -> page number of the plate

    @property
    def n(self):
        return len(self.pages) + 1   # number of the page being added

    def verso(self):
        return self.n % 2 == 0

    def add(self, body, bg=None, folio=True):
        n = self.n
        style = f' style="background:{bg}"' if bg else ""
        f = ""
        if folio:
            side = f"left:{T(M['outer'])}mm" if n % 2 == 0 else f"right:{T(M['outer'])}mm"
            run = f"{e(D['artist'])} — {e(self.v['title'])}"
            f = (f'<div class="folio" style="{side}">{n:02d}</div>'
                 f'<div class="folio" style="{"left" if n % 2 == 0 else "right"}:{T(M["outer"] + 12)}mm">{run}</div>')
        self.pages.append(f'<section class="page"{style}>{body}{f}</section>')

    # ---- page types ---------------------------------------------------------
    def half_title(self):
        v = self.v
        self.add(f'''
        <div class="abs caps" style="left:{T(M['inner'])}mm;top:{T(M['top'])}mm">{e(D['artist'])}</div>
        <div class="abs display" style="left:{T(M['inner'])}mm;top:{T(132)}mm;font-size:34pt">{e(v['title'])}</div>
        ''', folio=False)

    def full_bleed(self, k, crop, label=None, dark=True):
        lab = ""
        if label:
            col = "#F4F0E8" if dark else INK
            side = f"left:{T(M['outer'])}mm" if self.verso() else f"right:{T(M['outer'])}mm"
            lab = (f'<div class="abs mono" style="{side};bottom:{T(10)}mm;color:{col};'
                   f'background:rgba(20,18,15,.55);padding:.8mm 1.6mm;color:#F4F0E8">{label}</div>')
        self.add(crop_box(k, crop, 0, 0, PW, PH) + lab, folio=False)

    def title_page(self):
        v = self.v
        x = T(M['inner'])
        self.add(f'''
        <div class="abs caps" style="left:{x}mm;top:{T(M['top'])}mm">{e(D['artist'])}</div>
        <div class="abs caps" style="left:{x}mm;top:{T(M['top'] + 5)}mm;color:{MUTED}">{e(D['collection'])}</div>
        <div class="abs display" style="right:{T(M['outer'])}mm;top:{T(M['top'] - 6)}mm;font-size:150pt;color:{v['accent']}">{v['id']}</div>
        <div class="abs" style="left:{x}mm;right:{T(M['outer'])}mm;top:{T(150)}mm;border-top:.25mm solid {INK}"></div>
        <div class="abs display" style="left:{x - 1.5}mm;top:{T(154)}mm;font-size:150pt">{e(v['title'])}</div>
        <div class="abs" style="right:{T(M['outer'])}mm;top:{T(157)}mm;text-align:right">
          <div style="font-style:italic;font-size:13pt">{e(v['subtitle'])}</div>
          <div class="caps" style="margin-top:3mm;color:{MUTED}">Volume {v['id']} de III</div>
        </div>
        ''', folio=False)

    def copyright(self):
        v = self.v
        lines = [
            f"© {D['year']} {D['artist']}. Todos os direitos reservados.",
            "Nenhuma parte desta publicação pode ser reproduzida sem autorização do artista.",
            "",
            f"{D['collection']} — Volume {v['id']}: {v['title']}",
            f"{D['publisher']}, primeira edição, {D['year']}.",
            "",
            "Projeto gráfico, digitalização e tratamento de imagem: edição do artista.",
            "Tipografia: Instrument Serif, Newsreader, Inter Tight, IBM Plex Mono.",
            "Formato: 30 × 24 cm. Miolo: papel offset/fine-art 170 g/m².",
        ]
        body = "<br>".join(e(l) for l in lines)
        self.add(f'''<div class="abs cap" style="left:{T(M['outer'])}mm;bottom:{T(M['bottom'])}mm;width:110mm;color:{MUTED}">{body}</div>''',
                 folio=False)

    def epigraph_contents(self):
        v = self.v
        x = T(M['inner'])
        ep = ""
        if v.get('epigraph'):
            src = f'<div class="caps" style="margin-top:4mm;color:{MUTED}">{e(v["epigraph_src"])}</div>' if v.get('epigraph_src') else ""
            ep = (f'<div class="abs" style="left:{x}mm;top:{T(40)}mm;width:150mm">'
                  f'<div style="font-style:italic;font-size:21pt;line-height:1.22;font-weight:300">“{e(v["epigraph"])}”</div>{src}</div>')
        rows = "".join(
            f'<tr><td class="n" style="width:14mm">{i + 1:02d}</td><td>{e(D["works"][k]["title"])}</td>'
            f'<td style="color:{MUTED}">{e(D["works"][k]["medium"])}</td><td class="p">{{P{k}}}</td></tr>'
            for i, k in enumerate(v['works']))
        toc = (f'<div class="abs" style="left:{x}mm;right:{T(M["outer"])}mm;bottom:{T(M["bottom"] + 4)}mm">'
               f'<div class="caps" style="margin-bottom:3mm">Pranchas</div>'
               f'<table class="toc" style="width:100%;border-collapse:collapse"><tr><td class="n" style="width:14mm"></td>'
               f'<td>Sobre este volume</td><td></td><td class="p">{{PESSAY}}</td></tr>{rows}'
               f'<tr><td class="n"></td><td>Índice das obras</td><td></td><td class="p">{{PINDEX}}</td></tr></table></div>')
        self.add(ep + toc, folio=False)

    def essay(self):
        v = self.v
        self.essay_page = self.n
        first = v['essay'][0].split('.')[0] + '.'
        self.add(f'''
          <div class="abs caps" style="left:{T(M['outer'])}mm;top:{T(M['top'])}mm;color:{v['accent_ink']};opacity:.8">Sobre este volume</div>
          <div class="abs display" style="left:{T(M['outer'])}mm;top:{T(M['top'] + 10)}mm;font-size:30pt;line-height:1.02;width:200mm;color:{v['accent_ink']}">{e(first)}</div>
          <div class="abs display" style="left:{T(M['outer']) - 3}mm;bottom:{T(6)}mm;font-size:300pt;line-height:.72;color:{v['accent_ink']};opacity:.95">{e(v['title'])}</div>
        ''', bg=v['accent'], folio=False)
        paras = "".join(f"<p>{e(p)}</p>" for p in v['essay'])
        self.add(f'''
          <div class="abs caps" style="left:{T(M['inner'])}mm;top:{T(M['top'])}mm">{e(v['title'])} — Volume {v['id']}</div>
          <div class="abs essay" lang="pt-BR" style="left:{T(M['inner'] + 72)}mm;top:{T(M["top"] + 2)}mm;width:150mm">{paras}</div>
        ''')

    def plate(self, k, idx):
        """Recto or verso page with the full work on the tipped-in sheet + caption."""
        self.plate_page[k] = self.n
        v = self.v
        verso = self.verso()
        left = M['outer'] if verso else M['inner']
        right = M['inner'] if verso else M['outer']
        bw, bh = W - left - right, H - M['top'] - M['bottom'] - 18
        w, h = fit(k, bw, bh)
        x = left + (bw - w) / 2
        y = M['top'] + (bh - h) / 2
        if aspect(k) < 1:  # portrait: plate to the outer side, caption in the free column
            x = (W - right - w) if not verso else left
        cap = (f'<span class="n">{v["id"]}.{idx + 1:02d}</span><i>{e(D["works"][k]["title"])}</i><br>'
               f'{e(D["works"][k]["medium"])}<br><span style="color:{MUTED}">{e(D["artist"])}</span>')
        if aspect(k) < 1:
            cx = (left if not verso else left + w + 10)
            capd = f'<div class="abs cap" style="left:{T(cx)}mm;bottom:{T(M["bottom"] + 18)}mm;width:50mm">{cap}</div>'
        else:
            capd = f'<div class="abs cap" style="left:{T(x)}mm;top:{T(y + h + 5)}mm;width:90mm">{cap}</div>'
        self.add(f'<img class="plate" src="{IMG}/{k}.jpg" style="left:{T(x):.2f}mm;top:{T(y):.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm">{capd}')

    def detail(self, k, idx):
        self.full_bleed(k, DET[k], label=f"{self.v['id']}.{idx + 1:02d} — detalhe")

    def index(self):
        v = self.v
        self.index_page = self.n
        cells = []
        works = v['works']
        cols = 3
        gx, gy = 8, 10
        # two pages: verso header + first half, recto second half
        half = (len(works) + 1) // 2
        for page_i, chunk in enumerate([works[:half], works[half:]]):
            verso = self.verso()
            left = M['outer'] if verso else M['inner']
            right = M['inner'] if verso else M['outer']
            colw = (W - left - right - gx * (cols - 1)) / cols
            parts = []
            if page_i == 0:
                parts.append(f'<div class="abs caps" style="left:{T(left)}mm;top:{T(M["top"])}mm">Índice das obras</div>')
                parts.append(f'<div class="abs display" style="left:{T(left)}mm;top:{T(M["top"] + 8)}mm;font-size:44pt">{e(v["title"])}</div>')
                top0 = M['top'] + 52
                avail = list(chunk)
            else:
                top0 = M['top'] + 52
                avail = list(chunk)
            for i, k in enumerate(avail):
                c, r = i % cols, i // cols
                tw, th = fit(k, colw, 62)
                x = left + c * (colw + gx)
                y = top0 + r * (62 + 26)
                gi = works.index(k)
                parts.append(f'<img class="plate" src="{IMG}/web/{k}.jpg" style="left:{T(x):.2f}mm;top:{T(y + 62 - th):.2f}mm;width:{tw:.2f}mm;height:{th:.2f}mm;box-shadow:none">')
                parts.append(f'<div class="abs cap" style="left:{T(x)}mm;top:{T(y + 65)}mm;width:{colw}mm">'
                             f'<span class="n">{v["id"]}.{gi + 1:02d} &nbsp;·&nbsp; p. {{P{k}}}</span>'
                             f'<i>{e(D["works"][k]["title"])}</i><br>{e(D["works"][k]["medium"])}</div>')
            self.add("".join(parts))

    def colophon(self):
        v = self.v
        vols = "".join(
            f'<div style="display:flex;gap:4mm;align-items:baseline;margin-top:1.6mm;opacity:{1 if o["id"] == v["id"] else .45}">'
            f'<span class="mono" style="width:8mm">{o["id"]}</span><span style="font-style:italic;font-size:11pt">{e(o["title"])}</span>'
            f'<span class="cap" style="color:{MUTED}">{e(o["subtitle"])}</span></div>' for o in D['volumes'])
        self.add(f'''
          <div class="abs" style="left:{T(M['inner'])}mm;bottom:{T(M['bottom'] + 8)}mm;width:120mm">
            <div class="caps" style="margin-bottom:3mm">{e(D['artist'])} — {e(D['collection'])}</div>{vols}
          </div>
          <div class="abs" style="right:{T(M['outer'])}mm;bottom:{T(M['bottom'] + 8)}mm;width:14mm;height:14mm;background:{v['accent']}"></div>
        ''', folio=False)

    def panorama(self):
        """Closing image that runs across the gutter (verso + recto)."""
        k, crop = self.v['panorama']['work'], self.v['panorama']['crop']
        SW = 2 * W + 2 * B
        self.add(crop_box(k, crop, 0, 0, SW, PH), folio=False)
        self.add(crop_box(k, crop, -(W + B), 0, SW, PH), folio=False)

    def blank(self):
        self.add("", folio=False)

    # ---- assembly -----------------------------------------------------------
    def build(self):
        v = self.v
        self.half_title()                              # 1
        self.full_bleed(v['frontis'], v['frontis_crop'])  # 2
        self.title_page()                              # 3
        self.copyright()                               # 4
        self.epigraph_contents()                       # 5
        self.essay()                                   # 6-7 essay spread (verso colour / recto text)
        for i, k in enumerate(v['works']):
            if self.verso():
                if i % 2 == 0:
                    self.detail(k, i); self.plate(k, i)
                else:
                    self.plate(k, i); self.detail(k, i)
            else:
                self.plate(k, i)
        if not self.verso():
            self.blank()
        self.index()
        # pad to a multiple of 4 leaving the colophon last
        if (-(len(self.pages) + 1)) % 4 >= 2 and self.verso():
            self.panorama()
        while (len(self.pages) + 1) % 4:
            self.blank()
        self.colophon()
        out = "\n".join(self.pages)
        for k, p in self.plate_page.items():
            out = out.replace("{P" + k + "}", f"{p:02d}")
        out = out.replace("{PESSAY}", f"{self.essay_page:02d}").replace("{PINDEX}", f"{self.index_page:02d}")
        return out


def cover(v):
    """Hardcover case artwork: back | spine | front, with bleed. (Confirm spine/board allowances with the printer.)"""
    CW = 2 * W + SPINE + 2 * B
    fx = B + W + SPINE           # front panel x
    band = 54
    art_h = H - band
    k = v['cover']['work']
    crop = [0, 0, 1, 1]
    front = crop_box(k, crop, fx, 0, W + B, B + art_h)
    body = f'''
    <div class="abs" style="left:0;top:{B + art_h}mm;width:{CW}mm;height:{band + B}mm;background:{v['accent']}"></div>
    <div class="abs" style="left:{B + W}mm;top:0;width:{SPINE}mm;height:{H + 2 * B}mm;background:{v['accent']}"></div>
    {front}
    <!-- front band typography -->
    <div class="abs display" style="left:{fx + 16}mm;top:{B + art_h + 9}mm;font-size:72pt;color:{v['accent_ink']}">{e(v['title'])}</div>
    <div class="abs" style="right:{B + 16}mm;top:{B + art_h + 12}mm;text-align:right;color:{v['accent_ink']}">
      <div class="caps" style="font-size:8.5pt;letter-spacing:.3em">{e(D['artist'])}</div>
      <div style="font-style:italic;font-size:11pt;margin-top:2.5mm;opacity:.85">{e(D['collection'])} · {e(v['subtitle'])}</div>
    </div>
    <div class="abs display" style="right:{B + 16}mm;bottom:{B + 8}mm;font-size:16pt;color:{v['accent_ink']};opacity:.7">{v['id']}</div>
    <!-- spine -->
    <div class="abs" style="left:{B + W}mm;top:{B}mm;width:{SPINE}mm;height:{H}mm;display:flex;align-items:center;justify-content:center">
      <div style="transform:rotate(90deg);white-space:nowrap;color:{v['accent_ink']};display:flex;gap:9mm;align-items:baseline">
        <span class="caps" style="font-size:7.5pt;letter-spacing:.3em">{e(D['artist'])}</span>
        <span class="display" style="font-size:15pt">{e(v['title'])}</span>
        <span class="mono" style="font-size:7pt;opacity:.8">{v['id']}/III</span>
      </div>
    </div>
    <!-- back -->
    <div class="abs" style="left:{B + 22}mm;top:{B + 24}mm;width:118mm">
      <div class="caps" style="margin-bottom:6mm">{e(D['artist'])} — {e(D['collection'])}</div>
      <div style="font-size:12.5pt;line-height:1.5">{e(v['essay'][0])}</div>
      <div style="font-size:12.5pt;line-height:1.5;margin-top:3mm;font-style:italic;color:{MUTED}">{e(v['essay'][-1])}</div>
    </div>
    <div class="abs" style="left:{B + 22}mm;top:{B + art_h + 13}mm;color:{v['accent_ink']}">
      {''.join(f'<div style="display:flex;gap:4mm;align-items:baseline;opacity:{1 if o["id"] == v["id"] else .55}"><span class="mono" style="width:8mm">{o["id"]}</span><span style="font-style:italic;font-size:10.5pt">{e(o["title"])}</span></div>' for o in D['volumes'])}
    </div>
    <img class="plate" src="{IMG}/{v['works'][1]}.jpg" style="left:{B + 168}mm;top:{B + 24}mm;width:{fit(v['works'][1], 108, 120)[0]:.1f}mm">
    '''
    css = CSS.replace(f"size: {PW}mm {PH}mm", f"size: {CW}mm {PH}mm").replace(
        f".page {{ width: {PW}mm;", f".page {{ width: {CW}mm;")
    return f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{css}</style></head><body><section class="page">{body}</section></body></html>'


if __name__ == "__main__":
    os.makedirs(f"{R}/build", exist_ok=True)
    for v in D['volumes']:
        b = Book(v)
        pages = b.build()
        doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{e(D["artist"])} — {e(v["title"])}</title><style>{CSS}</style></head><body>{pages}</body></html>'
        open(f"{R}/build/vol-{v['id']}-{v['slug']}.html", "w").write(doc)
        open(f"{R}/build/capa-{v['id']}-{v['slug']}.html", "w").write(cover(v))
        print(v['id'], len(b.pages), "páginas")
