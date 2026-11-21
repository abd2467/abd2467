"""Builds the SVG artwork for the GitHub profile README (data portfolio style).

Edit the CONTENT section below, then run:  python3 scripts/build.py
Every SVG embeds a subset of Host Grotesk / Geist Mono, so the type matches the portfolio.
Requires: pip install fonttools
"""
import base64, io, os, html, math, random
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'assets')
FONTS = {
    'hg500': os.path.join(HERE, 'fonts', 'host-grotesk-latin-500-normal.woff'),
    'hg300': os.path.join(HERE, 'fonts', 'host-grotesk-latin-300-normal.woff'),
    'mono': os.path.join(HERE, 'fonts', 'geist-mono-latin-400-normal.woff'),
}

# ------------------------------------------------------------------ CONTENT
NAME = 'abdallah diaa'
ROLE = 'data analyst'
PLACE = 'singapore'
TITLE = ['DATA, MADE', 'USEFUL']
FACTS = [('focus', 'simulation · optimisation · decisions'),
         ('core', 'python · simpy · or-tools · streamlit'),
         ('based', 'Singapore')]
INTRO = ['I turn open data into decisions a manager',
         'can act on: hospital flow, shipping, energy,',
         'retail and travel, each priced in money.']
PROJECTS = [
    ('Blindspot', 'radar change detection · uncertainty audit',
     'How much land change under the haze in Kalimantan peat never shows up in the fire hotspot record?',
     '71% of 122 km² of radar-detected change had no hotspot (61 to 75%)', 'NISAR radar, NASA FIRMS · NASA Space Apps 2026'),
    ('Hospital discharge flow', 'healthcare · discrete-event simulation',
     'Which lever buys the most per pound: more beds, faster discharge, or a discharge lounge?',
     '[Cutting delays by X hours beats Y beds: Z more seen in 4 hours]', 'NHS England A&E, MIMIC-IV-ED · SimPy'),
    ('Chokepoint disruption rerouting', 'shipping · stochastic network flow',
     'When a chokepoint loses capacity, how should traffic be rerouted to cut voyage time and emissions?',
     '[X fewer voyage-days, Y fewer t CO2 than rerouting everything]', 'IMF PortWatch · Pyomo, HiGHS'),
    ('EV charging, misjudged departures', 'energy · LP scheduling · behavioural bias',
     "How much does drivers' misjudgement of departure times hurt smart charging, and can we recover it?",
     '[Bias correction cuts peak by X kW, $Y a month]', 'Caltech ACN-Data, ACN-Sim · PuLP'),
    ('Fresh food, hidden demand', 'food retail · censored-demand inventory',
     'How much better can a store order fresh food once it corrects for demand hidden by stockouts?',
     '[Waste down X%, fill rate up Y points]', 'FreshRetailNet-50K · Tobit, simulation'),
    ('Bike rebalancing: trucks vs incentives', 'city transport · vehicle routing · simulation',
     'For the morning peak, what mix of trucks and rider incentives keeps the most stations usable?',
     '[Incentives at X% of riders cut truck-km by Y%]', 'Citi Bike, GBFS · OR-Tools, SimPy'),
    ('Hotel overbooking & deposits', 'hospitality · survival model · revenue',
     'How many rooms should a hotel overbook each night, and do deposits change guest behaviour?',
     '[Overbook X weekdays, Y weekends: +Z% net revenue]', 'Antonio et al. bookings · lifelines'),
]
STACK = [
    ('01', 'decision tools', 'Streamlit · Plotly · memos', 'Every project ends in a dashboard and a two-page memo a manager can act on.'),
    ('02', 'optimisation & simulation', 'SimPy · OR-Tools · PuLP · Pyomo', 'Simulation, network flow, scheduling and routing, each against a baseline.'),
    ('03', 'data & models', 'pandas · DuckDB · lifelines · scikit-learn', 'Open data checked, then survival, censored-demand and causal models.'),
]
HELLO = 'say hello'
# --------------------------------------------------------------------------

W = 1000
RED = '#E5372D'
THEMES = {
    'dark': dict(fg='#ECEBE6', muted='#A3A6AD', label='#C9CCD2', body='#B9BCC2', line='#30333A', sig='#3DDC97',
                 dotE=(130, 130, 140), dotC=(245, 235, 210)),
    'light': dict(fg='#111317', muted='#5D626B', label='#353940', body='#4B5058', line='#D5D7DB', sig='#0E9F6E',
                  dotE=(150, 154, 162), dotC=(17, 19, 23)),
}
E = html.escape
_tt = {k: TTFont(v) for k, v in FONTS.items()}


def width(text, font, size, tracking=0.0):
    t = _tt[font]; cmap = t.getBestCmap(); hm = t['hmtx']; upm = t['head'].unitsPerEm
    return sum(hm[cmap.get(ord(c), cmap.get(32))][0] for c in text) * size / upm + tracking * size * max(0, len(text) - 1)


def face(name, text):
    opts = subset.Options(); opts.flavor = 'woff'; opts.layout_features = ['kern', 'liga']
    f = TTFont(FONTS[name]); s = subset.Subsetter(opts)
    s.populate(text=''.join(sorted(set(text + ' .')))); s.subset(f)
    b = io.BytesIO(); f.save(b)
    fam = {'hg500': 'HG5', 'hg300': 'HG3', 'mono': 'GM'}[name]
    return "@font-face{font-family:%s;src:url(data:font/woff;base64,%s) format('woff')}" % (fam, base64.b64encode(b.getvalue()).decode())


def svg(w, h, body, used, extra_css=''):
    css = ''.join(face(k, v) for k, v in used.items() if v)
    css += '.d{font-family:HG5,sans-serif;font-weight:500}.l{font-family:HG3,sans-serif;font-weight:300}.m{font-family:GM,monospace;font-weight:400}'
    css += extra_css + '@media (prefers-reduced-motion:reduce){*{animation:none!important}}'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none"><style>{css}</style>{body}</svg>'


def logo(x, y, s, fg, dot):
    k = s / 100
    return f'<g transform="translate({x},{y}) scale({k})" stroke="{fg}" stroke-width="8"><circle cx="27" cy="64" r="22"/><path d="M49 42V90"/><circle cx="71" cy="64" r="22"/><path d="M93 14V90"/></g><circle cx="{x + 109 * k:.1f}" cy="{y + 85 * k:.1f}" r="{6.5 * k:.1f}" fill="{dot}"/>'


def write(name, s):
    with open(os.path.join(OUT, name), 'w') as f:
        f.write(s)


RISE = '.r{transform-box:fill-box}@keyframes up{from{transform:translateY(112%)}to{transform:none}}@keyframes fade{from{opacity:0}to{opacity:1}}'

for f in os.listdir(OUT):
    if f.endswith('.svg'):
        os.remove(os.path.join(OUT, f))

for mode, t in THEMES.items():
    # ------------------------------------------------------------ header
    body = logo(0, 6, 44, t['fg'], RED) + \
        f'<text class="d" x="{W/2}" y="40" text-anchor="middle" font-size="22" letter-spacing=".66" fill="{t["fg"]}">{E(ROLE.upper())}</text>' + \
        f'<text class="m" x="{W}" y="38" text-anchor="end" font-size="12" fill="{t["muted"]}">{E(PLACE)}</text>' + \
        f'<rect y="71" width="{W}" height="1" fill="{t["line"]}"/>'
    write(f'header-{mode}.svg', svg(W, 72, body, {'hg500': ROLE.upper(), 'mono': PLACE}))

    # ------------------------------------------------------------ hero: membrane dots + title
    HH = 520
    cols, rows = 56, 26
    sx, sy = W / cols, HH / rows
    cx, cy = W / 2, HH / 2
    md = math.hypot(cx, cy)
    dots = []
    for r in range(rows):
        for c in range(cols):
            x, y = (c + .5) * sx, (r + .5) * sy
            cf = (1 - min(1, math.hypot(x - cx, y - cy) / md * 1.4)) ** 1.5
            rgb = [int(t['dotE'][i] + (t['dotC'][i] - t['dotE'][i]) * cf) for i in range(3)]
            a = 0.08 + cf * 0.2
            # quieter behind the title and facts
            if 60 < y < 340 and x < 760: a *= 0.55
            if y > 380 and x < 420: a *= 0.55
            rad = 0.9 + cf * 0.6
            delay = (c * 0.15 + r * 0.12) % 6.28
            dots.append(f'<circle class="dt" style="animation-delay:-{delay:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="{rad:.2f}" fill="rgb({rgb[0]},{rgb[1]},{rgb[2]})" fill-opacity="{a:.3f}"/>')
    fs = 132
    lines = TITLE
    title = ''
    for i, ln in enumerate(lines):
        y = 172 + i * fs * 0.96
        extra = f'<tspan fill="{RED}">.</tspan>' if i == len(lines) - 1 else ''
        title += f'<svg x="0" y="{y - fs*0.84:.0f}" width="{W}" height="{fs*1.02:.0f}" overflow="hidden"><text class="l r" style="animation:up 1.3s cubic-bezier(.16,1,.3,1) {0.15 + i*0.13:.2f}s both" x="-4" y="{fs*0.84:.0f}" font-size="{fs}" letter-spacing="{-0.05*fs:.1f}" fill="{t["fg"]}">{E(ln)}{extra}</text></svg>'
    facts = ''.join(f'<text class="m" x="0" y="{410 + i*24}" font-size="12" fill="{t["muted"]}">{E(k)}</text><text class="m" x="64" y="{410 + i*24}" font-size="12" fill="{t["fg"]}">{E(v)}</text>' for i, (k, v) in enumerate(FACTS))
    intro = ''.join(f'<text class="l" x="{W}" y="{412 + i*30}" text-anchor="end" font-size="24" letter-spacing="-.48" fill="{t["fg"]}">{E(s)}</text>' for i, s in enumerate(INTRO))
    css = RISE + '@keyframes br{0%,100%{opacity:1}50%{opacity:.35}}.dt{animation:br 6.3s ease-in-out infinite}.ft{animation:fade 1.2s ease .6s both}'
    body = '<g>' + ''.join(dots) + '</g>' + \
        f'<text class="m ft" x="0" y="44" font-size="12" fill="{t["muted"]}">{E(NAME)}</text>' + title + \
        f'<g class="ft">{facts}{intro}</g>'
    write(f'hero-{mode}.svg', svg(W, HH, body, {'hg300': ''.join(TITLE) + '.' + ''.join(INTRO), 'mono': NAME + ''.join(k + v for k, v in FACTS)}, css))

    # ------------------------------------------------------------ project chapters
    for i, (ti, ty, q, dec, data) in enumerate(PROJECTS):
        H = 230
        def wrap(txt, n):
            out, cur = [], ''
            for w_ in txt.split():
                if cur and len(cur) + len(w_) + 1 > n: out.append(cur); cur = w_
                else: cur = (cur + ' ' + w_).strip()
            return out + [cur]
        ql = wrap(q, 52); dl = wrap(dec, 26)
        LK = 'see the live site' if i == 0 else 'read the write-up'
        qtxt = ''.join(f'<text class="d" x="180" y="{142 + k*24}" font-size="16" fill="{t["body"]}" style="font-weight:400">{E(s)}</text>' for k, s in enumerate(ql))
        dtxt = ''.join(f'<text class="l" x="724" y="{104 + k*24}" font-size="19" letter-spacing="-.4" fill="{t["fg"]}">{E(s)}</text>' for k, s in enumerate(dl))
        body = f'''<rect width="{W}" height="1" fill="{t["line"]}"/>
<text class="l" x="-4" y="104" font-size="96" letter-spacing="-5.8" fill="{t["fg"]}">{i:02d}</text>
<text class="m" x="180" y="108" font-size="12" fill="{t["label"]}">{E(ty)}</text>
<text class="m" x="180" y="{150 + len(ql)*24}" font-size="12" fill="{t["muted"]}">{E(data)}</text>
<text class="d" x="180" y="80" font-size="30" letter-spacing="-1.2" fill="{t["fg"]}">{E(ti)}</text>
{qtxt}
<rect x="700" y="56" width="1" height="146" fill="{t["line"]}"/>
<text class="m" x="724" y="74" font-size="12" fill="{t["muted"]}">{"the result" if i == 0 else "the decision"}</text>
{dtxt}
<text class="m" x="724" y="190" font-size="12" fill="{t["fg"]}">{LK}</text>
<rect x="724" y="196" width="{width(LK, "mono", 12):.0f}" height="1" fill="{t["fg"]}"/>
<path d="M{W-14} 30l8-8M{W-12} 22h6v6" stroke="{t["fg"]}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="{W-36}" cy="26" r="3.5" fill="{t["sig"]}"/>'''
        write(f'project-{i:02d}-{mode}.svg', svg(W, H, body, {'hg500': ti + q, 'hg300': f'{i:02d}' + dec, 'mono': ty + data + 'the decisionthe resultread the write-upsee the live site'}))

    # ------------------------------------------------------------ section labels
    for fname, left, right in (('label-work', '01 / projects', 'flagship · more in progress'),
                               ('label-stack', '02 / the stack, taken apart', 'fig. 7')):
        out = f'<text class="m" x="0" y="14" font-size="12" fill="{t["fg"]}">{E(left)}</text><text class="m" x="{W}" y="14" text-anchor="end" font-size="12" fill="{t["muted"]}">{E(right)}</text>'
        write(f'{fname}-{mode}.svg', svg(W, 24, out, {'mono': left + right}))

    # ------------------------------------------------------------ stack (three slices)
    SH = 300
    out = ''
    for k, (n, name, tools, desc) in enumerate(STACK):
        y = 40 + k * 90
        cx0, rx, ry = 120, 110, 22
        out += f'''<g class="sl" style="animation-delay:{k*0.15:.2f}s">
<path d="M{cx0-rx} {y} v40 a{rx} {ry} 0 0 0 {2*rx} 0 v-40" fill="{t["line"]}" fill-opacity=".35" stroke="{t["line"]}"/>
<ellipse cx="{cx0}" cy="{y}" rx="{rx}" ry="{ry}" fill="{t["line"]}" fill-opacity=".55" stroke="{RED}" stroke-width="1.5"/>
<circle cx="{cx0+rx-14}" cy="{y+40}" r="4" fill="{t["sig"]}"/>
<path d="M{cx0} {y} H{304}" stroke="{t["muted"]}" stroke-opacity=".55" stroke-width="1"/><circle cx="{cx0}" cy="{y}" r="2.5" fill="{t["fg"]}"/>
<text class="m" x="324" y="{y-10}" font-size="12" fill="{t["muted"]}">{n}  {E(name)}</text>
<text class="m" x="324" y="{y+10}" font-size="12" fill="{t["label"]}">{E(tools)}</text>
<text class="d" x="324" y="{y+34}" font-size="16" fill="{t["body"]}" style="font-weight:400">{E(desc)}</text></g>'''
    css = '@keyframes sl{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}.sl{animation:sl 1s cubic-bezier(.16,1,.3,1) both}'
    write(f'stack-{mode}.svg', svg(W, SH, out, {'hg500': ''.join(s[3] for s in STACK), 'mono': ''.join(s[0] + s[1] + s[2] for s in STACK)}, css))

    # ------------------------------------------------------------ footer
    fs2 = 168
    out = f'''<rect width="{W}" height="1" fill="{t["line"]}"/>
<text class="m" x="0" y="34" font-size="12" fill="{t["fg"]}">03 / contact</text>
<svg x="0" y="50" width="{W}" height="{fs2*0.98:.0f}" overflow="hidden"><text class="l r" style="animation:up 1.2s cubic-bezier(.16,1,.3,1) .1s both" x="{W/2}" y="{fs2*0.8:.0f}" text-anchor="middle" font-size="{fs2}" letter-spacing="{-0.065*fs2:.1f}" fill="{t["fg"]}">{E(HELLO)}<tspan fill="{RED}">.</tspan></text></svg>'''
    write(f'hello-{mode}.svg', svg(W, int(50 + fs2 * 0.98), out, {'hg300': HELLO + '.', 'mono': '03 / contact'}, RISE))

print('built', len(os.listdir(OUT)), 'files')
