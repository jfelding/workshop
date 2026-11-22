#!/bin/sh
# Every check this project has; exits non-zero on the first failure. Run it before committing (CI does not).
set -e
cd "$(dirname "$0")"
uv run python cad/guard.py   # builds the guard, checks it against the switch, writes exports/
uv run ws-check-pictures .   # every part has a picture and the README shows it
