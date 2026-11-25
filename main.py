"""Entrypoint: render the 25 November 2026 world-news poster.

Writes /output/entry.png (1024x1024 PNG, under 1 MiB), and a local
copy at ./entry.png for inspection. Deterministic: no network, no
clock, no randomness beyond a fixed seed inside draw.py.
"""

import os
import shutil
from pathlib import Path

from draw import render

OUT = Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.png"))


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    render(str(OUT))
    local = Path(__file__).resolve().parent / "entry.png"
    if local.resolve() != OUT.resolve():
        shutil.copyfile(OUT, local)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
