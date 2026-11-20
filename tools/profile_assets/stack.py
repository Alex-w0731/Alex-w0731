"""Tools and methods: what is used to compute, and what is used to validate."""
from __future__ import annotations

from theme import T, W, chip_row, document, panel, text

COMPUTE = ["R", "Python", "Seurat", "Scanpy", "CellChat", "CytoTRACE2", "Palantir", "pySCENIC",
           "bulk RNA-seq", "scRNA-seq", "ChIP-seq", "survival analysis", "pathway enrichment"]
VALIDATE = ["CRISPR-Cas9 screens", "qRT-PCR", "Western blot", "Co-IP", "flow cytometry", "cell culture",
            "xenograft models", "H&E · IHC · IF", "confocal microscopy", "pathology-image analysis"]

COL_W = 392


def _column(x: float, title: str, caption: str, items: list[str], color: str, icon: str) -> tuple[str, float]:
    c = T[color]
    out = [
        f'<rect x="{x}" y="30" width="30" height="30" rx="8" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".7"/>{icon}',
        text(x + 42, 44, title, size=15, cls="mono b caps", extra=f' fill="{c}"'),
        text(x + 42, 61, caption, size=12.5, cls="sans mid"),
    ]
    row, _, last_y = chip_row(x, 80, [(i, color) for i in items], size=12, height=24, gap=8, max_width=COL_W)
    out.append(row)
    return "  " + "\n  ".join(out), last_y + 24


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


def build(out_dir) -> list[str]:
    from theme import write

    write(f"{out_dir}/stack.svg", build_svg())
    return ["stack.svg"]
