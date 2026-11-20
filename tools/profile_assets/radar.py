"""Research radar: five directions being scanned, each with methods to evaluate.

A sonar-style display, not a chart: blip positions carry no quantitative meaning.
"""
from __future__ import annotations

import math

from theme import T, W, document, panel, text

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


def build_svg() -> str:
    out = [panel(W, H, accent="violet")]
    out.append("  " + text(28, 34, "RESEARCH RADAR", size=12, cls="mono low caps"))
    out.append("  " + text(W - 28, 34, "A LEARNING ROADMAP, NOT A LIST OF RESULTS", size=12, cls="mono low caps", anchor="end"))
    # scope
    rings = "".join(f'<circle cx="{CX}" cy="{CY}" r="{R * f:g}" fill="none" stroke="{T["line2"]}" stroke-width="1"/>' for f in (0.33, 0.66, 1.0))
    cross = f'<path d="M{CX - R} {CY}h{2 * R}M{CX} {CY - R}v{2 * R}" stroke="{T["line2"]}" stroke-width="1"/>'
    ticks = "".join(
        f'<line x1="{CX + (R - 5) * math.cos(math.radians(a)):.1f}" y1="{CY + (R - 5) * math.sin(math.radians(a)):.1f}" '
        f'x2="{CX + R * math.cos(math.radians(a)):.1f}" y2="{CY + R * math.sin(math.radians(a)):.1f}" stroke="{T["low"]}" stroke-width="1"/>'
        for a in range(0, 360, 15)
    )
    # sweep wedge (rotates around the scope centre: the transparent circle fixes the bounding box)
    a = math.radians(-38)
    wedge = (
        f'<g class="sweep"><circle cx="{CX}" cy="{CY}" r="{R}" fill="none"/>'
        f'<path d="M{CX} {CY}L{CX + R} {CY}A{R} {R} 0 0 0 {CX + R * math.cos(a):.1f} {CY + R * math.sin(a):.1f}Z" fill="url(#sweepG)"/>'
        f'<line x1="{CX}" y1="{CY}" x2="{CX + R}" y2="{CY}" stroke="{T["cyan2"]}" stroke-width="1.6" stroke-linecap="round"/></g>'
    )
    out.append(f'  <circle cx="{CX}" cy="{CY}" r="{R}" fill="{T["bg0"]}" fill-opacity=".55"/>{rings}{cross}{ticks}{wedge}<circle cx="{CX}" cy="{CY}" r="2.5" fill="{T["cyan2"]}"/>')
    # blips and list
    y0, step = 76, 46
    for i, (title, methods, color, (ang, frac)) in enumerate(DIRECTIONS):
        c = T[color]
        bx = CX + R * frac * math.cos(math.radians(ang))
        by = CY + R * frac * math.sin(math.radians(ang))
        halo = "haloM" if color == "magenta" else "halo"
        out.append(
            f'  <circle cx="{bx:.1f}" cy="{by:.1f}" r="13" fill="url(#{halo})"/>'
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4.2" fill="{c}" class="pulse" style="animation-delay:{i * 0.6:g}s"/>'
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="8.5" fill="none" stroke="{c}" stroke-opacity=".5"/>'
            + text(bx + 12, by - 9, f"0{i + 1}", size=10.5, cls="mono", extra=f' fill="{c}"')
        )
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
    extra_defs = (
        f'<linearGradient id="sweepG" x1="1" y1=".5" x2=".55" y2="0"><stop offset="0" stop-color="{T["cyan"]}" stop-opacity=".42"/>'
        f'<stop offset="1" stop-color="{T["cyan"]}" stop-opacity="0"/></linearGradient>'
    )
    extra_style = ".sweep { transform-box: fill-box; transform-origin: center; animation: spin 9s linear infinite; }\n"
    title = "Research radar: " + "; ".join(f"{t} ({m})" for t, m, _, _ in DIRECTIONS)
    return document(W, H, "\n".join(out), title, extra_defs=extra_defs, extra_style=extra_style)


def build(out_dir) -> list[str]:
    from theme import write

    write(f"{out_dir}/radar.svg", build_svg())
    return ["radar.svg"]
