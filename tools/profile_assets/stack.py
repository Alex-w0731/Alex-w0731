"""Tools and methods: what is used to compute, and what is used to validate."""
from __future__ import annotations

from theme import MW, T, W, chip_row, document, panel, text

COMPUTE = ["R", "Python", "Seurat", "Scanpy", "CellChat", "CytoTRACE2", "Palantir", "pySCENIC",
           "bulk RNA-seq", "scRNA-seq", "ChIP-seq", "survival analysis", "pathway enrichment"]
VALIDATE = ["CRISPR-Cas9 screens", "qRT-PCR", "Western blot", "Co-IP", "flow cytometry", "cell culture",
            "xenograft models", "H&E · IHC · IF", "confocal microscopy", "pathology-image analysis"]

COL_W = 392


def _column(x: float, title: str, caption: str, items: list[str], color: str, icon: str, dy: float = 0,
            chip_size: float = 12, chip_h: float = 24) -> tuple[str, float]:
    c = T[color]
    out = [
        f'<g transform="translate(0 {dy:g})"><rect x="{x}" y="30" width="30" height="30" rx="8" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".7"/>{icon}</g>',
        text(x + 42, 44 + dy, title, size=15, cls="mono b caps", extra=f' fill="{c}"'),
        text(x + 42, 61 + dy, caption, size=12.5, cls="sans mid"),
    ]
    row, _, last_y = chip_row(x, 80 + dy, [(i, color) for i in items], size=chip_size, height=chip_h, gap=8, max_width=COL_W)
    out.append(row)
    return "  " + "\n  ".join(out), last_y + chip_h


def build_svg() -> str:
    xl, xr = 30, W - 30 - COL_W
    cy = T["cyan"]
    mg = T["magenta"]
    icon_l = (  # terminal prompt
        f'<path d="M{xl + 9} 39l6 6l-6 6M{xl + 17} 52h6" fill="none" stroke="{cy}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    icon_r = (  # flask
        f'<path d="M{xr + 12} 37h6M{xr + 13} 37v6l-5 9a1.6 1.6 0 0 0 1.4 2.4h11.2a1.6 1.6 0 0 0 1.4-2.4l-5-9v-6" fill="none" stroke="{mg}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
    )
    left, bottom_l = _column(xl, "COMPUTE", "tumor omics, cell states, reproducible analysis", COMPUTE, "cyan", icon_l)
    right, bottom_r = _column(xr, "VALIDATE", "functional genomics, tumor models, quantitative imaging", VALIDATE, "magenta", icon_r)
    height = int(max(bottom_l, bottom_r) + 28)
    divider = f'  <line x1="{W / 2}" y1="30" x2="{W / 2}" y2="{height - 28}" stroke="{T["line2"]}" stroke-dasharray="2 6"/>'
    body = "\n".join([panel(W, height), left, divider, right])
    title = "Tools and methods. Compute: " + ", ".join(COMPUTE) + ". Validate: " + ", ".join(VALIDATE) + "."
    return document(W, height, body, title)


def build_mobile_svg() -> str:
    """Narrow-screen layout: the two blocks stacked, with larger chips."""
    x = 24
    cy, mg = T["cyan"], T["magenta"]
    icon_l = f'<path d="M{x + 9} 39l6 6l-6 6M{x + 17} 52h6" fill="none" stroke="{cy}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    icon_r = f'<path d="M{x + 12} 37h6M{x + 13} 37v6l-5 9a1.6 1.6 0 0 0 1.4 2.4h11.2a1.6 1.6 0 0 0 1.4-2.4l-5-9v-6" fill="none" stroke="{mg}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'
    top, bottom_top = _column(x, "COMPUTE", "tumor omics, cell states, reproducible analysis", COMPUTE, "cyan", icon_l, chip_size=13, chip_h=26)
    dy = bottom_top + 6
    bottom, bottom_end = _column(x, "VALIDATE", "functional genomics, tumor models, imaging", VALIDATE, "magenta", icon_r, dy=dy, chip_size=13, chip_h=26)
    height = int(bottom_end + 28)
    divider = f'  <line x1="{x}" y1="{dy + 12:g}" x2="{MW - x}" y2="{dy + 12:g}" stroke="{T["line2"]}" stroke-dasharray="2 6"/>'
    body = "\n".join([panel(MW, height), top, divider, bottom])
    title = "Tools and methods. Compute: " + ", ".join(COMPUTE) + ". Validate: " + ", ".join(VALIDATE) + "."
    return document(MW, height, body, title)


def build(out_dir) -> list[str]:
    from theme import write

    write(f"{out_dir}/stack.svg", build_svg())
    write(f"{out_dir}/m/stack.svg", build_mobile_svg())
    return ["stack.svg", "m/stack.svg"]
