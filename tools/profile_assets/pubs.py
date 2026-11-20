"""Year and journal chips shown above each publication title."""
from __future__ import annotations

from theme import T, document, mono_width, text

CH = 26

PUBS = [
    # stem, year, journal, accent
    ("pub-cell-bioscience", "2025", "CELL & BIOSCIENCE", "cyan"),
    ("pub-jacs-au", "2024", "JACS AU", "violet"),
    ("pub-biology-direct", "2025", "BIOLOGY DIRECT", "magenta"),
]


def chip(year: str, journal: str, accent: str) -> str:
    c = T[accent]
    yw = mono_width(year, 12.5, 1.2) + 20
    jw = mono_width(journal, 11.5, 11.5 * 0.16) + 22
    w = int(yw + jw)
    year_extra = ' fill="' + c + '" letter-spacing="1.2"'
    body = (
        f'  <rect x=".5" y=".5" width="{w - 1}" height="{CH - 1}" rx="7" fill="url(#bg)" stroke="{T["line2"]}"/>\n'
        f'  <path d="M7.5 .5H{yw:g}V{CH - .5}H7.5a7 7 0 0 1 -7 -7V7.5a7 7 0 0 1 7 -7z" fill="{c}" fill-opacity=".14" stroke="{c}" stroke-opacity=".7"/>\n'
        f'  {text(yw / 2, CH / 2 + 4.5, year, size=12.5, cls="mono b", anchor="middle", extra=year_extra)}\n'
        f'  {text(yw + 11, CH / 2 + 4, journal, size=11.5, cls="mono mid caps")}'
    )
    return document(w, CH, body, f"{year} · {journal.title()}")


def build(out_dir) -> list[str]:
    from theme import write

    names = []
    for stem, year, journal, accent in PUBS:
        write(f"{out_dir}/{stem}.svg", chip(year, journal, accent))
        names.append(f"{stem}.svg")
    return names
