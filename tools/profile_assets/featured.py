"""Two full-width feature banners: the agent-skills repository and the tmelens toolkit."""
from __future__ import annotations

from theme import T, W, chip_row, document, panel, text

PAD_BOTTOM = 30


def _left(label: str, title: str, lines: list[str], chips: list[tuple[str, str]], badge: str | None = None) -> tuple[str, float]:
    out = []
    x = 32
    lx = x
    if badge:
        bw = len(badge) * 7.6 + 18
        out.append(
            f'<rect x="{x}" y="27" width="{bw:g}" height="20" rx="10" fill="{T["magenta"]}" fill-opacity=".16" stroke="{T["magenta"]}" stroke-opacity=".8"/>'
            + text(x + bw / 2, 41, badge, size=11, cls="mono mg caps b", anchor="middle")
        )
        lx = x + bw + 12
    out.append(text(lx, 41, label, size=12, cls="mono low caps"))
    out.append(text(x, 82, title, size=27, cls="mono b hi"))
    for i, line in enumerate(lines):
        out.append(text(x, 110 + i * 21, line, size=15, cls="sans mid"))
    row, _, last_y = chip_row(x, 158, chips, size=12, height=24, gap=8, max_width=480)
    out.append(row)
    return "  " + "\n  ".join(out), last_y + 24


def skills_svg(example_skill: str = "tme-bulk-profiling") -> str:
    left, bottom = _left(
        "AGENT SKILLS · SKILL.md",
        "tumor-immunology-skills",
        ["Evidence-linked skills that teach coding agents to analyse", "tumor-immune data: cited rules, tested scripts, evals."],
        [("cited sources", "cyan"), ("stdlib scripts", "violet"), ("unit tests", "green"), ("evals", "magenta")],
        badge="NEW",
    )
    H = int(bottom + PAD_BOTTOM)
    # right: a skill file being scanned
    bw, bh = 308, 160
    bx, by = 540, (H - bh) // 2
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
    right = (
        f'  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{T["bg0"]}" stroke="{T["line2"]}"/>\n'
        f'  <circle cx="{bx + 16}" cy="{by + 14}" r="3.5" fill="{T["magenta"]}" fill-opacity=".8"/><circle cx="{bx + 29}" cy="{by + 14}" r="3.5" fill="{T["amber"]}" fill-opacity=".8"/><circle cx="{bx + 42}" cy="{by + 14}" r="3.5" fill="{T["green"]}" fill-opacity=".8"/>\n'
        f'  {text(bx + bw - 14, by + 18, "SKILL.md", size=10.5, cls="mono low", anchor="end")}\n'
        f'  <line x1="{bx}" y1="{by + 27.5}" x2="{bx + bw}" y2="{by + 27.5}" stroke="{T["line"]}"/>\n'
        f'  {"".join(lines)}\n'
        f'  <clipPath id="box"><rect x="{bx + 1}" y="{by + 28}" width="{bw - 2}" height="{bh - 29}" rx="9"/></clipPath>\n'
        f'  <g clip-path="url(#box)"><rect class="scan" x="{bx}" y="{by + 28}" width="{bw}" height="26" fill="url(#scanG)"/></g>'
    )
    extra_defs = (
        f'<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["cyan"]}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{T["cyan"]}" stop-opacity=".16"/></linearGradient>'
    )
    extra_style = "@keyframes scan { 0% { transform: translateY(0); } 100% { transform: translateY(132px); } } .scan { animation: scan 5.5s ease-in-out infinite alternate; }\n"
    body = panel(W, H, accent="magenta") + "\n" + left + "\n" + right
    return document(W, H, body, "tumor-immunology-skills: evidence-linked agent skills for tumor immunology research", extra_defs=extra_defs, extra_style=extra_style)


def tmelens_svg() -> str:
    left, bottom = _left(
        "PYTHON TOOLKIT · MIT",
        "tmelens",
        ["Look inside the tumour immune microenvironment", "from a bulk expression matrix."],
        [("signature scoring", "cyan"), ("hot / excluded / cold", "magenta"), ("deconvolution", "violet"), ("survival", "green"), ("ICB response", "amber")],
    )
    # right: a sample-by-signature matrix under a lens (schematic, no values)
    H = int(bottom + PAD_BOTTOM)
    cell, gap, cols, rows_n = 15, 4, 16, 8
    gx, gy = 548, (H - (rows_n * (cell + gap) - gap) - 18) // 2
    palette = [T["cyan"], T["violet"], T["magenta"], T["line2"]]
    squares = []
    for r in range(rows_n):
        for c in range(cols):
            k = (r * 7 + c * 3 + (r * c) % 5) % 9
            col = palette[0] if k < 3 else palette[1] if k < 5 else palette[2] if k < 6 else palette[3]
            op = (0.28, 0.5, 0.75, 0.95)[(r + 2 * c) % 4]
            squares.append(f'<rect x="{gx + c * (cell + gap)}" y="{gy + r * (cell + gap)}" width="{cell}" height="{cell}" rx="3" fill="{col}" fill-opacity="{op}"/>')
    lcx, lcy, lr = gx + 7.5 * (cell + gap), gy + 3.9 * (cell + gap), 46
    lens = (
        f'<circle cx="{lcx:g}" cy="{lcy:g}" r="{lr + 16}" fill="url(#halo)"/>'
        f'<circle cx="{lcx:g}" cy="{lcy:g}" r="{lr}" fill="{T["bg0"]}" fill-opacity=".35" stroke="{T["cyan2"]}" stroke-width="1.8"/>'
        f'<g class="spin"><circle cx="{lcx:g}" cy="{lcy:g}" r="{lr + 8}" fill="none" stroke="{T["cyan"]}" stroke-opacity=".55" stroke-dasharray="2 9"/></g>'
        f'<path d="M{lcx - lr - 12:g} {lcy:g}h10M{lcx + lr + 2:g} {lcy:g}h10M{lcx:g} {lcy - lr - 12:g}v10M{lcx:g} {lcy + lr + 2:g}v10" stroke="{T["cyan2"]}" stroke-width="1.6" stroke-linecap="round"/>'
        f'<path d="M{lcx + lr * 0.72:g} {lcy + lr * 0.72:g}l22 22" stroke="{T["cyan2"]}" stroke-width="4" stroke-linecap="round"/>'
    )
    right = (
        "  <g>" + "".join(squares) + "</g>\n"
        f"  {lens}\n"
        f'  {text(gx, gy + rows_n * (cell + gap) + 14, "SAMPLES", size=10.5, cls="mono low caps")}'
        f'{text(gx + cols * (cell + gap) - gap, gy + rows_n * (cell + gap) + 14, "SIGNATURES", size=10.5, cls="mono low caps", anchor="end")}'
    )
    body = panel(W, H, accent="cyan") + "\n" + left + "\n" + right
    return document(W, H, body, "tmelens: profile the tumour immune microenvironment from bulk transcriptomes")


def build(out_dir) -> list[str]:
    from theme import write

    write(f"{out_dir}/feat-skills.svg", skills_svg())
    write(f"{out_dir}/feat-tmelens.svg", tmelens_svg())
    return ["feat-skills.svg", "feat-tmelens.svg"]
