#!/usr/bin/env python3
"""Generator for hero.svg -- BIO-TERMINAL / SEQUENCER CONSOLE direction.

Standard library only, deterministic.

    python3 gen.py [out.svg] [t0]

t0 (seconds, default 0) bakes a later animation time into the static state.
It exists only so a static renderer can preview other frames; the shipped
file is always generated with t0 = 0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "hero.svg")
T0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0

MONO = ("ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,"
        "'Liberation Mono',monospace")

# ---------------------------------------------------------------- palette
BG0 = "#050809"    # panel backdrop
BG1 = "#0A1214"    # terminal body
BG2 = "#101B1E"    # title bar
LINE = "#1E3033"   # hairlines
PH = "#2DFFC4"     # phosphor green-cyan (primary)
MINT = "#E4FFF6"   # brightest text
SOFT = "#9FDCCB"   # secondary text
DIM = "#6C948A"    # chrome / tertiary text
AMBER = "#FFB547"  # warm secondary accent
CYAN = "#22E4FF"   # chromatic fringe (cool)
RED = "#FF7A45"    # chromatic fringe (warm) + close dot

ADV = 0.6          # nominal monospace advance (em); pinned with textLength


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def mono(x, y, s, size, fill, weight=None, extra="", track=0.0):
    """Text pinned to a nominal monospace grid, so SF Mono, Menlo, Consolas
    and Liberation Mono all occupy exactly the same width."""
    n = len(s)
    adv = size * ADV + track
    tl = f' textLength="{f(n * adv - track)}"' if n > 1 else ""
    w = f' font-weight="{weight}"' if weight else ""
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{f(size)}" fill="{fill}"'
            f'{w}{tl}{extra}>{esc(s)}</text>')


def segs(x, y, parts, size, track=0.0):
    """Coloured segments laid on one monospace grid line."""
    out, col = [], 0
    adv = size * ADV + track
    for text, fill, weight in parts:
        if text.strip():
            lead = len(text) - len(text.lstrip(" "))
            out.append(mono(x + (col + lead) * adv, y, text.strip(" "), size,
                            fill, weight, track=track))
        col += len(text)
    return "".join(out)


def chevron(x, y, color=AMBER):
    return (f'<path d="M{f(x)} {f(y - 9.6)}l5.4 4.8-5.4 4.8" fill="none" '
            f'stroke="{color}" stroke-width="2" stroke-linecap="round" '
            f'stroke-linejoin="round"/>')


# ---------------------------------------------------------------- geometry
W, H = 880, 360
WX, WY, WW, WH = 20, 20, 840, 320          # terminal window
TB = 30                                    # title-bar height
DIV = 626                                  # pane divider x
X0 = 46                                    # left text margin
XC = X0 + 16                               # command text x
FS = 13.5                                  # terminal text size

Y_P1, Y_NAME, Y_TAG = 74, 150, 176
Y_P2, Y_FOCUS = 209, 231
Y_P3, Y_LOOP = 264, 287
Y_P4 = 323

NAME_SIZE = 86
NAME_ADV = NAME_SIZE * 0.62 + 2.6          # glyph pitch (explicit x list)
NAME_GAP = 28                              # word gap (narrower than a cell)
TAG_SIZE = 17

# helix (B-DNA proportions: 10 bp per turn, right-handed)
HX, HR = 757, 34                           # axis x, radius
ROW0, ROWDY, NROW = 80, 14, 17             # first base row, rise, base pairs
PITCH = ROWDY * 10
XL, XR = HX - 58, HX + 58                  # letter columns
TROT = 9.0                                 # seconds per full turn
SEQ = "GCATTGACCTATGGCAT"                  # strand 1, 5'->3' (top->bottom)
PAM = (11, 12, 13)                         # N G G on strand 1
COMP = {"A": "T", "T": "A", "G": "C", "C": "G"}
PHI0, K0 = 18.0, 2                         # static phase

S_LO, S_HI, O_LO, O_HI = 0.5, 1.3, 0.26, 1.0   # dot depth cue
EASE = "cubic-bezier(.3642,0,.6358,1)"         # sine ease (max err 2e-4)

# ---------------------------------------------------------------- styles
css = []
half = TROT / 2
css.append(f".sx,.rs,.dz{{animation:sx {f(half)}s {EASE} infinite alternate-reverse}}")
css.append(".rs{animation-name:rs}.dz{animation-name:dz}")
css.append(f"@keyframes sx{{from{{transform:translateX(-{HR}px)}}to{{transform:translateX({HR}px)}}}}")
css.append("@keyframes rs{from{transform:scaleX(-1)}to{transform:scaleX(1)}}")
css.append(f"@keyframes dz{{from{{transform:scale({S_LO});opacity:{O_LO}}}to{{transform:scale({S_HI});opacity:{O_HI}}}}}")

w = 2 * math.pi / TROT
TH_A0 = math.radians(36 * K0 + PHI0)       # strand-1 angle at row 0, t = 0
for k in range(10):
    th = math.radians(36 * k + PHI0) - w * T0
    # x(t) = r sin(th - w t) == r cos(2 pi tau / T), tau = t + (pi/2 - th) T / 2 pi
    tau_x = ((math.pi / 2 - th) % (2 * math.pi)) / (2 * math.pi) * TROT
    tau_z = ((-th) % (2 * math.pi)) / (2 * math.pi) * TROT
    sx, cz = math.sin(th), math.cos(th)
    sc = (S_LO + S_HI) / 2 + (S_HI - S_LO) / 2 * cz
    op = (O_LO + O_HI) / 2 + (O_HI - O_LO) / 2 * cz
    css.append(f".x{k}{{transform:translateX({f(HR * sx)}px);animation-delay:-{f(tau_x)}s}}")
    css.append(f".r{k}{{transform:scaleX({f(sx)});animation-delay:-{f(tau_x)}s}}")
    css.append(f".z{k}{{transform:scale({f(sc)});opacity:{f(op)};animation-delay:-{f(tau_z)}s}}")
# backbone: rotating a helix == sliding it along its axis by one pitch per turn
bb0 = -PITCH * ((T0 / TROT) % 1.0)
css.append(f".bb{{transform:translateY({f(bb0)}px);animation:bb {f(TROT)}s linear infinite;animation-delay:-{f(T0 % TROT)}s}}")
css.append(f"@keyframes bb{{from{{transform:translateY(0)}}to{{transform:translateY(-{PITCH}px)}}}}")
# cursor
css.append(".cur{animation:bl 1.2s linear infinite}")
css.append("@keyframes bl{0%,52%{opacity:1}56%,96%{opacity:.08}100%{opacity:1}}")
# chromatic fringes on the name
FR0, FR1 = 1.3, 2.4
css.append(f".ca{{transform:translateX(-{FR0}px);animation:ca 7s ease-in-out infinite}}")
css.append(f".cb{{transform:translateX({FR0}px);animation:cb 7s ease-in-out infinite}}")
css.append(f"@keyframes ca{{0%,100%{{transform:translateX(-{FR0}px)}}50%{{transform:translateX(-{FR1}px)}}}}")
css.append(f"@keyframes cb{{0%,100%{{transform:translateX({FR0}px)}}50%{{transform:translateX({FR1}px)}}}}")
# research-loop stage highlight (8 s, 2 s per stage)
css.append(".st{opacity:0;animation:st 8s linear infinite}")
css.append("@keyframes st{0%,21%{opacity:1}25%,96%{opacity:0}100%{opacity:1}}")
css.append(".s0{opacity:1}.s1{animation-delay:-6s}.s2{animation-delay:-4s}.s3{animation-delay:-2s}")
# arrow flow + loop glyph
css.append(".fl{animation:fl 1.5s linear infinite}@keyframes fl{to{stroke-dashoffset:-12}}")
css.append(".ro{animation:ro 12s linear infinite}@keyframes ro{to{transform:rotate(360deg)}}")
# base-calling pulse running 5'->3' down strand 1
STEP = 0.42
BC = STEP * NROW
css.append(f".bc{{opacity:.58;animation:bc {f(BC)}s linear infinite}}")
css.append("@keyframes bc{0%,18%,100%{opacity:.58}5%{opacity:1}}")
# read head: a scan line that reaches each row as its base is called
Y_S0, Y_S1 = ROW0 - ROWDY / 2, ROW0 + ROWDY * (NROW - 0.5)
PEAK = PAM[1]
p_sc = ((PEAK + 0.5) / NROW + T0 / BC) % 1.0
css.append(f".sc{{transform:translateY({f(Y_S0 + (Y_S1 - Y_S0) * p_sc)}px);animation:sc {f(BC)}s linear infinite;animation-delay:-{f(p_sc * BC)}s}}")
css.append(f"@keyframes sc{{0%{{transform:translateY({f(Y_S0)}px);opacity:0}}7%,93%{{opacity:1}}100%{{transform:translateY({f(Y_S1)}px);opacity:0}}}}")
css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}}")

# ---------------------------------------------------------------- defs
o = []
o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Alex Wang: experimental and computational cancer research">')
o.append("<title>Alex Wang: experimental x computational cancer research</title>")
o.append("<defs>")
o.append(f'<clipPath id="pc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
o.append(f'<clipPath id="hc"><rect x="{HX - 46}" y="{WY + TB + 1}" width="92" height="{WH - TB - 2}"/></clipPath>')


def radial(i, cx, cy, r, col, a):
    return (f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{col}" stop-opacity="{a}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')


o.append(radial("g1", 170, -30, 470, PH, ".16"))
o.append(radial("g2", 820, 390, 420, AMBER, ".10"))
o.append(radial("g3", HX, 192, 150, PH, ".10"))
o.append(f'<linearGradient id="nm" x1="0" y1="{Y_NAME - 62}" x2="0" y2="{Y_NAME}" gradientUnits="userSpaceOnUse">'
         f'<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#B4FFE8"/></linearGradient>')
o.append(f'<linearGradient id="rg" x1="-{HR}" y1="0" x2="{HR}" y2="0" gradientUnits="userSpaceOnUse">'
         f'<stop offset="0" stop-color="{AMBER}"/><stop offset=".46" stop-color="{AMBER}"/>'
         f'<stop offset=".46" stop-color="{AMBER}" stop-opacity="0"/>'
         f'<stop offset=".54" stop-color="{PH}" stop-opacity="0"/>'
         f'<stop offset=".54" stop-color="{PH}"/><stop offset="1" stop-color="{PH}"/></linearGradient>')
for gid, y1, y2, a1, a2 in (("ft", WY + TB + 1, 78, 1, 0), ("fb", 306, WY + WH - 1, 0, 1)):
    o.append(f'<linearGradient id="{gid}" x1="0" y1="{y1}" x2="0" y2="{y2}" gradientUnits="userSpaceOnUse">'
             f'<stop offset="0" stop-color="{BG1}" stop-opacity="{a1}"/>'
             f'<stop offset="1" stop-color="{BG1}" stop-opacity="{a2}"/></linearGradient>')

# backbone curves + depth gradients (opacity follows cos(theta) along y)
YA, YB = WY + TB - 6, WY + WH + 6 + PITCH


def theta(y, strand):
    return TH_A0 - 2 * math.pi * (y - ROW0) / PITCH + (math.pi if strand else 0)


def backbone(strand):
    n = int(math.ceil((YB - YA) / ROWDY))
    pts = []
    for j in range(n + 1):
        y = YA + j * ROWDY
        th = theta(y, strand)
        pts.append((HX + HR * math.sin(th), y, HR * math.cos(th) * (-2 * math.pi / PITCH)))
    d = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
    for (xa, ya, da), (xb, yb, db) in zip(pts, pts[1:]):
        h = (yb - ya) / 3
        d.append(f"C{f(xa + da * h)} {f(ya + h)} {f(xb - db * h)} {f(yb - h)} {f(xb)} {f(yb)}")
    return "".join(d)


def depth_grad(gid, strand, col, lo, hi):
    stops = []
    n = int(round((YB - YA) / (PITCH / 8)))
    for j in range(n + 1):
        y = YA + j * (YB - YA) / n
        c = math.cos(theta(y, strand))
        a = lo + (hi - lo) * (1 + c) / 2
        stops.append(f'<stop offset="{f(j / n)}" stop-color="{col}" stop-opacity="{f(a)}"/>')
    return (f'<linearGradient id="{gid}" x1="0" y1="{YA}" x2="0" y2="{YB}" gradientUnits="userSpaceOnUse">'
            + "".join(stops) + "</linearGradient>")


o.append(depth_grad("da", 0, PH, 0.14, 0.95))
o.append(depth_grad("db", 1, AMBER, 0.14, 0.95))
SX0, SX1 = XL + 9, XR - 9
o.append(f'<linearGradient id="sl" x1="{SX0}" y1="0" x2="{SX1}" y2="0" gradientUnits="userSpaceOnUse">'
         f'<stop offset="0" stop-color="{PH}" stop-opacity=".95"/><stop offset=".5" stop-color="{PH}" stop-opacity=".18"/>'
         f'<stop offset="1" stop-color="{PH}" stop-opacity=".95"/></linearGradient>')
o.append(f'<linearGradient id="sg" x1="0" y1="-16" x2="0" y2="0" gradientUnits="userSpaceOnUse">'
         f'<stop offset="0" stop-color="{PH}" stop-opacity="0"/><stop offset="1" stop-color="{PH}" stop-opacity=".13"/></linearGradient>')
o.append('<filter id="gl" x="-10%" y="-40%" width="120%" height="180%">'
         '<feGaussianBlur stdDeviation="5"/></filter>')
o.append("</defs>")
o.append("<style>" + "".join(css) + "</style>")

# ---------------------------------------------------------------- backdrop
o.append('<g clip-path="url(#pc)">'
         f'<rect width="{W}" height="{H}" fill="{BG0}"/>'
         f'<rect width="{W}" height="{H}" fill="url(#g1)"/>'
         f'<rect width="{W}" height="{H}" fill="url(#g2)"/></g>')
o.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="15.5" fill="none" stroke="#18292B"/>')

# ---------------------------------------------------------------- window
o.append(f'<rect x="{WX - 2}" y="{WY - 2}" width="{WW + 4}" height="{WH + 4}" rx="12" fill="none" '
         f'stroke="{PH}" stroke-opacity=".05" stroke-width="4"/>')
o.append(f'<rect x="{WX}" y="{WY}" width="{WW}" height="{WH}" rx="10" fill="{BG1}"/>')
o.append(f'<path d="M{WX} {WY + TB}V{WY + 10}a10 10 0 0 1 10-10H{WX + WW - 10}a10 10 0 0 1 10 10V{WY + TB}z" fill="{BG2}"/>')
o.append(f'<rect x="{DIV}" y="{WY + TB}" width="{WX + WW - DIV}" height="{WH - TB}" fill="url(#g3)"/>')
o.append(f'<path d="M{WX} {WY + TB + .5}H{WX + WW}M{DIV + .5} {WY + TB}V{WY + WH}" stroke="{LINE}" fill="none"/>')
o.append(f'<rect x="{WX + .5}" y="{WY + .5}" width="{WW - 1}" height="{WH - 1}" rx="9.5" fill="none" stroke="#24383B"/>')

o.append(f'<g font-family="{MONO}">')

# title bar
cy = WY + TB / 2
o.append(f'<circle cx="{WX + 22}" cy="{cy}" r="5" fill="{RED}"/>'
         f'<circle cx="{WX + 40}" cy="{cy}" r="5" fill="{AMBER}"/>'
         f'<circle cx="{WX + 58}" cy="{cy}" r="5" fill="{PH}"/>')
title = [("alex@tumor-immunology", SOFT, None), (": ~", DIM, None)]
tw = sum(len(t[0]) for t in title) * 12.5 * ADV
o.append(segs(W / 2 - tw / 2, cy + 4.4, title, 12.5))
orc = [("ORCID", DIM, None), (" 0009-0005-8480-5387", SOFT, None)]
ow = sum(len(t[0]) for t in orc) * 12 * ADV
o.append(segs(WX + WW - 22 - ow, cy + 4.3, orc, 12))

# --- block 1: whoami -> name + tagline
o.append(chevron(X0, Y_P1))
o.append(mono(XC, Y_P1, "whoami", FS, MINT))
xs = [X0 + i * NAME_ADV for i in range(4)]
xs += [X0 + 4 * NAME_ADV + NAME_GAP + i * NAME_ADV for i in range(4)]
name_right = xs[-1] + NAME_ADV
nattr = (f'x="{" ".join(f(v) for v in xs)}" y="{Y_NAME}" font-size="{NAME_SIZE}" '
         f'font-weight="800"')
NAME = "ALEXWANG"
o.append(f'<text {nattr} fill="{PH}" opacity=".45" filter="url(#gl)">{NAME}</text>')
o.append(f'<text {nattr} fill="{CYAN}" class="ca">{NAME}</text>')
o.append(f'<text {nattr} fill="{RED}" class="cb">{NAME}</text>')
o.append(f'<text {nattr} fill="url(#nm)">{NAME}</text>')
tag = [("Experimental ", MINT, 500), ("×", AMBER, 700),
       (" computational cancer research", MINT, 500)]
ntag = sum(len(t[0]) for t in tag)
measure = name_right - 5 - (X0 + 2)
o.append(segs(X0 + 2, Y_TAG, tag, TAG_SIZE,
              track=(measure - ntag * TAG_SIZE * ADV) / (ntag - 1)))

# --- block 2: focus
o.append(chevron(X0, Y_P2))
o.append(segs(XC, Y_P2, [("cat", MINT, None), (" focus.txt", SOFT, None)], FS))
focus = [("tumor immunology", PH, None), (" · ", AMBER, 700),
         ("functional genomics", PH, None), (" · ", AMBER, 700),
         ("single-cell & spatial omics", PH, None)]
o.append(segs(X0, Y_FOCUS, focus, FS))

# --- block 3: research loop
o.append(chevron(X0, Y_P3))
o.append(mono(XC, Y_P3, "./research-loop", FS, MINT))
stages = ["OBSERVE", "MODEL", "PERTURB", "VALIDATE"]
TS, TTR, PADX, TH, GAP = 12.5, 1.4, 11, 22, 34
x = X0
ty = Y_LOOP + 4.4
for i, s in enumerate(stages):
    tw_ = len(s) * (TS * ADV + TTR) - TTR
    bw = tw_ + 2 * PADX
    o.append(f'<rect x="{f(x + .5)}" y="{f(Y_LOOP - TH / 2 + .5)}" width="{f(bw - 1)}" height="{TH - 1}" rx="4" '
             f'fill="{PH}" fill-opacity=".06" stroke="{PH}" stroke-opacity=".45"/>')
    o.append(mono(x + PADX, ty, s, TS, MINT, 700, track=TTR))
    cls = f"st s{(i - int(T0 // 2)) % 4}"
    o.append(f'<g class="{cls}"><rect x="{f(x)}" y="{f(Y_LOOP - TH / 2)}" width="{f(bw)}" height="{TH}" rx="4" fill="{AMBER}"/>'
             + mono(x + PADX, ty, s, TS, "#0B0F0C", 700, track=TTR) + "</g>")
    x += bw
    if i < len(stages) - 1:
        a, b = x + 7, x + GAP - 7
        o.append(f'<path class="fl" d="M{f(a)} {Y_LOOP}H{f(b - 1.5)}" stroke="{PH}" stroke-opacity=".85" stroke-width="1.5" stroke-dasharray="3 3" fill="none"/>')
        o.append(f'<path d="M{f(b - 4.5)} {Y_LOOP - 4}l4.5 4-4.5 4" stroke="{PH}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        x += GAP
# loop glyph (closes the cycle back to OBSERVE)
gx, r = x + 20, 6.5
a0, a1 = math.radians(-50), math.radians(240)
p0 = (r * math.cos(a0), r * math.sin(a0))
p1 = (r * math.cos(a1), r * math.sin(a1))
tx, tyv = -math.sin(a1), math.cos(a1)


def rot(vx, vy, deg):
    c, s_ = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return vx * c - vy * s_, vx * s_ + vy * c


h1, h2, hl = rot(-tx, -tyv, 32), rot(-tx, -tyv, -32), 4.6
o.append(f'<g transform="translate({f(gx)} {Y_LOOP})"><g class="ro">'
         f'<path d="M{f(p0[0])} {f(p0[1])}A{r} {r} 0 1 1 {f(p1[0])} {f(p1[1])}'
         f'M{f(p1[0] + h1[0] * hl)} {f(p1[1] + h1[1] * hl)}L{f(p1[0])} {f(p1[1])}L{f(p1[0] + h2[0] * hl)} {f(p1[1] + h2[1] * hl)}" '
         f'fill="none" stroke="{AMBER}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></g></g>')

# --- block 4: waiting prompt
o.append(chevron(X0, Y_P4))
o.append(f'<rect class="cur" x="{XC}" y="{Y_P4 - 12.5}" width="8.4" height="16" rx="1" fill="{PH}"/>')

# ---------------------------------------------------------------- helix pane


def yl(i):
    return ROW0 + ROWDY * i


# read head (drawn under the helix)
o.append(f'<g class="sc"><rect x="{SX0}" y="-16" width="{SX1 - SX0}" height="16" fill="url(#sg)"/>'
         f'<path d="M{SX0} 0H{SX1}" stroke="url(#sl)" stroke-width="1.2" fill="none"/></g>')
# backbone strands (slide one pitch per turn == rotate), clipped + faded
o.append('<g clip-path="url(#hc)"><g class="bb" fill="none" stroke-width="1.6">'
         f'<path d="{backbone(1)}" stroke="url(#db)"/>'
         f'<path d="{backbone(0)}" stroke="url(#da)"/></g></g>')
o.append(f'<rect x="{HX - 46}" y="{WY + TB + 1}" width="92" height="{78 - WY - TB - 1}" fill="url(#ft)"/>')
o.append(f'<rect x="{HX - 46}" y="306" width="92" height="{WY + WH - 1 - 306}" fill="url(#fb)"/>')

# base pairs: rungs + nucleotides at fixed rise, moving only sideways
for i in range(NROW):
    y = yl(i)
    k = (K0 - i) % 10
    kb = (k + 5) % 10
    o.append(f'<g transform="translate({HX} {y})">'
             f'<line class="rs r{k}" x1="-{HR}" x2="{HR}" stroke="url(#rg)" stroke-opacity=".4" stroke-width="1.2"/>'
             f'<g class="sx x{kb}"><circle class="dz z{kb}" r="3.4" fill="{AMBER}"/></g>'
             f'<g class="sx x{k}"><circle class="dz z{k}" r="3.4" fill="{PH}"/></g>'
             '</g>')

# strand polarity + sequence (strand 2 is the reverse complement)
for xx, ytxt, s in ((XL, yl(-1), "5′"), (XR, yl(-1), "3′"),
                    (XL, yl(NROW), "3′"), (XR, yl(NROW), "5′")):
    o.append(mono(xx - 7.2, ytxt + 4.2, s, 12, DIM))
for i in range(NROW):
    y = yl(i)
    a, b = SEQ[i], COMP[SEQ[i]]
    delay = ((i - PEAK) * STEP - 0.05 * BC - T0) % BC - BC
    st = f'style="animation-delay:{f(delay)}s"'
    if i in PAM:
        o.append(f'<text x="{XL}" y="{f(y + 4.2)}" font-size="12" font-weight="700" text-anchor="middle" fill="{AMBER}">{a}</text>')
        o.append(f'<text class="bc" {st} x="{XR}" y="{f(y + 4.2)}" font-size="12" font-weight="500" text-anchor="middle" fill="{SOFT}">{b}</text>')
    else:
        o.append(f'<g class="bc" {st} font-size="12" font-weight="500" text-anchor="middle" fill="{SOFT}">'
                 f'<text x="{XL}" y="{f(y + 4.2)}">{a}</text>'
                 f'<text x="{XR}" y="{f(y + 4.2)}">{b}</text></g>')

# annotations on strand 1: sgRNA target (protospacer) followed 3' by the NGG PAM
bx = XL - 16
ya, yb = yl(0) - 5, yl(PAM[0] - 1) + 5
o.append(f'<path d="M{bx + 4} {ya}H{bx}V{yb}H{bx + 4}" fill="none" stroke="{PH}" stroke-opacity=".7" stroke-width="1.2"/>')
o.append(f'<text transform="translate({bx - 7} {f((ya + yb) / 2)}) rotate(-90)" font-size="12" fill="{PH}" text-anchor="middle" letter-spacing="1">sgRNA</text>')
ya2, yb2 = yl(PAM[0]) - 5, yl(PAM[-1]) + 5
o.append(f'<path d="M{bx + 4} {ya2}H{bx}V{yb2}H{bx + 4}" fill="none" stroke="{AMBER}" stroke-width="1.2"/>')
o.append(f'<text transform="translate({bx - 7} {f((ya2 + yb2) / 2)}) rotate(-90)" font-size="12" fill="{AMBER}" text-anchor="middle" letter-spacing="1">PAM</text>')

o.append("</g></svg>")

svg = "\n".join(o)
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write(svg + "\n")
print(OUT, len(svg.encode("utf-8")), "bytes")
