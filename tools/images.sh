#!/usr/bin/env bash
# Make every image in images/ readable by AI agents.
#
# Agents cannot open JPEG XL (.jxl) files. macOS can, so this converts any .jxl into a
# downscaled .jpg next to it. The .jxl stays as the archival original; the .jpg is what
# agents actually read.
#
#   ./scripts/images.sh          # convert anything missing or out of date
#   ./scripts/images.sh --force  # reconvert everything
#
# Longest edge is capped at 2000 px — plenty to read a motor label, small enough to keep
# the repository light.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MAX_EDGE=2000
force=0
[[ "${1:-}" == "--force" ]] && force=1

command -v sips >/dev/null || { echo "needs macOS 'sips' to decode .jxl" >&2; exit 1; }

shopt -s nullglob nocaseglob
found=0
while IFS= read -r -d '' src; do
  found=1
  dst="${src%.*}.jpg"
  if [[ $force -eq 0 && -f "$dst" && "$dst" -nt "$src" ]]; then
    echo "up to date  ${dst#$ROOT/}"
    continue
  fi
  sips -s format jpeg -s formatOptions 80 -Z "$MAX_EDGE" "$src" --out "$dst" >/dev/null
  echo "converted   ${dst#$ROOT/}  ($(du -h "$dst" | cut -f1))"
done < <(find "$ROOT/images" -type f -iname '*.jxl' -print0)

[[ $found -eq 0 ]] && echo "no .jxl files found — nothing to do"
exit 0
