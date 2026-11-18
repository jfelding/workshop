#!/bin/sh
# Rebuild the parts and publish them as a GitHub release; run again to update the same release.
#   ./publish.sh            needs the GitHub CLI (gh), logged in, and a pushed commit
# Printing sites are listed in publish-state.json; their listings link back to this release.
set -e
cd "$(dirname "$0")"
NAME=dyson-ontrac-bose-qc-ultra-adapter
VERSION=$(sed -n 's/^version = "\(.*\)"/\1/p' pyproject.toml)
TAG="$NAME-v$VERSION"
./check.sh
ZIP="exports/$NAME-v$VERSION.zip"
rm -f "$ZIP"
zip -j -q "$ZIP" exports/dyson_half.stl exports/dyson_half.step exports/bose_half.stl \
  exports/preview.png images/worn-pair.jpg LICENSE README.md
FILES="$ZIP exports/dyson_half.stl exports/dyson_half.step exports/bose_half.stl"
if gh release view "$TAG" >/dev/null 2>&1; then
  gh release upload "$TAG" $FILES --clobber
else
  gh release create "$TAG" $FILES --title "Dyson OnTrac cushions on Bose QuietComfort Ultra, v$VERSION" \
    --notes "Print two of each part. Instructions: https://github.com/jfelding/workshop/tree/main/projects/$NAME

Licence: CC BY-NC-SA 4.0. The Bose half is a remix of Dr. Watt's earpad frame (https://makerworld.com/en/models/529246-bose-quietcomfort-ultra-earpad-frame)."
fi
URL=$(gh release view "$TAG" --json url --jq .url)
uv run python - "$TAG" "$URL" <<'PY'
import json, sys
from pathlib import Path
p = Path("publish-state.json")
state = json.loads(p.read_text()) if p.exists() else {}
state["github"] = {"tag": sys.argv[1], "url": sys.argv[2]}
p.write_text(json.dumps(state, indent=2) + "\n")
PY
echo "published $URL"
