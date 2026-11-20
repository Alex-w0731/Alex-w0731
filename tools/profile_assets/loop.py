"""The research loop: observe -> model -> perturb -> validate, and back with new questions."""
from __future__ import annotations

from theme import T, W, document, panel, text

H = 236
Y = 96          # node centre line
R = 30          # node ring radius
XS = [128, 336, 544, 752]

STAGES = [
    ("OBSERVE", "tumor & clinical data", "cyan"),
    ("MODEL", "single-cell & spatial patterns", "blue"),
    ("PERTURB", "functional genomics", "magenta"),
    ("VALIDATE", "mechanisms & targets", "green"),
]


def _icon(kind: str, cx: float, cy: float, c: str) -> str:
    s = f'fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "OBSERVE":      # scope: ring, crosshair ticks, centre
        return (
            f'<g {s}><circle cx="{cx}" cy="{cy}" r="11"/>'
            f'<path d="M{cx} {cy - 17}v6M{cx} {cy + 11}v6M{cx - 17} {cy}h6M{cx + 11} {cy}h6"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="2.6" fill="{c}"/>'
        )
    if kind == "MODEL":        # small graph of cell states
        pts = [(-12, 7), (-4, -10), (9, -4), (11, 10), (-1, 3)]
        edges = [(0, 4), (1, 4), (2, 4), (3, 4), (1, 2)]
        lines = "".join(f'M{cx + pts[a][0]} {cy + pts[a][1]}L{cx + pts[b][0]} {cy + pts[b][1]}' for a, b in edges)
        dots = "".join(f'<circle cx="{cx + x}" cy="{cy + y}" r="2.8" fill="{c}"/>' for x, y in pts)
        return f'<path d="{lines}" {s} stroke-opacity=".7"/>{dots}'
    if kind == "PERTURB":      # double strand with a targeted break
        return (
            f'<g {s}><path d="M{cx - 16} {cy - 5}H{cx - 4}M{cx + 4} {cy - 5}H{cx + 16}"/>'
            f'<path d="M{cx - 16} {cy + 5}H{cx - 4}M{cx + 4} {cy + 5}H{cx + 16}"/>'
            f'<path d="M{cx - 11} {cy - 5}v10M{cx + 11} {cy - 5}v10" stroke-opacity=".55"/></g>'
            f'<path d="M{cx + 2} {cy - 15}l-5 12h6l-5 12" fill="none" stroke="{T["amber"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    return (                   # VALIDATE: check inside a hexagon
        f'<g {s}><path d="M{cx} {cy - 15}l13 7.5v15l-13 7.5l-13-7.5v-15z"/>'
        f'<path d="M{cx - 6} {cy}l4.5 4.5l8-9" stroke-width="2"/></g>'
    )


def build_svg() -> str:
    parts = [panel(W, H)]
    parts.append("  " + text(28, 34, "RESEARCH LOOP", size=12, cls="mono low caps"))
    parts.append("  " + text(W - 28, 34, "FROM A PATTERN TO A TESTED MECHANISM", size=12, cls="mono low caps", anchor="end"))

    # connectors between stages
    for i in range(len(XS) - 1):
        x0, x1 = XS[i] + R + 10, XS[i + 1] - R - 10
        c = T[STAGES[i][2]]
        parts.append(
            f'  <line x1="{x0}" y1="{Y}" x2="{x1}" y2="{Y}" stroke="{T["line2"]}" stroke-width="1"/>'
            f'<line x1="{x0}" y1="{Y}" x2="{x1}" y2="{Y}" stroke="{c}" stroke-width="1.8" class="flow" stroke-linecap="round"/>'
            f'<path d="M{x1 - 7} {Y - 5}l7 5l-7 5" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
        )

    # return path: validate -> observe ("new questions")
    y_ret = 204
    xa, xb = XS[-1], XS[0]
    parts.append(
        f'  <path d="M{xa} {Y + R + 62}V{y_ret - 10}a10 10 0 0 1 -10 10H{xb + 10}a10 10 0 0 1 -10 -10V{Y + R + 62}" '
        f'fill="none" stroke="{T["line2"]}" stroke-width="1"/>'
        f'<path d="M{xa} {Y + R + 62}V{y_ret - 10}a10 10 0 0 1 -10 10H{xb + 10}a10 10 0 0 1 -10 -10V{Y + R + 62}" '
        f'fill="none" stroke="{T["violet"]}" stroke-width="1.4" class="flow-slow" stroke-linecap="round" opacity=".9"/>'
        f'<path d="M{xb - 5} {Y + R + 69}l5 -7l5 7" fill="none" stroke="{T["violet"]}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    label = "NEW QUESTIONS"
    lw = len(label) * 7.6 + 24
    parts.append(
        f'  <rect x="{W / 2 - lw / 2:g}" y="{y_ret - 10}" width="{lw:g}" height="20" rx="10" fill="{T["bg2"]}" stroke="{T["line2"]}"/>'
        + text(W / 2, y_ret + 4, label, size=11, cls="mono vi caps", anchor="middle")
    )

    # stage nodes
    for i, (name, caption, color) in enumerate(STAGES):
        cx, c = XS[i], T[color]
        halo = "haloM" if color == "magenta" else "halo"
        delay = f' style="animation-delay:{i * 0.8:g}s"'
        parts.append(
            f'  <circle cx="{cx}" cy="{Y}" r="{R * 1.9:g}" fill="url(#{halo})" class="breathe"{delay}/>'
            f'<circle cx="{cx}" cy="{Y}" r="{R}" fill="{T["bg2"]}" stroke="{c}" stroke-width="1.5"/>'
            f'<circle cx="{cx}" cy="{Y}" r="{R + 7}" fill="none" stroke="{c}" stroke-opacity=".3" stroke-dasharray="3 7" class="spin"/>'
            + _icon(name, cx, Y, c)
        )
        parts.append(
            "  "
            + text(cx, Y + R + 30, name, size=15, cls="mono b caps", anchor="middle", extra=f' fill="{c}"')
            + text(cx, Y + R + 50, caption, size=13, cls="sans mid", anchor="middle")
        )
        parts.append("  " + text(cx - R - 4, Y - R + 2, f"0{i + 1}", size=11, cls="mono low", anchor="end"))

    title = "Research loop: observe tumor and clinical data, model single-cell and spatial patterns, perturb with functional genomics, validate mechanisms and targets, then return with new questions."
    return document(W, H, "\n".join(parts), title)


def build(out_dir) -> list[str]:
    from theme import write

    write(f"{out_dir}/loop.svg", build_svg())
    return ["loop.svg"]
