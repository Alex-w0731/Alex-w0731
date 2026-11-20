"""Link buttons used under the hero."""
from __future__ import annotations

from theme import T, document, mono_width, text

BH = 36


def _button(label: str, icon: str, color: str, title: str) -> str:
    c = T[color]
    w = int(mono_width(label, 12.5, 12.5 * 0.16) + 58)
    body = (
        f'  <rect x=".5" y=".5" width="{w - 1}" height="{BH - 1}" rx="9" fill="url(#bg)" stroke="{c}" stroke-opacity=".65"/>\n'
        f'  <rect x="1.5" y="1.5" width="{w - 3}" height="{BH - 3}" rx="8" fill="{c}" fill-opacity=".06"/>\n'
        f"  {icon}\n"
        f'  {text(40, BH / 2 + 4.5, label, size=12.5, cls="mono b hi caps")}'
    )
    return document(w, BH, body, title)


def _stroke(c: str) -> str:
    return f'fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'


BUTTONS = [
    ("btn-email", "EXCHANGE IDEAS", "cyan", "Email Alex: exchange ideas",
     lambda c: f'<g {_stroke(c)}><rect x="13" y="11" width="18" height="14" rx="2.5"/><path d="M14 13l8 6.5l8-6.5"/></g>'),
    ("btn-orcid", "ORCID", "green", "ORCID 0009-0005-8480-5387",
     lambda c: f'<circle cx="22" cy="18" r="9" fill="{c}" fill-opacity=".18" stroke="{c}" stroke-width="1.5"/><path d="M18.5 14.5v7.5M22 14.5h2.4a3.75 3.75 0 0 1 0 7.5H22z" {_stroke(c)}/><circle cx="18.5" cy="12" r=".9" fill="{c}"/>'),
    ("btn-skills", "AGENT SKILLS", "magenta", "tumor-immunology-skills repository",
     lambda c: f'<g {_stroke(c)}><path d="M22 10l9 4.5l-9 4.5l-9-4.5z"/><path d="M13 18.5l9 4.5l9-4.5"/><path d="M13 22.5l9 4.5l9-4.5" stroke-opacity=".55"/></g>'),
    ("btn-tmelens", "TMELENS", "violet", "tmelens repository",
     lambda c: f'<g {_stroke(c)}><circle cx="20.5" cy="16.5" r="6.5"/><path d="M25.5 21.5l5 5"/></g><circle cx="20.5" cy="16.5" r="2" fill="{c}"/>'),
]


def build(out_dir) -> list[str]:
    from theme import write

    names = []
    for stem, label, color, title, icon in BUTTONS:
        write(f"{out_dir}/{stem}.svg", _button(label, icon(T[color]), color, title))
        names.append(f"{stem}.svg")
    return names
