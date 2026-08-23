#!/usr/bin/env python3
"""Convert HEIC photos to browser-safe JPEG.

HEIC renders in Safari but not in Chrome or Firefox, so anything dropped into
content/<slug>/photos/ straight off an iPhone has to be converted before it can
go on a card.

Uses macOS `sips`, which is built in — no pip install, no dependencies.

    python3 scripts/convert-heic.py              # convert everything under content/
    python3 scripts/convert-heic.py --keep       # leave the .heic originals in place
    python3 scripts/convert-heic.py --dry-run    # show what would happen
    python3 scripts/convert-heic.py content/rotom/photos
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

QUALITY = "80"  # sips: low | normal | high | best, or a 0-100 int


def convert(src: Path, keep: bool, dry_run: bool) -> bool:
    dest = src.with_suffix(".jpg")

    if dest.exists():
        print(f"  skip   {src.name} -> {dest.name} already exists")
        return False

    if dry_run:
        print(f"  would  {src.name} -> {dest.name}")
        return True

    result = subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", QUALITY,
         str(src), "--out", str(dest)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0 or not dest.exists():
        print(f"  FAIL   {src.name}: {result.stderr.strip() or 'sips returned no output'}")
        return False

    before = src.stat().st_size
    after = dest.stat().st_size
    print(f"  ok     {src.name} -> {dest.name}  ({before // 1024}KB -> {after // 1024}KB)")

    if not keep:
        src.unlink()

    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="*", default=["content"],
                        help="directories to scan (default: content)")
    parser.add_argument("--keep", action="store_true",
                        help="keep the .heic originals instead of deleting them")
    parser.add_argument("--dry-run", action="store_true",
                        help="report what would be converted, change nothing")
    args = parser.parse_args()

    if not shutil.which("sips"):
        print("error: `sips` not found. This script needs macOS.", file=sys.stderr)
        return 1

    sources = []
    for raw in args.paths:
        root = Path(raw)
        if not root.exists():
            print(f"error: {root} does not exist", file=sys.stderr)
            return 1
        sources.extend(sorted(p for p in root.rglob("*")
                              if p.suffix.lower() == ".heic"))

    if not sources:
        print("No HEIC files found — nothing to do.")
        return 0

    print(f"Found {len(sources)} HEIC file(s):\n")
    converted = sum(convert(p, args.keep, args.dry_run) for p in sources)

    print(f"\n{converted}/{len(sources)} converted.")
    if converted and not args.keep and not args.dry_run:
        print("Originals removed. Recover any of them with: git checkout HEAD -- <path>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
