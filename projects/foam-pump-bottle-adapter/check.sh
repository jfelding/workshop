#!/bin/sh
# Every check this project has; exits non-zero on the first failure. Run it before committing (CI does not).
set -e
cd "$(dirname "$0")"
python3 concepts/sketch.py concepts "${TMPDIR:-/tmp}" >/dev/null   # concept sketches; no parts yet
uv run python cad/pump_c_gauge.py
uv run python cad/hanging_collar.py --draft   # drop --draft once BRACKET_RING_FRONT_WIDTH is measured
uv run python cad/illustrate.py --draft        # the collar's view-*.png pictures
uv run python cad/amber_holder.py              # amber holder and ring: STL, STEP, part pictures
uv run python cad/amber_shim.py                # shim under the printed v4 ring
uv run python cad/amber_split_gauge.py         # split-ring bore gauge
uv run python cad/amber_strength.py            # beam hand-calcs; fails below safety factor 3
uv run python cad/amber_illustrate.py          # runs cad/amber_checks.py (fails on any clash), writes exports/preview.png and amber-*.png
uv run ws-check-pictures .   # every part has a picture and the README shows it
