#!/usr/bin/env python3
"""Regenerate every profile graphic under assets/hud/ from the shared design tokens.

usage:
  python3 tools/profile_assets/build.py            # write assets/hud/*.svg
  python3 tools/profile_assets/build.py --check    # fail if the committed files are stale
  python3 tools/profile_assets/build.py --sheet out.html   # also write a contact sheet for review

Standard library only. Each module exposes build(out_dir) -> list of file names.
"""
from __future__ import annotations

import argparse
import importlib
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
OUT = REPO / "assets" / "hud"
MODULES = ["hero", "hero_alt", "sections", "loop", "cards", "featured", "stack", "radar", "footer", "buttons"]

sys.path.insert(0, str(HERE))


def generate(out_dir: Path) -> list[str]:
    names: list[str] = []
    for name in MODULES:
        if not (HERE / f"{name}.py").exists():
            continue
        names.extend(importlib.import_module(name).build(str(out_dir)))
    return names


def contact_sheet(names: list[str], prefix: str) -> str:
    rows = "".join(
        f'<figure><img src="{prefix}{n}" alt="{n}"><figcaption>{n}</figcaption></figure>' for n in names
    )
    return (
        "<!doctype html><meta charset='utf-8'><title>profile assets</title><style>"
        "body{margin:0;font:12px ui-monospace,Menlo,monospace}"
        ".col{padding:24px;display:flex;flex-direction:column;gap:14px;align-items:flex-start}"
        ".dark{background:#0d1117;color:#9198a1}.light{background:#fff;color:#59636e}"
        "figure{margin:0;max-width:846px}img{max-width:846px;display:block}figcaption{margin-top:4px;opacity:.7}"
        "</style>"
        f"<div class='col dark'>{rows}</div><div class='col light'>{rows}</div>"
        # review aid: sheet.html?only=card,feat shows matching graphics; &theme=dark|light shows one column
        "<script>const q=new URLSearchParams(location.search);const only=(q.get('only')||'').split(',').filter(Boolean);"
        "if(only.length)document.querySelectorAll('figure').forEach(f=>{if(!only.some(o=>f.textContent.includes(o)))f.remove()});"
        "const t=q.get('theme');if(t)document.querySelectorAll('.col').forEach(c=>{if(!c.classList.contains(t))c.remove()});</script>"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the profile graphics.")
    parser.add_argument("--check", action="store_true", help="verify that assets/hud is up to date")
    parser.add_argument("--sheet", metavar="HTML", help="write a contact sheet that shows every graphic")
    parser.add_argument("--sheet-prefix", default="/Alex-w0731/assets/hud/", help="URL prefix used by the contact sheet")
    args = parser.parse_args(argv)
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            names = generate(Path(tmp))
            stale = [n for n in names if not (OUT / n).exists() or (OUT / n).read_text(encoding="utf-8") != (Path(tmp) / n).read_text(encoding="utf-8")]
        if stale:
            print("stale graphics (run tools/profile_assets/build.py):", ", ".join(stale))
            return 1
        print(f"{len(names)} graphics up to date")
        return 0
    names = generate(OUT)
    print(f"wrote {len(names)} graphics to {OUT.relative_to(REPO)}")
    if args.sheet:
        Path(args.sheet).write_text(contact_sheet(names, args.sheet_prefix), encoding="utf-8")
        print("contact sheet:", args.sheet)
    return 0


if __name__ == "__main__":
    sys.exit(main())
