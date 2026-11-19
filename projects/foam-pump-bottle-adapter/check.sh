#!/bin/sh
# Every check this project has; exits non-zero on the first failure. Run it before committing (CI does not).
set -e
cd "$(dirname "$0")"
python3 concepts/sketch.py concepts "${TMPDIR:-/tmp}" >/dev/null   # concept sketches; no parts yet
uv run python cad/pump_c_gauge.py
uv run python cad/hanging_collar.py --draft   # drop --draft once BRACKET_RING_FRONT_WIDTH is measured
uv run python cad/illustrate.py --draft        # exports/preview.png and the view-*.png pictures
uv run ws-check-pictures .   # every part has a picture and the README shows it
