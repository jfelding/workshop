#!/bin/sh
# Every check this project has; exits non-zero on the first failure. Run it before committing (CI does not).
set -e
cd "$(dirname "$0")"
uv run python cad/holder.py         # cup, key
uv run python cad/holder_mag.py     # mag_insert
uv run python cad/adapter.py        # strip adapters, test heads, offset adapters
uv run python cad/holder_side.py    # saddle, tail, assembly STEPs; overlap, lowering and hold checks
uv run python cad/remote_shell.py   # slim remote shell
uv run python cad/cup_slim.py       # cup for the slim shell
uv run python cad/render_side.py    # side_profile.png, side_front.png, adapter.png
uv run python cad/preview.py        # preview.png
if [ -f vendor/dewertokin-classic/CLASSIC_6_keys.STEP ]; then
  uv run python cad/fit_remote.py   # remote_fit.png (needs the manufacturer STEP, not in git)
else
  echo "skipping fit_remote.py: download the STEP named in vendor/dewertokin-classic/README.md"
fi
uv run ws-check-pictures .   # every part has a picture and the README shows it
