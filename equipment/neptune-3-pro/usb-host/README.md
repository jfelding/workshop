# Controllable Neptune USB host

`host.py` is the single serial owner. `control.py` submits requests through the job's
filesystem queue; it never opens the serial port. Use the scripts copied into the
running job so code changes do not affect an active print. No automatic reconnect,
replay, or recovery after resets/disconnects. An existing job state refuses a second
launch. Explicit user authorization and confirmed empty/clean bed are required for a
new job; read `../README.md` first.

Launch with the existing pyserial environment and detached log/caffeinate procedure:

```sh
/tmp/neptune-print-venv/bin/python -u JOB/host.py --job JOB --port <device from ls /dev/cu.*>
```

Replace `JOB` with the job directory:

```sh
python3 JOB/control.py --job JOB speed --percent 100
python3 JOB/control.py --job JOB query
python3 JOB/control.py --job JOB pause
python3 JOB/control.py --job JOB resume
cat JOB/status.json
```

Speed is a firmware multiplier (`M220`), accepted from 25–200%, applied to the speeds
in the sliced G-code (100% = as sliced). It also scales slower first-layer/wall speeds.
Do not increase flow to accompany a speed change. Requests apply between acknowledged
commands, so requests during homing/heating wait for that command to finish. The client
waits 15 seconds, then reports pending; inspect its named result before resubmitting.
Only an `ok: true` result proves the firmware acknowledged the change.

Pause waits for `M400` (motion buffer drained), leaves heaters on, and holds the same
in-memory job. Resume continues without homing. This is intended for short supervised
pauses; it does not support power-off, reset, lost position, filament-change parking,
or recovery after a physical/manual move. Do not use the printer screen's pause or
insert/remove cards during a USB job. Keep USB connected and the Mac awake/lid open.

`status.json` updates at least once per second of command progress or firmware response:
G-code file line, acknowledged command count, percentage, layer-change marker, planned
layer Z, feature, speed override, and temperature reports. Layer markers include
independently spaced support layers. Z is the sliced layer height, not a physical probe.
`query` returns `M105` temperatures and `M114` firmware position; movement can still be
buffered, so this position is not an exact mapping to a completed source line.

`progress.sqlite3` durably commits the last **sent** and last **acknowledged** source
command separately, on every G-code command, plus its serial sequence and G-code hash.
Read it while the host is running without opening the serial port:

```sh
python3 - <<'PY'
import json, sqlite3
from pathlib import Path
job = Path('scratch/neptune-pulley-extractor-20261006')
with sqlite3.connect(f'file:{job}/progress.sqlite3?mode=ro', uri=True) as db:
    print(json.dumps(json.loads(db.execute('SELECT data FROM checkpoint').fetchone()[0]), indent=2))
PY
```

Acknowledged means accepted by firmware, not necessarily physically executed. A
connection failure may leave buffered moves in flight and one sent command of uncertain
acceptance. Better records do **not** make automatic fault recovery safe.

The host drops unsupported `M73` display-progress commands, numbers/checksums remaining
commands, handles current-line resends, and fails on other firmware errors/unexpected
pause/cancel signals. Fault handling attempts quick-stop and heater/fan shutdown;
commands cannot reach a disconnected printer. No safety/leveling bypass commands.

Validation: seven fake-serial tests cover live speed/pause/resume dispatch, invalid
requests without serial writes, resend, thermal fault, end-of-job buffer drain, and
sent-versus-acknowledged checkpoints during disconnect. Hardware validation is recorded
in the journal; fake-serial tests do not prove all firmware failure behavior.
