"""Design tokens and drawing helpers shared by every profile graphic.

All graphics are self-contained SVG files embedded in the README through <img>, so:
no scripts, no external fonts or images, system font stacks only, CSS animations that are
switched off under `prefers-reduced-motion`, and a complete picture at t = 0.

One viewBox unit is about one CSS pixel on a desktop README (content width ~846 px for an
880-unit-wide graphic), so keep readable text at 13 units or more.
"""
from __future__ import annotations

from xml.sax.saxutils import escape

# ----------------------------------------------------------------------------- tokens
T = {
    # surfaces
    "bg0": "#04060d",      # deepest background
    "bg1": "#070b16",      # panel fill, top
    "bg2": "#0b1222",      # panel fill, bottom / raised surfaces
    "line": "#18233a",     # hairlines, grid
    "line2": "#24365a",    # stronger outlines
    # text
    "hi": "#eaf2ff",
    "mid": "#a3b3cc",
    "low": "#62748f",
    # accents
    "cyan": "#2ce8ff",
    "cyan2": "#9ff4ff",
    "blue": "#60a5fa",
    "violet": "#a78bfa",
    "magenta": "#ff5cb8",
    "amber": "#fbbf24",
    "green": "#34d399",
}

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

W = 880                 # full-width graphics
MW = 440                # narrow-screen variants (served through <picture> below 640 px)
MONO_ADVANCE = 0.62     # conservative glyph advance (em) used to size chips and rules


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def mono_width(text: str, size: float, spacing: float = 0.0) -> float:
    """Estimated rendered width of monospace text (slightly generous on purpose)."""
    return len(text) * (size * MONO_ADVANCE + spacing)


# ----------------------------------------------------------------------------- document

BASE_STYLE = f"""
    .mono {{ font-family: {MONO}; }}
    .sans {{ font-family: {SANS}; }}
    .hi {{ fill: {T['hi']}; }} .mid {{ fill: {T['mid']}; }} .low {{ fill: {T['low']}; }}
    .cy {{ fill: {T['cyan']}; }} .cy2 {{ fill: {T['cyan2']}; }} .mg {{ fill: {T['magenta']}; }}
    .vi {{ fill: {T['violet']}; }} .am {{ fill: {T['amber']}; }} .gr {{ fill: {T['green']}; }} .bl {{ fill: {T['blue']}; }}
    .caps {{ letter-spacing: 0.16em; }}
    .tight {{ letter-spacing: 0.04em; }}
    .b {{ font-weight: 700; }} .sb {{ font-weight: 600; }}
    .s-cy {{ stroke: {T['cyan']}; }} .s-mg {{ stroke: {T['magenta']}; }} .s-vi {{ stroke: {T['violet']}; }}
    .s-line {{ stroke: {T['line']}; }} .s-line2 {{ stroke: {T['line2']}; }} .s-low {{ stroke: {T['low']}; }}
    .nf {{ fill: none; }}
    @keyframes pulse {{ 0%, 100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
    @keyframes breathe {{ 0%, 100% {{ opacity: .55; }} 50% {{ opacity: 1; }} }}
    @keyframes blink {{ 0%, 55% {{ opacity: 1; }} 56%, 100% {{ opacity: 0; }} }}
    @keyframes dash {{ to {{ stroke-dashoffset: -64; }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes spinr {{ to {{ transform: rotate(-360deg); }} }}
    @keyframes floaty {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-4px); }} }}
    .pulse {{ animation: pulse 3.2s ease-in-out infinite; }}
    .breathe {{ animation: breathe 4.8s ease-in-out infinite; }}
    .blink {{ animation: blink 1.2s steps(1) infinite; }}
    .flow {{ stroke-dasharray: 6 10; animation: dash 2.4s linear infinite; }}
    .flow-slow {{ stroke-dasharray: 2 14; animation: dash 5s linear infinite; }}
    .spin {{ transform-box: fill-box; transform-origin: center; animation: spin 24s linear infinite; }}
    .spinr {{ transform-box: fill-box; transform-origin: center; animation: spinr 36s linear infinite; }}
    .floaty {{ animation: floaty 6s ease-in-out infinite; }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
"""

BASE_DEFS = f"""
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{T['bg1']}"/><stop offset="1" stop-color="{T['bg2']}"/>
    </linearGradient>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{T['cyan']}"/><stop offset=".55" stop-color="{T['violet']}"/><stop offset="1" stop-color="{T['magenta']}"/>
    </linearGradient>
    <linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{T['cyan']}" stop-opacity=".9"/><stop offset="1" stop-color="{T['cyan']}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="halo" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{T['cyan']}" stop-opacity=".35"/><stop offset="1" stop-color="{T['cyan']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="haloM" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{T['magenta']}" stop-opacity=".32"/><stop offset="1" stop-color="{T['magenta']}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{T['line']}" stroke-width="1" opacity=".55"/>
    </pattern>
    <pattern id="dots" width="12" height="12" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{T['line2']}" opacity=".7"/>
    </pattern>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
"""


def document(width: int, height: int, body: str, title: str, *, extra_defs: str = "", extra_style: str = "") -> str:
    """Wrap a body in a complete, accessible SVG document."""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="{esc(title)}">\n'
        f"  <title>{esc(title)}</title>\n"
        f"  <defs>{BASE_DEFS}{extra_defs}  </defs>\n"
        f"  <style>{BASE_STYLE}{extra_style}  </style>\n"
        f"{body}\n</svg>\n"
    )


# ----------------------------------------------------------------------------- primitives

def panel(width: int, height: int, *, rx: int = 14, grid: bool = True, accent: str = "cyan") -> str:
    """Dark rounded panel with a faint grid, hairline border and corner brackets."""
    c = T[accent]
    g = f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="{rx}" fill="url(#grid)"/>' if grid else ""
    b = 16  # bracket arm length
    m = 9   # bracket inset
    brackets = (
        f'<path d="M{m} {m + b}V{m + 5}a5 5 0 0 1 5-5H{m + b}" /><path d="M{width - m - b} {m}H{width - m - 5}a5 5 0 0 1 5 5V{m + b}" />'
        f'<path d="M{width - m} {height - m - b}V{height - m - 5}a5 5 0 0 1-5 5H{width - m - b}" /><path d="M{m + b} {height - m}H{m + 5}a5 5 0 0 1-5-5V{height - m - b}" />'
    )
    return (
        f'  <rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="{rx}" fill="url(#bg)" stroke="{T["line2"]}"/>\n'
        f"  {g}\n"
        f'  <g fill="none" stroke="{c}" stroke-width="1.4" stroke-linecap="round" opacity=".75">{brackets}</g>'
    )


def text(x: float, y: float, content: str, *, size: float = 14, cls: str = "mono mid", anchor: str = "start", extra: str = "") -> str:
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" class="{cls}"{a}{extra}>{esc(content)}</text>'


def chip(x: float, y: float, label: str, *, color: str = "cyan", size: float = 13, pad: float = 10, height: float = 24, filled: bool = False) -> tuple[str, float]:
    """Rounded label chip. Returns (svg, width) so callers can lay chips out in a row."""
    c = T[color]
    w = mono_width(label, size, 0.6) + pad * 2
    fill = f'fill="{c}" fill-opacity=".12"' if filled else 'fill="none"'
    svg = (
        f'<g><rect x="{x:g}" y="{y:g}" width="{w:.1f}" height="{height:g}" rx="{height / 2:g}" {fill} stroke="{c}" stroke-opacity=".55"/>'
        f'<text x="{x + w / 2:.1f}" y="{y + height / 2 + size * 0.36:.1f}" font-size="{size:g}" class="mono" fill="{c}" text-anchor="middle" letter-spacing=".6">{esc(label)}</text></g>'
    )
    return svg, w


def chip_row(x: float, y: float, labels: list[tuple[str, str]], *, gap: float = 8, max_width: float | None = None, **kw) -> tuple[str, float, float]:
    """Lay out chips left to right, wrapping at max_width. Returns (svg, last_x, last_y)."""
    out, cx, cy = [], x, y
    height = kw.get("height", 24)
    for label, color in labels:
        svg, w = chip(cx, cy, label, color=color, **kw)
        if max_width is not None and cx + w > x + max_width and cx > x:
            cx, cy = x, cy + height + gap
            svg, w = chip(cx, cy, label, color=color, **kw)
        out.append(svg)
        cx += w + gap
    return "\n  ".join(out), cx, cy


def node(cx: float, cy: float, r: float, *, color: str = "cyan", ring: bool = True, cls: str = "") -> str:
    """A glowing cell-like node: halo, body and nucleus."""
    c = T[color]
    halo = "haloM" if color == "magenta" else "halo"
    ringed = f'<circle cx="{cx:g}" cy="{cy:g}" r="{r + 5:g}" fill="none" stroke="{c}" stroke-opacity=".28"/>' if ring else ""
    k = f' class="{cls}"' if cls else ""
    return (
        f'<g{k}><circle cx="{cx:g}" cy="{cy:g}" r="{r * 2.4:g}" fill="url(#{halo})"/>{ringed}'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="{c}" fill-opacity=".16" stroke="{c}" stroke-width="1.3"/>'
        f'<circle cx="{cx:g}" cy="{cy:g}" r="{max(r * 0.32, 1.6):g}" fill="{c}"/></g>'
    )


def hairline(x1: float, y1: float, x2: float, y2: float, *, color: str = "line2", width: float = 1, cls: str = "", opacity: float = 1) -> str:
    k = f' class="{cls}"' if cls else ""
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="{T[color]}" stroke-width="{width:g}" opacity="{opacity:g}"{k}/>'


def write(path, svg: str) -> None:
    from pathlib import Path

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(svg, encoding="utf-8")
