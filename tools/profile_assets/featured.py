"""Feature banners: the agent-skills repository and the tmelens toolkit.

Each banner has a wide layout (text left, drawing right) and a narrow-screen layout
(text on top, drawing below). The drawings are schematics: no values, no results.
"""
from __future__ import annotations

from theme import MW, T, W, chip_row, document, panel, text

PAD_BOTTOM = 30

SKILLS_COPY = {
    "label": "AGENT SKILLS · SKILL.md",
    "title": "tumor-immunology-skills",
    "wide": ["Evidence-linked skills that teach coding agents to analyse", "tumor-immune data: cited rules, tested scripts, evals."],
    "narrow": ["Evidence-linked skills that teach coding agents", "to analyse tumor-immune data: cited rules,", "tested scripts, evals."],
    "chips": [("cited sources", "cyan"), ("stdlib scripts", "violet"), ("unit tests", "green"), ("evals", "magenta")],
    "alt": "tumor-immunology-skills: evidence-linked agent skills for tumor immunology research",
}
TMELENS_COPY = {
    "label": "PYTHON TOOLKIT · MIT",
    "title": "tmelens",
    "wide": ["Look inside the tumour immune microenvironment", "from a bulk expression matrix."],
    "narrow": ["Look inside the tumour immune microenvironment", "from a bulk expression matrix."],
    "chips": [("signature scoring", "cyan"), ("hot / excluded / cold", "magenta"), ("deconvolution", "violet"), ("survival", "green"), ("ICB response", "amber")],
    "alt": "tmelens: profile the tumour immune microenvironment from bulk transcriptomes",
}


def _text_block(copy: dict, lines: list[str], *, x: float, width: float, title_size: float, badge: str | None = None,
                chip_size: float = 12, chip_h: float = 24) -> tuple[str, float]:
    """Label, title, description lines and chips. Returns (svg, bottom edge)."""
    out = []
    lx = x
    if badge:
        bw = len(badge) * 7.6 + 18
        out.append(
            f'<rect x="{x}" y="27" width="{bw:g}" height="20" rx="10" fill="{T["magenta"]}" fill-opacity=".16" stroke="{T["magenta"]}" stroke-opacity=".8"/>'
            + text(x + bw / 2, 41, badge, size=11, cls="mono mg caps b", anchor="middle")
        )
        lx = x + bw + 12
    out.append(text(lx, 41, copy["label"], size=12, cls="mono low caps"))
    y_title = 55 + title_size
    out.append(text(x, y_title, copy["title"], size=title_size, cls="mono b hi"))
    y = y_title + 28
    for line in lines:
        out.append(text(x, y, line, size=15, cls="sans mid"))
        y += 21
    row, _, last_y = chip_row(x, y - 4, copy["chips"], size=chip_size, height=chip_h, gap=8, max_width=width)
    out.append(row)
    return "  " + "\n  ".join(out), last_y + chip_h


def _skill_window(bx: float, by: float, bw: float, bh: float, example_skill: str) -> tuple[str, str, str]:
    """A SKILL.md file being scanned. Returns (svg, extra defs, extra style)."""
    rows = [
        ("---", "low", None),
        ("name:", "cy", example_skill),
        ("description:", "cy", "what + when"),
        ("---", "low", None),
        ("## Workflow", "hi", None),
        ("## Pitfalls", "hi", None),
        ("## Scripts", "hi", "tested"),
        ("## References", "hi", "DOI-checked"),
    ]
    lines = []
    for i, (key, cls, val) in enumerate(rows):
        y = by + 43 + i * 15.5
        lines.append(text(bx + 16, y, key, size=11.5, cls=f"mono {cls}"))
        if val and key.endswith(":"):
            lines.append(text(bx + 16 + (len(key) + 1) * 7.15, y, val, size=11.5, cls="mono mid"))
        elif val:
            lines.append(
                f'<path d="M{bx + 150} {y - 4}l3 3l6 -7" fill="none" stroke="{T["green"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>'
                + text(bx + 166, y, val, size=11, cls="mono gr")
            )
    svg = (
        f'  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{T["bg0"]}" stroke="{T["line2"]}"/>\n'
        f'  <circle cx="{bx + 16}" cy="{by + 14}" r="3.5" fill="{T["magenta"]}" fill-opacity=".8"/><circle cx="{bx + 29}" cy="{by + 14}" r="3.5" fill="{T["amber"]}" fill-opacity=".8"/><circle cx="{bx + 42}" cy="{by + 14}" r="3.5" fill="{T["green"]}" fill-opacity=".8"/>\n'
        f'  {text(bx + bw - 14, by + 18, "SKILL.md", size=10.5, cls="mono low", anchor="end")}\n'
        f'  <line x1="{bx}" y1="{by + 27.5}" x2="{bx + bw}" y2="{by + 27.5}" stroke="{T["line"]}"/>\n'
        f'  {"".join(lines)}\n'
        f'  <clipPath id="box"><rect x="{bx + 1}" y="{by + 28}" width="{bw - 2}" height="{bh - 29}" rx="9"/></clipPath>\n'
        f'  <g clip-path="url(#box)"><rect class="scan" x="{bx}" y="{by + 28}" width="{bw}" height="26" fill="url(#scanG)"/></g>'
    )
    defs = (
        f'<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["cyan"]}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{T["cyan"]}" stop-opacity=".16"/></linearGradient>'
    )
    style = f"@keyframes scan {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY({bh - 28}px); }} }} .scan {{ animation: scan 5.5s ease-in-out infinite alternate; }}\n"
    return svg, defs, style


def _matrix_lens(gx: float, gy: float, *, cell: int = 15, gap: int = 4, cols: int = 16, rows_n: int = 8) -> tuple[str, float]:
    """A samples-by-signatures tile matrix under a lens. Returns (svg, bottom edge)."""
    palette = [T["cyan"], T["violet"], T["magenta"], T["line2"]]
    squares = []
    for r in range(rows_n):
        for c in range(cols):
            k = (r * 7 + c * 3 + (r * c) % 5) % 9
            col = palette[0] if k < 3 else palette[1] if k < 5 else palette[2] if k < 6 else palette[3]
            op = (0.28, 0.5, 0.75, 0.95)[(r + 2 * c) % 4]
            squares.append(f'<rect x="{gx + c * (cell + gap)}" y="{gy + r * (cell + gap)}" width="{cell}" height="{cell}" rx="3" fill="{col}" fill-opacity="{op}"/>')
    lcx, lcy, lr = gx + 7.5 * (cell + gap), gy + (rows_n / 2 - 0.1) * (cell + gap), 46
    lens = (
        f'<circle cx="{lcx:g}" cy="{lcy:g}" r="{lr + 16}" fill="url(#halo)"/>'
        f'<circle cx="{lcx:g}" cy="{lcy:g}" r="{lr}" fill="{T["bg0"]}" fill-opacity=".35" stroke="{T["cyan2"]}" stroke-width="1.8"/>'
        f'<g class="spin"><circle cx="{lcx:g}" cy="{lcy:g}" r="{lr + 8}" fill="none" stroke="{T["cyan"]}" stroke-opacity=".55" stroke-dasharray="2 9"/></g>'
        f'<path d="M{lcx - lr - 12:g} {lcy:g}h10M{lcx + lr + 2:g} {lcy:g}h10M{lcx:g} {lcy - lr - 12:g}v10M{lcx:g} {lcy + lr + 2:g}v10" stroke="{T["cyan2"]}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<path d="M{lcx + lr * 0.72:g} {lcy + lr * 0.72:g}l22 22" stroke="{T["cyan2"]}" stroke-width="4" stroke-linecap="round"/>'
    )
    y_label = gy + rows_n * (cell + gap) + 14
    svg = (
        "  <g>" + "".join(squares) + "</g>\n"
        f"  {lens}\n"
        f'  {text(gx, y_label, "SAMPLES", size=10.5, cls="mono low caps")}'
        f'{text(gx + cols * (cell + gap) - gap, y_label, "SIGNATURES", size=10.5, cls="mono low caps", anchor="end")}'
    )
    return svg, y_label + 6


def skills_svg(example_skill: str = "tme-bulk-profiling", badge: str | None = "NEW") -> str:
    left, bottom = _text_block(SKILLS_COPY, SKILLS_COPY["wide"], x=32, width=480, title_size=27, badge=badge)
    h = int(bottom + PAD_BOTTOM)
    bw, bh = 308, 160
    window, defs, style = _skill_window(540, (h - bh) // 2, bw, bh, example_skill)
    body = panel(W, h, accent="magenta") + "\n" + left + "\n" + window
    return document(W, h, body, SKILLS_COPY["alt"], extra_defs=defs, extra_style=style)


def skills_mobile_svg(example_skill: str = "tme-bulk-profiling", badge: str | None = "NEW") -> str:
    left, bottom = _text_block(SKILLS_COPY, SKILLS_COPY["narrow"], x=24, width=392, title_size=23, badge=badge, chip_size=13, chip_h=26)
    bw, bh = 392, 160
    by = int(bottom + 18)
    window, defs, style = _skill_window(24, by, bw, bh, example_skill)
    h = by + bh + 26
    body = panel(MW, h, accent="magenta") + "\n" + left + "\n" + window
    return document(MW, h, body, SKILLS_COPY["alt"], extra_defs=defs, extra_style=style)


def tmelens_svg() -> str:
    left, bottom = _text_block(TMELENS_COPY, TMELENS_COPY["wide"], x=32, width=480, title_size=27)
    h = int(bottom + PAD_BOTTOM)
    cell, gap, rows_n = 15, 4, 8
    gy = (h - (rows_n * (cell + gap) - gap) - 18) // 2
    matrix, _ = _matrix_lens(548, gy, cell=cell, gap=gap, rows_n=rows_n)
    body = panel(W, h, accent="cyan") + "\n" + left + "\n" + matrix
    return document(W, h, body, TMELENS_COPY["alt"])


def tmelens_mobile_svg() -> str:
    left, bottom = _text_block(TMELENS_COPY, TMELENS_COPY["narrow"], x=24, width=392, title_size=25, chip_size=13, chip_h=26)
    cell, gap, cols = 19, 5, 16          # 16 * 24 - 5 = 379 wide
    matrix, bottom2 = _matrix_lens(30, int(bottom + 22), cell=cell, gap=gap, cols=cols, rows_n=6)
    h = int(bottom2 + 22)
    body = panel(MW, h, accent="cyan") + "\n" + left + "\n" + matrix
    return document(MW, h, body, TMELENS_COPY["alt"])


def build(out_dir) -> list[str]:
    from theme import write

    write(f"{out_dir}/feat-skills.svg", skills_svg())
    write(f"{out_dir}/m/feat-skills.svg", skills_mobile_svg())
    write(f"{out_dir}/feat-tmelens.svg", tmelens_svg())
    write(f"{out_dir}/m/feat-tmelens.svg", tmelens_mobile_svg())
    return ["feat-skills.svg", "m/feat-skills.svg", "feat-tmelens.svg", "m/feat-tmelens.svg"]
