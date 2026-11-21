"""Social preview card (1280 x 640) for the tumor-immunology-skills repository.

GitHub accepts PNG, JPG or GIF for social previews, so this SVG is rendered to PNG separately
(see build_social_png in build.py). Not part of the profile README.
"""
from __future__ import annotations

from featured import SKILLS_COPY, _skill_window
from theme import T, chip_row, document, panel, text

SW, SH = 1280, 640


def social_svg(n_skills: int, n_tests: int, version: str) -> str:
    x = 72
    parts = [panel(SW, SH, rx=0, accent="magenta")]
    parts.append("  " + text(x, 120, "AGENT SKILLS · SKILL.md · " + version, size=22, cls="mono low caps"))
    parts.append("  " + text(x, 196, "tumor-immunology", size=64, cls="mono b hi"))
    parts.append("  " + text(x, 266, "-skills", size=64, cls="mono b", extra=' fill="url(#acc)"'))
    parts.append("  " + text(x, 332, "Evidence-linked agent skills that teach coding", size=27, cls="sans mid"))
    parts.append("  " + text(x, 368, "agents to analyse tumor-immune data.", size=27, cls="sans mid"))
    chips = [(f"{n_skills} skills", "cyan"), ("cited sources", "violet"), (f"{n_tests} unit tests", "green"), ("blind evals", "magenta")]
    row, _, _ = chip_row(x, 412, chips, size=18, height=38, gap=12, max_width=720, pad=16)
    parts.append("  " + row)
    parts.append("  " + text(x, 560, "Alex Wang", size=24, cls="sans sb hi") + text(x + 136, 560, "github.com/Alex-w0731/tumor-immunology-skills", size=20, cls="mono low"))
    # the SKILL.md window is drawn at its banner size (308 x 160) and scaled up as a whole
    window, defs, style = _skill_window(0, 0, 308, 160, "tme-bulk-profiling")
    parts.append(f'  <g transform="translate(812 220) scale(1.3)">{window}</g>')
    return document(SW, SH, "\n".join(parts), SKILLS_COPY["alt"], extra_defs=defs, extra_style=style)
