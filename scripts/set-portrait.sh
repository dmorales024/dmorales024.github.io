#!/usr/bin/env bash
# Replace the portrait on the links page.
#
#   scripts/set-portrait.sh ~/Downloads/whatever-you-downloaded.jpg
#
# No HTML change is needed — links/index.html always points at
# assets/dmitri-portrait.jpg. This just converts, resizes and drops it there.
#
# The photo cell renders at ~512x723 CSS px, which is 1024x1446 device pixels on a
# retina screen. Anything smaller than that gets upscaled and looks soft.

set -euo pipefail

SRC="${1:-}"
OUT="$(cd "$(dirname "$0")/.." && pwd)/assets/dmitri-portrait.jpg"
TARGET_W=1400   # comfortably above the 1024 the layout asks for

if [ -z "$SRC" ] || [ ! -f "$SRC" ]; then
  echo "usage: $0 <path-to-image>" >&2
  exit 1
fi

W=$(sips -g pixelWidth "$SRC" | awk '/pixelWidth/{print $2}')
H=$(sips -g pixelHeight "$SRC" | awk '/pixelHeight/{print $2}')
echo "source: ${W}x${H}"

if [ "$W" -lt 1024 ]; then
  echo "warning: only ${W}px wide — the layout wants 1024px. It will look soft." >&2
fi

TMP=$(mktemp -t portrait).jpg
if [ "$W" -gt "$TARGET_W" ]; then
  sips --resampleWidth "$TARGET_W" "$SRC" --out "$TMP" >/dev/null
else
  cp "$SRC" "$TMP"
fi
sips -s format jpeg -s formatOptions 85 "$TMP" --out "$OUT" >/dev/null
rm -f "$TMP"

NW=$(sips -g pixelWidth "$OUT" | awk '/pixelWidth/{print $2}')
NH=$(sips -g pixelHeight "$OUT" | awk '/pixelHeight/{print $2}')
echo "wrote:  $OUT  (${NW}x${NH}, $(du -h "$OUT" | cut -f1))"
echo
echo "If the framing is off, adjust object-position in links/index.html (.c-photo img)."
