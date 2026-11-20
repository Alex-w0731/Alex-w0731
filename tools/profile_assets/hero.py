#!/usr/bin/env python3
"""Hero banner: a mission-control view scanning a schematic tumor microenvironment.

Standard library only and deterministic (fixed random seeds). Part of the profile asset
pipeline: `python3 tools/profile_assets/build.py` writes assets/hud/hero.svg.
The drawing is a schematic, not data: cell positions carry no measurements.
"""
import math
import os
import random


W, H = 880, 360
CX, CY = 700, 180          # radar centre
T = 12.0                   # sweep period, seconds
TH0 = 38.0                 # beam clock angle at t = 0 (0 = up, clockwise)
R_SCOPE, R_BAND, R_OUT = 95, 113, 123
FRAME = 150                # half side of the bracketed frame

CYAN = "#2CE8FF"
CYAN_HI = "#9FF4FF"
MAG = "#FF3DAE"
MAG_HI = "#FF8CCB"
VIO = "#8E5BFF"
VIO_HI = "#C4B2FF"
MUTED = "#8FA3C8"


def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def P(r, a):
    """Clock angle a (deg, 0 = up, clockwise) at radius r -> local x, y."""
    t = math.radians(a)
    return (r * math.sin(t), -r * math.cos(t))


def arc(r, a1, a2, cw=True, move=True):
    x1, y1 = P(r, a1)
    x2, y2 = P(r, a2)
    d = (a2 - a1) % 360 if cw else (a1 - a2) % 360
    large = 1 if d > 180 else 0
    head = f"M{f(x1)} {f(y1)}" if move else f"L{f(x1)} {f(y1)}"
    return f"{head}A{f(r)} {f(r)} 0 {large} {1 if cw else 0} {f(x2)} {f(y2)}"


def smooth_closed(pts):
    """Closed Catmull-Rom spline through pts as cubic Beziers."""
    n = len(pts)
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d + "Z"


def blob(r0, seed, n=18):
    rnd = random.Random(seed)
    p2, p3, p5 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        r = r0 * (1 + 0.10 * math.sin(5 * t + p5) + 0.09 * math.sin(3 * t + p3) + 0.07 * math.sin(2 * t + p2))
        pts.append((r * math.cos(t), r * math.sin(t)))
    return smooth_closed(pts)


# --------------------------------------------------------------------------
# Tumour microenvironment (local coordinates, origin = radar centre)
# --------------------------------------------------------------------------
T0 = (-30.0, 20.0, 3.7)     # intratumoural T cell = nest centre
S = 15.6
HEX = [(S, 0), (S / 2, S * 0.866), (-S / 2, S * 0.866), (-S, 0), (-S / 2, -S * 0.866), (S / 2, -S * 0.866),
       (-2 * S, 0), (-1.5 * S, S * 0.866), (-1.5 * S, -S * 0.866), (0, S * 1.732), (-S, S * 1.732)]
RAD = [7.4, 6.3, 7.9, 6.6, 7.2, 6.1, 6.9, 5.8, 6.4, 7.6, 6.2]


def pack_nest():
    """Relax jittered hex seeds into an organic, non-overlapping tumour nest."""
    rnd = random.Random(11)
    cells = [[T0[0] + dx + rnd.uniform(-2.5, 2.5), T0[1] + dy + rnd.uniform(-2.5, 2.5), r]
             for (dx, dy), r in zip(HEX, RAD)]
    for _ in range(500):
        for i in range(len(cells)):
            for j in range(i + 1, len(cells)):
                a, b = cells[i], cells[j]
                d = math.hypot(a[0] - b[0], a[1] - b[1]) or 1e-6
                need = a[2] + b[2] + 0.9
                if d < need:
                    k = (need - d) / 2 / d
                    dx, dy = (a[0] - b[0]) * k, (a[1] - b[1]) * k
                    a[0] += dx; a[1] += dy; b[0] -= dx; b[1] -= dy
        for c in cells:
            d = math.hypot(c[0] - T0[0], c[1] - T0[1]) or 1e-6
            need = c[2] + T0[2] + 1.3
            if d < need:
                k = (need - d) / d
                c[0] += (c[0] - T0[0]) * k; c[1] += (c[1] - T0[1]) * k
            c[0] += (T0[0] - c[0]) * 0.012
            c[1] += (T0[1] - c[1]) * 0.012
    return [tuple(c) for c in cells]


TUM = pack_nest()


def margin_t(clock, r=3.8):
    """T cell docked on the outermost tumour cell in a given direction."""
    t = math.radians(clock)
    ux, uy = math.sin(t), -math.cos(t)
    idx = max(range(len(TUM)), key=lambda i: (TUM[i][0] - T0[0]) * ux + (TUM[i][1] - T0[1]) * uy)
    c = TUM[idx]
    x, y = c[0] + ux * (c[2] + r + 1.3), c[1] + uy * (c[2] + r + 1.3)
    for _ in range(60):
        for o in TUM:
            d = math.hypot(x - o[0], y - o[1]) or 1e-6
            need = o[2] + r + 1.3
            if d < need:
                x += (x - o[0]) * (need - d) / d
                y += (y - o[1]) * (need - d) / d
    return (x, y, r), idx


MARGIN = [margin_t(a) for a in (38, 92, 148, 328)]
TC = [T0] + [m[0] for m in MARGIN] + [
    (25, -34, 3.8), (46, -10, 3.6), (33, 24, 3.7), (9, -62, 3.5), (60, -44, 3.7),
    (-55, -46, 3.6), (20, 60, 3.6)]
N_DOCKED = 1 + len(MARGIN)
MC = [(-70, -14, 6.6), (53, 42, 6.8), (-4, 73, 6.2), (69, 6, 6.3), (-20, -67, 6.4)]

# engaged T cell -> tumour cell pairs (index into TC, index into TUM)
ENGAGED = [(k + 1, MARGIN[k][1]) for k in range(len(MARGIN))]
_near = sorted(range(len(TUM)), key=lambda i: math.hypot(TUM[i][0] - T0[0], TUM[i][1] - T0[1]))
ENGAGED += [(0, _near[0]), (0, _near[1])]


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def seg(a, b, pad=1.2):
    """Line between two nodes, trimmed to their outlines."""
    d = dist(a, b)
    if d < a[2] + b[2] + 2 * pad + 0.5:
        return None
    ux, uy = (b[0] - a[0]) / d, (b[1] - a[1]) / d
    x1, y1 = a[0] + ux * (a[2] + pad), a[1] + uy * (a[2] + pad)
    x2, y2 = b[0] - ux * (b[2] + pad), b[1] - uy * (b[2] + pad)
    return f"M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}"


def build_edges():
    faint, bars = [], []
    for ti, ui in ENGAGED:
        a, b = TC[ti], TUM[ui]
        d = dist(a, b)
        ux, uy = (b[0] - a[0]) / d, (b[1] - a[1]) / d
        m = a[2] + (d - a[2] - b[2]) / 2          # midpoint of the cleft
        mx, my = a[0] + ux * m, a[1] + uy * m
        px, py = -uy * 2.6, ux * 2.6
        bars.append(f"M{f(mx - px)} {f(my - py)}L{f(mx + px)} {f(my + py)}")
    # stromal network: immune cells to their nearest neighbours
    stroma = [("T", i, TC[i]) for i in range(len(TC))] + [("M", i, MC[i]) for i in range(len(MC))]
    seen = set()
    for kind, i, a in stroma:
        if kind == "T" and i == 0:
            continue
        cands = sorted(((dist(a, b), k2, j, b) for k2, j, b in stroma if b is not a and not (k2 == "T" and j == 0)),
                       key=lambda t: t[0])
        k = 0
        for d, k2, j, b in cands:
            if d > 52 or k >= 2:
                break
            key = tuple(sorted([(kind, i), (k2, j)]))
            if key not in seen:
                seen.add(key)
                s = seg(a, b)
                if s:
                    faint.append(s)
            k += 1
        if kind == "M" or (kind == "T" and i >= N_DOCKED):
            dn, un = min(((dist(a, u), u) for u in TUM), key=lambda t: t[0])
            if dn < 50:
                s = seg(a, un)
                if s:
                    faint.append(s)
    return faint, bars


def nest_contour(pad=5.0, n=20):
    cx = sum(p[0] for p in TUM) / len(TUM)
    cy = sum(p[1] for p in TUM) / len(TUM)
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        ux, uy = math.cos(t), math.sin(t)
        h = max((p[0] - cx) * ux + (p[1] - cy) * uy + p[2] for p in TUM) + pad
        pts.append((cx + ux * h, cy + uy * h))
    return smooth_closed(pts)


def clock_angle(x, y):
    return math.degrees(math.atan2(x, -y)) % 360


def ping_delay(x, y):
    t_hit = ((clock_angle(x, y) - TH0) % 360) / 360 * T
    return t_hit - T


# --------------------------------------------------------------------------
# SVG assembly
# --------------------------------------------------------------------------
CSS = """
.m{font-family:ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace}
.s{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes back{to{transform:rotate(-15deg)}}
@keyframes ping{0%{opacity:0;transform:scale(.55)}2.5%{opacity:.95;transform:scale(.8)}40%{opacity:0;transform:scale(1.25)}100%{opacity:0;transform:scale(1.25)}}
@keyframes phase{0%{opacity:0}3%{opacity:1}25%{opacity:1}29%{opacity:0}100%{opacity:0}}
@keyframes syn{0%,100%{opacity:.5}50%{opacity:1}}
@keyframes scan{0%{transform:translateY(0);opacity:0}7%{opacity:1}90%{opacity:1}100%{transform:translateY(300px);opacity:0}}
@keyframes head{0%{transform:translateX(0);opacity:0}4%{opacity:1}96%{opacity:1}100%{transform:translateX(256px);opacity:0}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
@keyframes pulse{0%{stroke-dashoffset:12}35%{stroke-dashoffset:-72}100%{stroke-dashoffset:-72}}
.sw{animation:spin 12s linear infinite}
.tk{animation:back 24s linear infinite}
.pg{opacity:0;animation:ping 12s linear infinite}
.ph{opacity:0;animation:phase 12s linear infinite}
.ph.on{opacity:1}
.sy{animation:syn 3.2s ease-in-out infinite}
.sc{transform:translateY(SCAN0px);animation:scan 9s linear infinite;animation-delay:SCAND}
.hd{transform:translateX(HEAD0px);animation:head 12s linear infinite;animation-delay:HEADD}
.bk{animation:blink 2.6s ease-in-out infinite}
.pl{animation:pulse 6s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def build_svg():
    o = []
    a = o.append
    scan0 = 122.0
    head0 = TH0 / 360 * 256
    css = (CSS.replace("SCAN0", f(scan0)).replace("SCAND", f"{-scan0 / 300 * 9:.2f}s")
              .replace("HEAD0", f(head0)).replace("HEADD", f"{-TH0 / 360 * T:.2f}s"))

    a(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
      f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
      f'aria-labelledby="t d">')
    a('<title id="t">Alex Wang: experimental × computational cancer research</title>')
    a('<desc id="d">Mission-control style banner. Left: the name ALEX WANG, the tagline and tool chips. '
      'Right: a circular TME SCAN radar sweeping over a schematic tumour microenvironment of tumour cells, '
      'CD8+ T cells and macrophages, with the research loop observe, model, perturb, validate around the dial.</desc>')
    a(f"<style>{css}</style>")

    # ---------------------------------------------------------------- defs
    a("<defs>")
    a('<clipPath id="pc"><rect width="880" height="360" rx="16"/></clipPath>')
    a(f'<clipPath id="fc"><rect x="{CX - FRAME}" y="{CY - FRAME}" width="{2 * FRAME}" height="{2 * FRAME}"/></clipPath>')
    a('<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
      '<stop offset="0" stop-color="#0C1838"/><stop offset=".55" stop-color="#060B1D"/>'
      '<stop offset="1" stop-color="#02040A"/></linearGradient>')
    a(f'<radialGradient id="gA" gradientUnits="userSpaceOnUse" cx="{CX}" cy="{CY}" r="250">'
      '<stop offset="0" stop-color="#19CFFF" stop-opacity=".2"/>'
      '<stop offset=".5" stop-color="#2B6BFF" stop-opacity=".07"/>'
      '<stop offset="1" stop-color="#2B6BFF" stop-opacity="0"/></radialGradient>')
    a('<radialGradient id="gB" gradientUnits="userSpaceOnUse" cx="90" cy="400" r="330">'
      '<stop offset="0" stop-color="#7A45FF" stop-opacity=".22"/>'
      '<stop offset="1" stop-color="#7A45FF" stop-opacity="0"/></radialGradient>')
    a('<radialGradient id="gC" gradientUnits="userSpaceOnUse" cx="880" cy="0" r="240">'
      '<stop offset="0" stop-color="#FF3DAE" stop-opacity=".1"/>'
      '<stop offset="1" stop-color="#FF3DAE" stop-opacity="0"/></radialGradient>')
    a('<pattern id="g1" width="15" height="15" patternUnits="userSpaceOnUse" x="10" y="0">'
      '<path d="M15 0H0V15" fill="none" stroke="#6FD3FF" stroke-opacity=".08" stroke-width="1"/></pattern>')
    a('<pattern id="g2" width="75" height="75" patternUnits="userSpaceOnUse" x="25" y="30">'
      '<path d="M75 0H0V75" fill="none" stroke="#6FD3FF" stroke-opacity=".13" stroke-width="1.2"/></pattern>')
    a(f'<radialGradient id="gmg" gradientUnits="userSpaceOnUse" cx="{CX}" cy="{CY}" r="560">'
      '<stop offset="0" stop-color="#fff"/><stop offset=".45" stop-color="#777"/>'
      '<stop offset="1" stop-color="#2a2a2a"/></radialGradient>')
    a('<mask id="gm"><rect width="880" height="360" fill="url(#gmg)"/></mask>')
    a('<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".55"/>'
      '<stop offset=".45" stop-color="#5B7BC8" stop-opacity=".18"/>'
      f'<stop offset="1" stop-color="{VIO}" stop-opacity=".5"/></linearGradient>')
    a('<linearGradient id="ng" x1="0" y1="0" x2="0" y2="1">'
      '<stop offset=".25" stop-color="#FFFFFF"/><stop offset="1" stop-color="#A6E8FF"/></linearGradient>')
    a('<filter id="nf" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>')
    a(f'<radialGradient id="scope" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="{R_SCOPE}">'
      '<stop offset="0" stop-color="#0D2B4E" stop-opacity=".85"/>'
      '<stop offset=".7" stop-color="#071630" stop-opacity=".9"/>'
      '<stop offset="1" stop-color="#0A2A48" stop-opacity=".92"/></radialGradient>')
    a(f'<radialGradient id="beam" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="{R_SCOPE}">'
      f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".1"/>'
      f'<stop offset="1" stop-color="{CYAN}" stop-opacity="1"/></radialGradient>')
    a(f'<linearGradient id="lead" gradientUnits="userSpaceOnUse" x1="0" y1="-4" x2="0" y2="-{R_SCOPE}">'
      f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".1"/>'
      '<stop offset="1" stop-color="#E9FDFF" stop-opacity="1"/></linearGradient>')
    for gid, col in (("hC", CYAN), ("hM", MAG), ("hV", VIO)):
        a(f'<radialGradient id="{gid}"><stop offset="0" stop-color="{col}" stop-opacity=".9"/>'
          f'<stop offset=".45" stop-color="{col}" stop-opacity=".3"/>'
          f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
    a(f'<linearGradient id="sl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>'
      f'<stop offset=".5" stop-color="#C9FBFF" stop-opacity=".4"/>'
      f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>')
    a(f'<radialGradient id="st" cx=".5" cy="1" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".1"/>'
      f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>')
    a(f'<linearGradient id="eg" gradientUnits="userSpaceOnUse" x1="458" y1="0" x2="526" y2="0">'
      f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".1"/>'
      f'<stop offset="1" stop-color="{CYAN}" stop-opacity=".75"/></linearGradient>')
    # word paths on the bezel
    rb_top = (R_SCOPE + R_BAND) / 2 - 4.3
    rb_bot = (R_SCOPE + R_BAND) / 2 + 4.3
    a(f'<path id="w0" d="{arc(rb_top, 1, 89)}"/>')
    a(f'<path id="w1" d="{arc(rb_bot, 179, 91, cw=False)}"/>')
    a(f'<path id="w2" d="{arc(rb_bot, 269, 181, cw=False)}"/>')
    a(f'<path id="w3" d="{arc(rb_top, 271, 359)}"/>')
    # macrophage glyph reused by the legend
    a(f'<path id="mac" d="{blob(6.4, 3)}"/>')
    a("</defs>")

    # ---------------------------------------------------------- background
    a('<g clip-path="url(#pc)">')
    a('<rect width="880" height="360" fill="url(#bg)"/>')
    a('<rect width="880" height="360" fill="url(#gB)"/>')
    a('<rect width="880" height="360" fill="url(#gC)"/>')
    a('<rect width="880" height="360" fill="url(#gA)"/>')
    a('<g mask="url(#gm)"><rect width="880" height="360" fill="url(#g1)"/>'
      '<rect width="880" height="360" fill="url(#g2)"/></g>')

    # ---------------------------------------------------------- left column
    X0 = 44
    LW = 428           # lock-up width (name, tagline, domains and chips justify to it)
    YT = 49.5          # top rail baseline
    YB = 319           # bottom rail baseline
    # top rail
    a(f'<rect class="bk" x="{X0}" y="{f(YT - 8.2)}" width="7.6" height="7.6" fill="{CYAN}"/>')
    a(f'<text class="m" x="{X0 + 16}" y="{YT}" font-size="12" letter-spacing="2.2" fill="{MUTED}">'
      f'<tspan fill="{CYAN_HI}" font-weight="600">MISSION CONTROL</tspan>'
      f'<tspan fill="#56678F"> // </tspan>TUMOR MICROENVIRONMENT</text>')
    a(f'<path d="M458 {f(YT - 4.3)}H526" stroke="url(#eg)" stroke-width="1" fill="none"/>')
    a(f'<path class="pl" d="M458 {f(YT - 4.3)}H526" stroke="#D9FCFF" stroke-width="1.2" fill="none" '
      f'stroke-dasharray="12 400" stroke-dashoffset="12" stroke-linecap="round"/>')
    a(f'<path d="M526 {f(YT - 8.3)}v8" stroke="{CYAN}" stroke-opacity=".8" stroke-width="1"/>')

    # name
    NY = 146
    name_attrs = f'class="s" x="{X0 - 2}" y="{NY}" font-size="68" font-weight="800" letter-spacing="4"'
    a(f'<text {name_attrs} fill="#19CFFF" opacity=".42" filter="url(#nf)">ALEX WANG</text>')
    a(f'<text {name_attrs} fill="url(#ng)">ALEX WANG</text>')
    # tagline + domains
    a(f'<text class="s" x="{X0}" y="{NY + 37}" font-size="19.5" font-weight="500" fill="#DCE9FF" letter-spacing=".1">'
      f'Experimental <tspan fill="{MAG_HI}">×</tspan> computational cancer research</text>')
    a(f'<text class="s" x="{X0}" y="{NY + 61}" font-size="13" fill="{MUTED}">'
      f'tumor immunology <tspan fill="{CYAN}">·</tspan> functional genomics '
      f'<tspan fill="{CYAN}">·</tspan> single-cell &amp; spatial omics</text>')

    # chips (computational toolkit in cyan, wet-lab screen in magenta)
    chips = [("R", 0), ("Python", 0), ("Seurat", 0), ("Scanpy", 0), ("CellChat", 0), ("CRISPR-Cas9", 1)]
    gap = 8
    pad = (LW - sum(len(c[0]) for c in chips) * 7.2 - gap * (len(chips) - 1)) / (2 * len(chips))
    x = X0
    cy0, ch, cut = NY + 86, 26, 5
    for label, kind in chips:
        w = len(label) * 7.2 + 2 * pad
        col, tcol = (CYAN, "#CFF6FF") if kind == 0 else (MAG, "#FFD0E9")
        pts = [(x + cut, cy0), (x + w, cy0), (x + w, cy0 + ch - cut), (x + w - cut, cy0 + ch),
               (x, cy0 + ch), (x, cy0 + cut)]
        a(f'<path d="M{" ".join(f(px) + " " + f(py) for px, py in pts)}Z" fill="{col}" fill-opacity=".07" '
          f'stroke="{col}" stroke-opacity=".55" stroke-width="1"/>')
        a(f'<text class="m" x="{f(x + w / 2)}" y="{f(cy0 + 17.2)}" font-size="12" text-anchor="middle" '
          f'fill="{tcol}">{label}</text>')
        x += w + gap

    # bottom rail: ORCID + phase ruler
    a(f'<text class="m" x="{X0}" y="{YB}" font-size="12" letter-spacing="1.4" fill="#A9B8D6">'
      f'<tspan fill="{CYAN_HI}" font-weight="600">ORCID</tspan> 0009-0005-8480-5387</text>')
    RX0, RL = 270, 256
    d_minor = "".join(f"M{RX0 + k * 8} {YB}v-3" for k in range(RL // 8 + 1) if k % 8)
    d_major = "".join(f"M{RX0 + k * 64} {YB}v-7" for k in range(5))
    a(f'<path d="M{RX0} {YB}H{RX0 + RL}" stroke="#6FD3FF" stroke-opacity=".4" stroke-width="1"/>')
    a(f'<path d="{d_minor}" stroke="#6FD3FF" stroke-opacity=".4" stroke-width="1"/>')
    a(f'<path d="{d_major}" stroke="{CYAN_HI}" stroke-opacity=".85" stroke-width="1.2"/>')
    a(f'<g transform="translate({RX0} {YB})"><g class="hd">'
      f'<path d="M0 -4.5l-3.6 -6.4h7.2z" fill="{CYAN_HI}"/>'
      f'<path d="M0 0v-4.5" stroke="{CYAN_HI}" stroke-width="1"/></g></g>')

    # ---------------------------------------------------------- radar frame
    x1, y1, x2, y2 = CX - FRAME, CY - FRAME, CX + FRAME, CY + FRAME
    a(f'<rect x="{x1}" y="{y1}" width="{2 * FRAME}" height="{2 * FRAME}" fill="#040A1A" fill-opacity=".35" '
      f'stroke="#6FD3FF" stroke-opacity=".14" stroke-width="1"/>')
    b = 18
    a(f'<path d="M{x1} {y1 + b}V{y1}H{x1 + b}M{x2 - b} {y1}H{x2}V{y1 + b}M{x2} {y2 - b}V{y2}H{x2 - b}'
      f'M{x1 + b} {y2}H{x1}V{y2 - b}" fill="none" stroke="{CYAN}" stroke-width="1.5"/>')
    a(f'<path d="M{CX} {y1}v5M{CX} {y2}v-5M{x1} {CY}h5M{x2} {CY}h-5" stroke="{CYAN}" stroke-opacity=".7" stroke-width="1"/>')
    # corner labels
    a(f'<circle class="bk" cx="{x1 + 15}" cy="{f(YT - 4.2)}" r="3" fill="{CYAN}"/>')
    a(f'<text class="m" x="{x1 + 25}" y="{YT}" font-size="12" font-weight="600" letter-spacing="2" fill="{CYAN_HI}">TME SCAN</text>')
    a(f'<text class="m" x="{x2 - 25}" y="{YT}" font-size="12" letter-spacing="1" text-anchor="end" fill="{CYAN_HI}">CD8+ T</text>')
    gx = x2 - 14
    a(f'<circle cx="{gx}" cy="{f(YT - 4.2)}" r="3.8" fill="{CYAN}"/>'
      f'<circle cx="{gx}" cy="{f(YT - 4.2)}" r="6" fill="none" stroke="{CYAN}" stroke-opacity=".5" stroke-width=".8"/>')
    a(f'<circle cx="{x1 + 15}" cy="{f(YB - 4.2)}" r="5.6" fill="#3A0F3C" stroke="{MAG}" stroke-width="1.1"/>'
      f'<circle cx="{x1 + 15}" cy="{f(YB - 4.2)}" r="2.4" fill="{MAG}"/>')
    a(f'<text class="m" x="{x1 + 27}" y="{YB}" font-size="12" letter-spacing="1" fill="{MAG_HI}">TUMOR</text>')
    a(f'<text class="m" x="{x2 - 26}" y="{YB}" font-size="12" letter-spacing="1" text-anchor="end" fill="{VIO_HI}">MACROPHAGE</text>')
    a(f'<g transform="translate({gx - 1} {f(YB - 4.2)})"><use xlink:href="#mac" fill="#22184F" stroke="{VIO_HI}" stroke-width="1.1"/>'
      f'<ellipse cx="1" cy="-.7" rx="2.5" ry="1.6" transform="rotate(-25)" fill="{VIO_HI}"/></g>')

    # ---------------------------------------------------------- instrument
    a(f'<g transform="translate({CX} {CY})">')
    a(f'<circle r="{R_BAND}" fill="#07122B" fill-opacity=".8"/>')
    a(f'<circle r="{R_SCOPE}" fill="url(#scope)"/>')
    # active-phase band segments
    for i in range(4):
        a1, a2 = 90 * i + 1.2, 90 * (i + 1) - 1.2
        d = (arc(R_BAND - 1.5, a1, a2) + arc(R_SCOPE + 1.5, a2, a1, cw=False, move=False) + "Z")
        on = " on" if i == 0 else ""
        delay = (((90 * i - TH0) % 360) / 360 * T) - T
        a(f'<path class="ph{on}" style="animation-delay:{delay:.2f}s" d="{d}" fill="{CYAN}" fill-opacity=".13"/>')
    # range rings + crosshair
    a(f'<circle r="{f(R_SCOPE / 3)}" fill="none" stroke="{CYAN}" stroke-opacity=".22" stroke-width=".7" stroke-dasharray="1.5 3.5"/>')
    a(f'<circle r="{f(2 * R_SCOPE / 3)}" fill="none" stroke="{CYAN}" stroke-opacity=".22" stroke-width=".7" stroke-dasharray="1.5 3.5"/>')
    a(f'<path d="M-{R_SCOPE} 0H-8M8 0H{R_SCOPE}M0 -{R_SCOPE}V-8M0 8V{R_SCOPE}" stroke="{CYAN}" stroke-opacity=".16" stroke-width=".7"/>')

    # sweep wedge (under the cells)
    n_l, step, peak = 18, 5.0, 0.42
    prof = [peak * (1 - j / n_l) ** 2 for j in range(n_l + 1)]
    a(f'<g transform="rotate({f(TH0)})"><g class="sw">')
    for k in range(1, n_l + 1):
        alpha = prof[k - 1] - prof[k]
        xa, ya = P(R_SCOPE, -k * step)
        a(f'<path d="M0 0L{f(xa)} {f(ya)}A{R_SCOPE} {R_SCOPE} 0 0 1 0 -{R_SCOPE}Z" fill="url(#beam)" fill-opacity="{alpha:.4f}"/>')
    a("</g></g>")

    # unclassified stromal cells: a faint point field
    rnd = random.Random(23)
    dust = []
    occupied = [(c[0], c[1], c[2] + 4) for c in TUM + TC + MC] + [(0, 0, 9)]
    while len(dust) < 46:
        rr, aa = (R_SCOPE - 7) * math.sqrt(rnd.random()), rnd.uniform(0, 2 * math.pi)
        x, y = rr * math.cos(aa), rr * math.sin(aa)
        if all(math.hypot(x - ox, y - oy) > orad for ox, oy, orad in occupied):
            dust.append((x, y))
            occupied.append((x, y, 5))
    a(f'<path d="{"".join(f"M{f(x)} {f(y)}h.01" for x, y in dust)}" stroke="#9FC4E8" stroke-opacity=".42" '
      f'stroke-width="1.5" stroke-linecap="round" fill="none"/>')

    # tumour nest contour
    a(f'<path d="{nest_contour()}" fill="{MAG}" fill-opacity=".07" stroke="{MAG}" stroke-opacity=".55" stroke-width=".8" stroke-dasharray="2.5 2.5"/>')

    # interaction lines
    faint, bars = build_edges()
    a(f'<path d="{"".join(faint)}" stroke="#8FDCFF" stroke-opacity=".32" stroke-width=".7" fill="none"/>')

    # ping halos
    for (x, y, r) in TUM:
        a(f'<g transform="translate({f(x)} {f(y)})"><circle class="pg" style="animation-delay:{ping_delay(x, y):.2f}s" r="15" fill="url(#hM)"/></g>')
    for (x, y, r) in MC:
        a(f'<g transform="translate({f(x)} {f(y)})"><circle class="pg" style="animation-delay:{ping_delay(x, y):.2f}s" r="15" fill="url(#hV)"/></g>')
    for (x, y, r) in TC:
        a(f'<g transform="translate({f(x)} {f(y)})"><circle class="pg" style="animation-delay:{ping_delay(x, y):.2f}s" r="13" fill="url(#hC)"/></g>')

    # cells
    for (x, y, r) in TUM:
        a(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#3A0F3C" stroke="{MAG}" stroke-width="1.1"/>'
          f'<circle cx="{f(x + 0.4)}" cy="{f(y - 0.3)}" r="{f(r * 0.42)}" fill="{MAG}"/>')
    for i, (x, y, r) in enumerate(MC):
        a(f'<g transform="translate({f(x)} {f(y)}) rotate({i * 67})"><path d="{blob(r, 10 + i)}" fill="#22184F" stroke="{VIO_HI}" stroke-width="1.1"/>'
          f'<ellipse cx="1.1" cy="-.8" rx="{f(r * 0.4)}" ry="{f(r * 0.26)}" transform="rotate(-25)" fill="{VIO_HI}"/></g>')
    for (x, y, r) in TC:
        a(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r + 4.5)}" fill="url(#hC)" opacity=".55"/>'
          f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{CYAN}"/>'
          f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * 0.45)}" fill="#E9FDFF"/>')
    # immune synapses: bright bars in the cleft between docked T cells and tumour cells
    for k, d in enumerate(bars):
        a(f'<path class="sy" style="animation-delay:{-0.7 * k:.1f}s" d="{d}" stroke="#F2FEFF" stroke-width="1.3" stroke-linecap="round"/>')

    # hub
    a(f'<path d="M0 -3.2L3.2 0L0 3.2L-3.2 0Z" fill="{CYAN_HI}"/>')

    # leading edge + pointer (over the cells)
    a(f'<g transform="rotate({f(TH0)})"><g class="sw">')
    a(f'<path d="M0 -6V-{R_SCOPE}" stroke="url(#lead)" stroke-width="1.3" stroke-linecap="round"/>')
    a(f'<path d="{arc(R_OUT, -34, 0)}" stroke="{CYAN}" stroke-opacity=".35" stroke-width="2" fill="none"/>')
    a(f'<path d="{arc(R_OUT, -12, 0)}" stroke="{CYAN_HI}" stroke-width="2" fill="none"/>')
    a(f'<path d="M0 -{R_OUT + 3}l-3.8 -7h7.6z" fill="{CYAN_HI}"/>')
    a("</g></g>")

    # bezel rings
    a(f'<circle r="{R_SCOPE}" fill="none" stroke="{CYAN}" stroke-opacity=".7" stroke-width="1"/>')
    a(f'<circle r="{R_BAND}" fill="none" stroke="{CYAN}" stroke-opacity=".32" stroke-width="1"/>')
    a(f'<circle r="{R_OUT}" fill="none" stroke="{CYAN}" stroke-opacity=".5" stroke-width="1"/>')
    # ticks (dash trick)
    rm = R_OUT - 1.75
    per = 2 * math.pi * rm / 120
    a('<g class="tk">')
    a(f'<circle r="{f(rm)}" fill="none" stroke="{CYAN}" stroke-opacity=".55" stroke-width="3.5" '
      f'stroke-dasharray=".6 {per - 0.6:.4f}" stroke-dashoffset=".3"/>')
    rm2 = R_OUT - 3
    per2 = 2 * math.pi * rm2 / 24
    a(f'<circle r="{f(rm2)}" fill="none" stroke="{CYAN_HI}" stroke-opacity=".9" stroke-width="6" '
      f'stroke-dasharray=".9 {per2 - 0.9:.4f}" stroke-dashoffset=".45"/>')
    a("</g>")
    # chevrons at the cardinals + dotted arcs
    rmid = (R_SCOPE + R_BAND) / 2
    for i in range(4):
        c = 90 * i
        tip = P(rmid, c + 2.4)
        b1 = P(rmid + 3.4, c - 1.4)
        b2 = P(rmid - 3.4, c - 1.4)
        a(f'<path d="M{f(tip[0])} {f(tip[1])}L{f(b1[0])} {f(b1[1])}L{f(b2[0])} {f(b2[1])}Z" fill="{CYAN}" fill-opacity=".85"/>')
    words = ["OBSERVE", "MODEL", "PERTURB", "VALIDATE"]
    dots = []
    for i, wd in enumerate(words):
        half = math.degrees((len(wd) * 7.2 + (len(wd) - 1) * 3) / 2 / rmid)
        c = 90 * i + 45
        dots.append(arc(rmid, 90 * i + 7, c - half - 5))
        dots.append(arc(rmid, c + half + 5, 90 * (i + 1) - 7))
    a(f'<path d="{"".join(dots)}" stroke="{CYAN}" stroke-opacity=".5" stroke-width="1" stroke-dasharray=".1 3.9" stroke-linecap="round" fill="none"/>')
    for i, wd in enumerate(words):
        on = " on" if i == 0 else ""
        delay = (((90 * i - TH0) % 360) / 360 * T) - T
        common = 'font-size="12" letter-spacing="3" text-anchor="middle"'
        tp = f'<textPath xlink:href="#w{i}" startOffset="50%">{wd}</textPath>'
        a(f'<text {common} class="m" fill="#7C93BD">{tp}</text>')
        a(f'<text {common} class="m ph{on}" style="animation-delay:{delay:.2f}s" font-weight="600" fill="#E9FDFF">{tp}</text>')
    a("</g>")

    # scan line inside the frame
    a(f'<g clip-path="url(#fc)"><g transform="translate({x1} {y1})"><g class="sc">'
      f'<rect y="-26" width="{2 * FRAME}" height="26" fill="url(#st)"/>'
      f'<rect y="-.4" width="{2 * FRAME}" height=".8" fill="url(#sl)"/></g></g></g>')

    a("</g>")
    # panel border
    a('<rect x=".5" y=".5" width="879" height="359" rx="15.5" fill="none" stroke="url(#edge)" stroke-width="1"/>')
    a("</svg>")
    return "\n".join(o) + "\n"


def build(out_dir) -> list:
    path = os.path.join(str(out_dir), "hero.svg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(build_svg())
    return ["hero.svg"]


if __name__ == "__main__":
    print(build(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "hud")))
