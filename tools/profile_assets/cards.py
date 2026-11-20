"""Project cards (six schematic tiles) for the Selected work grid.

The drawings are schematics that say what kind of analysis a project contains. They are
not data: no axis values, no statistics, no results.
"""
from __future__ import annotations

from theme import T, document, panel, text

CW, CH = 432, 184


def _frame(index: str, label: str, lang: str, tagline: str, art: str, title: str, accent: str = "cyan") -> str:
    c = T[accent]
    lang_w = len(lang) * 7.4 + 18
    body = "\n".join([
        panel(CW, CH, rx=12, accent=accent),
        "  " + text(26, 36, index, size=14, cls="mono b", extra=f' fill="{c}" letter-spacing="1.2"')
        + text(52, 36, "/", size=14, cls="mono low")
        + text(68, 36, label, size=12.5, cls="mono mid caps"),
        f'  <rect x="{CW - 26 - lang_w:g}" y="22" width="{lang_w:g}" height="20" rx="10" fill="none" stroke="{T["line2"]}"/>'
        + text(CW - 26 - lang_w / 2, 36, lang, size=10.5, cls="mono low caps", anchor="middle"),
        art,
        "  " + text(26, CH - 22, tagline, size=11.5, cls="mono low caps"),
        f'  <rect x="{CW - 60}" y="{CH - 27}" width="34" height="2" rx="1" fill="{c}" class="pulse"/>',
    ])
    return document(CW, CH, body, title)


# ----------------------------------------------------------------------------- drawings

def art_multiomics() -> str:
    """Three stacked data layers (single-cell, spatial, bulk) tied together sample by sample."""
    out = []
    layers = [(58, "cyan", "scRNA-seq"), (88, "violet", "spatial"), (118, "magenta", "bulk")]
    x0 = 60
    for i, (y, color, name) in enumerate(layers):
        c = T[color]
        out.append(
            f'<path d="M{x0 + 34} {y - 12}h150l-34 24h-150z" fill="{c}" fill-opacity=".09" stroke="{c}" stroke-width="1.3" stroke-linejoin="round"/>'
        )
        for k, dx in enumerate((48, 86, 124, 158)):
            cls = ' class="pulse" style="animation-delay:%.1fs"' % (0.5 * k + 0.3 * i)
            out.append(f'<circle cx="{x0 + dx - (0 if k % 2 else 6)}" cy="{y + (3 if k % 2 else -3)}" r="2.6" fill="{c}"{cls}/>')
        out.append(text(x0 + 206, y + 4, name, size=12, cls="mono mid"))
    for dx in (48, 124):
        out.append(f'<line x1="{x0 + dx - 6}" y1="55" x2="{x0 + dx - 6}" y2="115" stroke="{T["low"]}" stroke-dasharray="2 4" stroke-width="1"/>')
    return "  " + "".join(out)


def art_multiscale() -> str:
    """Cells -> tissue spots -> cohort: the same biology read at three scales."""
    out = []
    cells = [(44, 70), (58, 92), (72, 64), (80, 104), (94, 82), (52, 112), (100, 60), (106, 108)]
    cols = ["cyan", "violet", "magenta", "cyan", "green", "violet", "cyan", "magenta"]
    for (x, y), col in zip(cells, cols):
        out.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{T[col]}" fill-opacity=".2" stroke="{T[col]}" stroke-width="1.2"/>')
    out.append(text(74, 138, "CELLS", size=10.5, cls="mono low caps", anchor="middle"))
    # tissue: hexagonally packed spots
    for r in range(4):
        for k in range(5):
            x = 176 + k * 16 + (8 if r % 2 else 0)
            y = 62 + r * 14
            col = T["cyan"] if (r + k) % 3 else T["magenta"]
            op = ".85" if (r * 5 + k) % 4 else ".35"
            out.append(f'<circle cx="{x}" cy="{y}" r="5.2" fill="{col}" fill-opacity="{op}"/>')
    out.append(text(212, 138, "TISSUE", size=10.5, cls="mono low caps", anchor="middle"))
    # cohort: one bar per patient
    for k, h in enumerate((30, 46, 22, 52, 38, 28)):
        x = 310 + k * 15
        out.append(f'<rect x="{x}" y="{112 - h}" width="9" height="{h}" rx="2" fill="{T["violet"]}" fill-opacity=".75"/>')
    out.append(f'<line x1="304" y1="112.5" x2="402" y2="112.5" stroke="{T["line2"]}"/>')
    out.append(text(353, 138, "COHORT", size=10.5, cls="mono low caps", anchor="middle"))
    for x in (130, 272):
        out.append(f'<path d="M{x} 86h18m-6 -5l6 5l-6 5" fill="none" stroke="{T["low"]}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')
    return "  " + "".join(out)


def art_survival() -> str:
    """Two Kaplan-Meier style step curves with censoring ticks (schematic, no values)."""
    out = [f'<path d="M58 52V124H330" fill="none" stroke="{T["line2"]}" stroke-width="1.2"/>']
    hi = "M58 58H96V64H132V68H170V75H214V79H262V86H330"
    lo = "M58 58H82V70H110V82H142V94H180V103H226V110H330"
    out.append(f'<path d="{hi}" fill="none" stroke="{T["cyan"]}" stroke-width="2" stroke-linejoin="round"/>')
    out.append(f'<path d="{lo}" fill="none" stroke="{T["magenta"]}" stroke-width="2" stroke-linejoin="round"/>')
    for x, y, col in ((150, 68, "cyan"), (238, 79, "cyan"), (296, 86, "cyan"), (124, 82, "magenta"), (204, 103, "magenta")):
        out.append(f'<line x1="{x}" y1="{y - 5}" x2="{x}" y2="{y + 5}" stroke="{T[col]}" stroke-width="1.4"/>')
    out.append(text(194, 141, "TIME", size=10.5, cls="mono low caps", anchor="middle"))
    out.append(f'<circle cx="352" cy="66" r="4" fill="{T["cyan"]}"/>' + text(362, 70, "high", size=11.5, cls="mono mid"))
    out.append(f'<circle cx="352" cy="88" r="4" fill="{T["magenta"]}"/>' + text(362, 92, "low", size=11.5, cls="mono mid"))
    return "  " + "".join(out)


def art_singlecell() -> str:
    """An embedding with four cell populations (schematic)."""
    out = []
    clusters = [
        ("cyan", [(96, 72), (108, 64), (118, 78), (104, 86), (90, 88), (122, 66), (112, 94), (98, 60), (126, 86)]),
        ("magenta", [(176, 104), (190, 96), (200, 110), (184, 116), (168, 114), (206, 100), (194, 122)]),
        ("violet", [(228, 60), (242, 68), (236, 78), (252, 58), (258, 74), (246, 84), (224, 74)]),
        ("green", [(300, 98), (312, 108), (322, 94), (308, 118), (328, 110), (296, 112)]),
    ]
    for i, (col, pts) in enumerate(clusters):
        for k, (x, y) in enumerate(pts):
            op = ".95" if k % 3 else ".5"
            out.append(f'<circle cx="{x}" cy="{y}" r="3.4" fill="{T[col]}" fill-opacity="{op}"/>')
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        out.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="27" fill="none" stroke="{T[col]}" stroke-opacity=".3" stroke-dasharray="3 5" class="breathe" style="animation-delay:{i * 0.9:g}s"/>')
    out.append(f'<path d="M44 132V112M44 132H64" fill="none" stroke="{T["low"]}" stroke-width="1.2" stroke-linecap="round"/>')
    out.append(text(70, 136, "UMAP", size=10, cls="mono low caps"))
    return "  " + "".join(out)


def art_crispr() -> str:
    """A guide RNA paired to its target next to the PAM, and guide-level counts feeding a gene ranking."""
    out = []
    y = 86
    out.append(f'<path d="M40 {y}H232M40 {y + 12}H232" fill="none" stroke="{T["line2"]}" stroke-width="2" stroke-linecap="round"/>')
    for x in range(48, 232, 12):
        out.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 12}" stroke="{T["line2"]}" stroke-width="1"/>')
    out.append(f'<rect x="84" y="{y - 14}" width="98" height="8" rx="4" fill="{T["cyan"]}" class="breathe"/>')
    out.append(text(133, y - 21, "sgRNA", size=11.5, cls="mono cy", anchor="middle"))
    out.append(f'<rect x="186" y="{y - 4}" width="26" height="20" rx="4" fill="{T["amber"]}" fill-opacity=".16" stroke="{T["amber"]}" stroke-opacity=".8"/>')
    out.append(text(199, y + 31, "PAM", size=10.5, cls="mono am", anchor="middle"))
    out.append(f'<path d="M172 {y - 2}l5 8l-5 8" fill="none" stroke="{T["magenta"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append(text(170, y + 31, "cut", size=10.5, cls="mono mg", anchor="end"))
    # gene ranking: sorted scores, top hits highlighted
    for k in range(14):
        x = 268 + k * 9.5
        h = 8 + (k * k) * 0.22
        col = T["magenta"] if k >= 11 else T["low"]
        out.append(f'<rect x="{x:g}" y="{118 - h:.1f}" width="5.5" height="{h:.1f}" rx="1.5" fill="{col}"/>')
    out.append(f'<line x1="262" y1="118.5" x2="404" y2="118.5" stroke="{T["line2"]}"/>')
    out.append(text(333, 136, "GENE RANK", size=10.5, cls="mono low caps", anchor="middle"))
    return "  " + "".join(out)


def art_volume() -> str:
    """A calibrated image volume with three orthogonal slice planes."""
    out = []
    ox, oy, w, h, d = 104, 116, 96, 62, 44          # front-bottom-left corner, sizes, depth offset
    front = f"M{ox} {oy}h{w}v{-h}h{-w}z"
    back = f"M{ox + d} {oy - d * 0.6:g}h{w}v{-h}h{-w}z"
    out.append(f'<path d="{back}" fill="none" stroke="{T["line2"]}" stroke-width="1.2"/>')
    for (x, y) in ((ox, oy), (ox + w, oy), (ox, oy - h), (ox + w, oy - h)):
        out.append(f'<line x1="{x}" y1="{y}" x2="{x + d}" y2="{y - d * 0.6:g}" stroke="{T["line2"]}" stroke-width="1.2"/>')
    # slice planes
    out.append(f'<path d="M{ox + d * 0.5:g} {oy - d * 0.3:g}h{w}v{-h}h{-w}z" fill="{T["cyan"]}" fill-opacity=".14" stroke="{T["cyan"]}" stroke-width="1.3" class="breathe"/>')
    out.append(f'<path d="M{ox} {oy - h * 0.5:g}h{w}l{d} {-d * 0.6:g}h{-w}z" fill="{T["magenta"]}" fill-opacity=".12" stroke="{T["magenta"]}" stroke-width="1.3"/>')
    out.append(f'<path d="M{ox + w * 0.5:g} {oy}v{-h}l{d} {-d * 0.6:g}v{h}z" fill="{T["violet"]}" fill-opacity=".12" stroke="{T["violet"]}" stroke-width="1.3"/>')
    out.append(f'<path d="{front}" fill="none" stroke="{T["mid"]}" stroke-opacity=".7" stroke-width="1.2"/>')
    for i, (lab, col) in enumerate((("XY", "cyan"), ("XZ", "magenta"), ("YZ", "violet"))):
        y = 64 + i * 24
        out.append(f'<rect x="286" y="{y - 9}" width="12" height="12" rx="3" fill="{T[col]}" fill-opacity=".25" stroke="{T[col]}"/>' + text(306, y + 1, lab, size=12, cls="mono mid"))
    out.append(text(346, 65, "calibrated", size=11, cls="mono low"))
    out.append(text(346, 89, "voxels", size=11, cls="mono low"))
    return "  " + "".join(out)


CARDS = [
    # stem, index, label, language chip, tagline, art, alt/title, accent
    ("card-multiomics", "01", "MULTIOMICS", "PYTHON", "CONNECTED LAYERS", art_multiomics,
     "01 / Multiomics: single-cell, spatial and bulk layers connected", "cyan"),
    ("card-multiscale", "02", "MULTISCALE", "R", "FROM CELLS TO TISSUE TO COHORT", art_multiscale,
     "02 / Multiscale: from cells to tissue to cohort", "violet"),
    ("card-survival", "03", "CLINICAL SIGNALS", "R", "EXPRESSION AND OUTCOME", art_survival,
     "03 / Clinical signals: expression and outcome", "cyan"),
    ("card-singlecell", "04", "SINGLE CELL", "PYTHON", "CELLULAR HETEROGENEITY", art_singlecell,
     "04 / Single cell: cellular heterogeneity", "magenta"),
    ("card-crispr", "05", "CRISPR SCREEN", "PYTHON", "PERTURBATION TO EVIDENCE", art_crispr,
     "05 / CRISPR screen: perturbation to evidence", "cyan"),
    ("card-volume", "06", "AX / VOLUME", "3D IMAGING", "VOXELS TO EVIDENCE", art_volume,
     "06 / AX / VOLUME: 3D microscopy, voxels to evidence", "violet"),
]


def build(out_dir) -> list[str]:
    from theme import write

    names = []
    for stem, index, label, lang, tagline, art, title, accent in CARDS:
        write(f"{out_dir}/{stem}.svg", _frame(index, label, lang, tagline, art(), title, accent))
        names.append(f"{stem}.svg")
    return names
