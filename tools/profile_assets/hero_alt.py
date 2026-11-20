"""Alternate hero: a bio-terminal console. Not used by the README by default.

To switch, point the first <img> in README.md at assets/hud/hero-terminal.svg.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "hero_terminal_gen.py"


def build(out_dir) -> list:
    out = Path(out_dir) / "hero-terminal.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(SCRIPT), str(out)], check=True, stdout=subprocess.DEVNULL)
    return ["hero-terminal.svg"]
