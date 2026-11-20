"""Footer signal trace: a quiet line with one travelling pulse."""
from __future__ import annotations

from theme import MW, T, W, document, text

H = 72


def build_svg(mobile: bool = False) -> str:
    y = 40
    W = MW if mobile else globals()["W"]
    lead = 150 if mobile else 330
    blip = f"M24 {y}H{lead}l10 -4l8 4l10 0l7 -22l9 40l8 -26l7 8h12l9 -5l9 5H{W - 24}"
    body = (
        f'  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="url(#bg)" stroke="{T["line2"]}"/>\n'
        f'  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="url(#dots)" opacity=".45"/>\n'
        f'  <path d="{blip}" fill="none" stroke="url(#acc)" stroke-opacity=".75" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round"/>\n'
        f'  <path d="{blip}" fill="none" stroke="{T["cyan2"]}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round" class="trace"/>\n'
        f'  {text(24, 22, "END OF SIGNAL", size=10.5, cls="mono low caps")}\n'
        f'  {text(W - 24, 22, "STAY CURIOUS", size=10.5, cls="mono low caps", anchor="end")}\n'
        f'  <rect x="{W - 24 - 7}" y="{H - 21}" width="7" height="11" fill="{T["cyan"]}" class="blink"/>'
    )
    extra_style = (
        ".trace { stroke-dasharray: 150 1100; animation: travel 6s linear infinite; }\n"
        "    @keyframes travel { from { stroke-dashoffset: 300; } to { stroke-dashoffset: -950; } }\n"
        "    @media (prefers-reduced-motion: reduce) { .trace { stroke-dasharray: none; } }\n"
    )
    return document(W, H, body, "End of signal. Stay curious.", extra_style=extra_style)


def build(out_dir) -> list[str]:
    from theme import write

    write(f"{out_dir}/footer.svg", build_svg())
    write(f"{out_dir}/m/footer.svg", build_svg(mobile=True))
    return ["footer.svg", "m/footer.svg"]
