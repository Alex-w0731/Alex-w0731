"""Research radar: five directions being scanned, each with methods to evaluate.

A sonar-style display, not a chart: blip positions carry no quantitative meaning.
"""
from __future__ import annotations

import math

from theme import MW, T, W, document, panel, text

H = 316
CX, CY, R = 172, 164, 112
CATALOGUE_SIZE = 97     # entries in research/catalogue.json

DIRECTIONS = [
    # title, methods, colour, (angle in degrees, radius fraction) of the blip
    ("Spatial context & treatment vulnerability", "SpatialData · BANKSY · LIANA+ · MultiNicheNet", "cyan", (-58, 0.62)),
    ("Resistant states & lineage dynamics", "CellRank · moscot · Cassiopeia · SCENIC+", "blue", (18, 0.80)),
    ("Perturbation models & experimental choices", "SCEPTRE · State · linear baselines · cell-eval", "magenta", (96, 0.50)),
    ("Geometry & effective delivery", "scadnano · oxDNA · Ax", "amber", (168, 0.74)),
    ("Morphology, transcription & function", "CellProfiler · Pycytominer · QuPath · COSMOS", "green", (236, 0.58)),
]


def _scope(cx: float, cy: float, r: float) -> str:
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r * f:g}" fill="none" stroke="{T["line2"]}" stroke-width="1"/>' for f in (0.33, 0.66, 1.0))
    cross = f'<path d="M{cx - r} {cy}h{2 * r}M{cx} {cy - r}v{2 * r}" stroke="{T["line2"]}" stroke-width="1"/>'
    ticks = "".join(
        f'<line x1="{cx + (r - 5) * math.cos(math.radians(a)):.1f}" y1="{cy + (r - 5) * math.sin(math.radians(a)):.1f}" '
        f'x2="{cx + r * math.cos(math.radians(a)):.1f}" y2="{cy + r * math.sin(math.radians(a)):.1f}" stroke="{T["low"]}" stroke-width="1"/>'
        for a in range(0, 360, 15)
    )
    a = math.radians(-38)
    wedge = (
        f'<g class="sweep"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none"/>'
        f'<path d="M{cx} {cy}L{cx + r} {cy}A{r} {r} 0 0 0 {cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}Z" fill="url(#sweepG)"/>'
        f'<line x1="{cx}" y1="{cy}" x2="{cx + r}" y2="{cy}" stroke="{T["cyan2"]}" stroke-width="1.6" stroke-linecap="round"/></g>'
    )
    out = [f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{T["bg0"]}" fill-opacity=".55"/>{rings}{cross}{ticks}{wedge}<circle cx="{cx}" cy="{cy}" r="2.5" fill="{T["cyan2"]}"/>']
    for i, (_, _, color, (ang, frac)) in enumerate(DIRECTIONS):
        c = T[color]
        bx = cx + r * frac * math.cos(math.radians(ang))
        by = cy + r * frac * math.sin(math.radians(ang))
        halo = "haloM" if color == "magenta" else "halo"
        out.append(
            f'  <circle cx="{bx:.1f}" cy="{by:.1f}" r="13" fill="url(#{halo})"/>'
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4.2" fill="{c}" class="pulse" style="animation-delay:{i * 0.6:g}s"/>'
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="8.5" fill="none" stroke="{c}" stroke-opacity=".5"/>'
            + text(bx + 12, by - 9, f"0{i + 1}", size=10.5, cls="mono", extra=f' fill="{c}"')
        )
    return "\n".join(out)


SWEEP_DEFS = (
    f'<linearGradient id="sweepG" x1="1" y1=".5" x2=".55" y2="0"><stop offset="0" stop-color="{T["cyan"]}" stop-opacity=".42"/>'
    f'<stop offset="1" stop-color="{T["cyan"]}" stop-opacity="0"/></linearGradient>'
)
SWEEP_STYLE = ".sweep { transform-box: fill-box; transform-origin: center; animation: spin 9s linear infinite; }\n"
TITLE = "Research radar: " + "; ".join(f"{t} ({m})" for t, m, _, _ in DIRECTIONS)


def build_mobile_svg() -> str:
    """Narrow-screen layout: the scope on top, the five directions listed below."""
    cx, cy, r = MW // 2, 162, 104
    y0, step = 318, 50
    h = y0 + len(DIRECTIONS) * step + 44
    out = [panel(MW, h, accent="violet")]
    out.append("  " + text(26, 36, "RESEARCH RADAR", size=12, cls="mono low caps"))
    out.append(_scope(cx, cy, r))
    for i, (title, methods, color, _) in enumerate(DIRECTIONS):
        c = T[color]
        y = y0 + i * step
        out.append(
            f'  <rect x="24" y="{y - 14}" width="28" height="22" rx="6" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".7"/>'
            + text(38, y + 1.5, f"0{i + 1}", size=12, cls="mono b", anchor="middle", extra=f' fill="{c}"')
            + text(64, y + 1, title, size=15, cls="sans sb hi")
            + text(64, y + 21, methods, size=11.5, cls="mono low")
        )
    yb = y0 + len(DIRECTIONS) * step + 10
    out.append(
        f'  <text x="24" y="{yb + 8}" font-size="30" class="mono b" fill="url(#acc)">{CATALOGUE_SIZE}</text>'
        + text(72, yb - 3, "PUBLIC RESOURCES", size=11, cls="mono mid caps")
        + text(72, yb + 11, "MAPPED IN THE CATALOGUE", size=11, cls="mono low caps")
    )
    return document(MW, h, "\n".join(out), TITLE, extra_defs=SWEEP_DEFS, extra_style=SWEEP_STYLE)


def build_svg() -> str:
    out = [panel(W, H, accent="violet")]
    out.append("  " + text(28, 34, "RESEARCH RADAR", size=12, cls="mono low caps"))
    out.append("  " + text(W - 28, 34, "A LEARNING ROADMAP, NOT A LIST OF RESULTS", size=12, cls="mono low caps", anchor="end"))
    out.append(_scope(CX, CY, R))
    y0, step = 76, 46
    for i, (title, methods, color, _) in enumerate(DIRECTIONS):
        c = T[color]
        y = y0 + i * step
        x = 336
        out.append(
            f'  <rect x="{x}" y="{y - 13}" width="26" height="20" rx="6" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".7"/>'
            + text(x + 13, y + 1.5, f"0{i + 1}", size=11.5, cls="mono b", anchor="middle", extra=f' fill="{c}"')
            + text(x + 40, y + 1, title, size=14.5, cls="sans sb hi")
            + text(x + 40, y + 20, methods, size=11.5, cls="mono low")
        )
    # catalogue tile: the number of entries in research/catalogue.json (kept in sync by hand)
    tx, ty, tw, th = 722, 74, 130, 168
    out.append(
        f'  <rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="12" fill="{T["bg0"]}" fill-opacity=".5" stroke="{T["line2"]}"/>'
        + text(tx + tw / 2, ty + 30, "CATALOGUE", size=10.5, cls="mono low caps", anchor="middle")
        + f'<text x="{tx + tw / 2:g}" y="{ty + 96}" font-size="56" class="mono b" text-anchor="middle" fill="url(#acc)">{CATALOGUE_SIZE}</text>'
        + text(tx + tw / 2, ty + 124, "PUBLIC", size=10.5, cls="mono mid caps", anchor="middle")
        + text(tx + tw / 2, ty + 140, "RESOURCES", size=10.5, cls="mono mid caps", anchor="middle")
        + text(tx + tw / 2, ty + 156, "MAPPED", size=10.5, cls="mono mid caps", anchor="middle")
    )
    return document(W, H, "\n".join(out), TITLE, extra_defs=SWEEP_DEFS, extra_style=SWEEP_STYLE)


def build(out_dir) -> list[str]:
    from theme import write

    write(f"{out_dir}/radar.svg", build_svg())
    write(f"{out_dir}/m/radar.svg", build_mobile_svg())
    return ["radar.svg", "m/radar.svg"]
