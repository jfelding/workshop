#!/bin/sh
# New project from templates/project.
#   tools/new-project.sh <name> [owner]                 -> projects/<name>/ (workspace member)
#   tools/new-project.sh --own-repo <dir> [owner]       -> <dir>, its own git repo, pinned to the latest tag
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OWN=0
if [ "$1" = "--own-repo" ]; then OWN=1; shift; fi
[ -n "$1" ] || { sed -n '2,4p' "$0"; exit 1; }
if [ $OWN = 1 ]; then DEST="$1"; else DEST="$ROOT/projects/$1"; fi
NAME="$(basename "$DEST")"
OWNER="${2:-$(git config user.name)}"
DATE="$(date +%Y-%m-%d)"
[ ! -e "$DEST" ] || { echo "$DEST already exists"; exit 1; }
cp -R "$ROOT/templates/project" "$DEST"
find "$DEST" -type f ! -name '.keep' -exec sed -i.bak \
  -e "s/__NAME__/$NAME/g" -e "s/__OWNER__/$OWNER/g" -e "s/__DATE__/$DATE/g" {} \;
find "$DEST" -name '*.bak' -delete
if [ $OWN = 1 ]; then
  TAG="$(git -C "$ROOT" describe --tags --abbrev=0 2>/dev/null || echo v0.1.0)"
  sed -i.bak -e '/workspace = true/d' -e '/Inside the workshop repo/d' -e '/In a repo of its own/d' \
    -e "s|^# workshop = { git = \(.*\), tag = \"v[0-9.]*\" }|workshop = { git = \1, tag = \"$TAG\" }|" \
    "$DEST/pyproject.toml" && rm "$DEST/pyproject.toml.bak"
  git -C "$DEST" init -q
  echo "Made $DEST (pinned to workshop $TAG). Add a row to $ROOT/projects/README.md."
else
  echo "Made projects/$NAME. Add a row to projects/README.md, then: cd projects/$NAME && ./check.sh"
fi
