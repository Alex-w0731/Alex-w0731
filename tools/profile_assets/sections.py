"""Section header strips: index, label, an animated signal rule and a right-hand tag."""
from __future__ import annotations

from theme import T, W, document, hairline, mono_width, text

H = 56

SECTIONS = [
    # (file stem, index, label, tag, accent)
    ("sec-focus", "01", "RESEARCH FOCUS", "OBSERVE · MODEL · PERTURB · VALIDATE", "cyan"),
    ("sec-build", "02", "OPEN TOOLS", "SKILLS · TOOLKITS", "violet"),
    ("sec-work", "03", "SELECTED WORK", "SIX STARTING POINTS", "cyan"),
    ("sec-stack", "04", "TOOLS & METHODS", "COMPUTE · VALIDATE", "magenta"),
    ("sec-radar", "05", "RESEARCH RADAR", "QUESTIONS TO METHODS", "violet"),
    ("sec-pubs", "06", "SELECTED PUBLICATIONS", "PEER REVIEWED", "cyan"),
]


def section(index: str, label: str, tag: str, accent: str) -> str:
    c = T[accent]
    label_size = 19
    x_index = 18
    x_label = x_index + mono_width(index, 15, 1.5) + 26
    label_w = mono_width(label, label_size, label_size * 0.16)
    tag_w = mono_width(tag, 11.5, 11.5 * 0.16)
    x_rule0 = x_label + label_w + 20
    x_rule1 = W - 18 - tag_w - 18
    y = H / 2
    index_extra = ' fill="' + c + '" letter-spacing="1.5"'
    rule = ""
    if x_rule1 - x_rule0 > 40:
        rule = (
            hairline(x_rule0, y, x_rule1, y, color="line2")
            + f'<line x1="{x_rule0:g}" y1="{y:g}" x2="{x_rule1:g}" y2="{y:g}" stroke="{c}" stroke-width="1.6" class="flow" opacity=".9"/>'
            + f'<circle cx="{x_rule1:g}" cy="{y:g}" r="2.6" fill="{c}" class="pulse"/>'
        )
    body = (
        f'  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="10" fill="url(#bg)" stroke="{T["line2"]}"/>\n'
        f'  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="10" fill="url(#dots)" opacity=".5"/>\n'
        f'  <rect x="0" y="12" width="3" height="{H - 24}" rx="1.5" fill="{c}"/>\n'
        f'  {text(x_index, y + 5.5, index, size=15, cls="mono b", extra=index_extra)}\n'
        f'  <path d="M{x_label - 16:g} {y + 9:g}l8 -18" stroke="{T["low"]}" stroke-width="1.4" fill="none"/>\n'
        f'  {text(x_label, y + 6.5, label, size=label_size, cls="mono b hi caps")}\n'
        f"  {rule}\n"
        f'  {text(W - 18, y + 4, tag, size=11.5, cls="mono low caps", anchor="end")}'
    )
    return document(W, H, body, label.title())


def build(out_dir) -> list[str]:
    from theme import write

    names = []
    for stem, index, label, tag, accent in SECTIONS:
        write(f"{out_dir}/{stem}.svg", section(index, label, tag, accent))
        names.append(f"{stem}.svg")
    return names
