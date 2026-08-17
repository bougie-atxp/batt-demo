#!/usr/bin/env python3
"""Build index.html from src/index.template.html.

Replaces every <!--BATT_PATHS--> placeholder with the BATT logo mark
(assets/batt-mark-paths.html — inner-SVG path markup originally extracted
from assets/batt-slim.svg). The output index.html is committed; GitHub
Pages serves it as-is from the repo root.

Usage: python3 build.py
"""
from pathlib import Path

root = Path(__file__).parent
template = (root / "src" / "index.template.html").read_text()
mark = (root / "assets" / "batt-mark-paths.html").read_text()

if "<!--BATT_PATHS-->" not in template:
    raise SystemExit("template has no <!--BATT_PATHS--> placeholder — aborting")

out = template.replace("<!--BATT_PATHS-->", mark)
(root / "index.html").write_text(out)
print(f"built index.html ({len(out):,} bytes, "
      f"{template.count('<!--BATT_PATHS-->')} mark placeholders filled)")
