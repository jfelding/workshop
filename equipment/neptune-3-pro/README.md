# Elegoo Neptune 3 Pro

Owner: Jacob. A bed-slinger FDM printer, sliced with **OrcaSlicer 2.4.2** on
the Mac. Jobs are printed over USB by an agent-run host, or from the SD card by a person.

## Rules (agents and people)

- **Start a print only when a person asks**, after they confirm three things: the printer is idle, the
  bed is clear and clean, and the right filament is loaded. A USB connection does not mean the printer
  is ready.
- **Check for a running job first.** Never open the serial port, start a second host, or re-slice into
  a running job's directory while a host is running:
  ```sh
  ps aux | grep -i "host.py\|stream.py" | grep -v grep
  ls -d */scratch/*/ scratch/*/ 2>/dev/null; cat scratch/*/status.json 2>/dev/null | grep -i state
  ```
  A job a person started **from the SD card** leaves no trace on the Mac. Ask before assuming the
  printer is idle.
- **Leave a running print alone.** Do not poll it or watch its logs unless asked (preference, 2026-10-17).
- Slice at the stock speeds in `profiles/pla-fast-0.4`, not slower. The firmware has no input shaping
  (vibration compensation), so do not go faster either.
- After the print, measure it and record the outcome in your project's journal. Record fit results in
  `materials/fits.md`.

## Machine facts

| | |
|---|---|
| Build volume | 230 × 230 × 280 mm in the machine profile (`BED` below, with a margin). The small-gears job stayed inside X 10–165, Y 0.5–184 |
| Firmware | Marlin 2.1.1 (built 2023-02-10). Saved bed mesh, enabled with `M420 S1` after `G28` |
| Serial | 115200 baud. The device `/dev/cu.usbserial-…` changes name every session: run `ls /dev/cu.*` each time |
| Bed | Textured PEI. Its worn patches lose small parts |
| Nozzles on hand | 0.4 (default), 0.3, 0.2 |
| Firmware quirks | Rejects Orca's `M73` progress lines (harmless, but the screen's % is wrong). `exclude_object=0` |
| Flow ceiling | About **9 mm³/s** of PLA in practice. To print faster than a profile allows: slice with Orca's volumetric flow capped at 3 mm³/s, then insert `M220 S300` at layer 4 and `M220 S100` at shutdown (first three layers at 100 %). Peak commanded flow 9.0 mm³/s; acceleration still limits it, so it is not 3× faster. Remove the `M73` estimates, which become wrong. First used 2026-10-13 |
| Time | Orca's estimate is within a few percent at 100 %. Hand estimates ran 2–3× low, so slice before quoting a time |

```python
BED = (220, 220, 270)   # usable margin inside the 230 × 230 × 280 profile; checks.fits_bed(part, BED)
```

## Profiles

Each directory under `profiles/` holds a flattened, CLI-ready Orca set: `machine.json`,
`process.json` and `filament.json`. **A profile that a printed part's provenance relies on is never edited.**
To change one, copy it to a new directory and record why in its README.

| Profile | Nozzle / layer | Use |
|---|---|---|
| [`pla-fast-0.4`](profiles/pla-fast-0.4/) | 0.4 / 0.2 | **Default.** Orca's stock Neptune speeds, 20 % gyroid, textured PEI 60 °C |
| [`petg-pro-fast-0.4`](profiles/petg-pro-fast-0.4/) | 0.4 / 0.2 | PETG at the same speeds. No outcome recorded |
| [`pla-precise-0.4`](profiles/pla-precise-0.4/) | 0.4 / 0.2 | Older slow profile: 4 walls, 40 % gyroid. Take its walls, not its speeds |
| [`pla-fine-0.3`](profiles/pla-fine-0.3/) | 0.3 / 0.15 | 7 Arachne walls. Start here for a 0.3 nozzle |
| [`pla-small-0.2`](profiles/pla-small-0.2/) | 0.2 / 0.10 | Small exact parts, solid infill. Start here for a 0.2 nozzle |

For another nozzle: start from the saved profile for that nozzle, set the speeds from
`pla-fast-0.4`, and save the working set as a new profile directory.

## Slice

Use a **new job directory** for every job, in the project's git-ignored `scratch/`. Never reuse
one: it is the record of what was printed.

```sh
set -e
JOB="$PWD/scratch/my-part-$(date +%Y%m%d)"; mkdir "$JOB"
P=<this repo>/equipment/neptune-3-pro
cp $P/profiles/pla-fast-0.4/*.json $P/usb-host/host.py $P/usb-host/control.py "$JOB/"

/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer \
  --debug 3 --logfile "$JOB/slice.log" \
  --load-settings "$JOB/machine.json;$JOB/process.json" \
  --load-filaments "$JOB/filament.json" \
  --arrange 1 --orient 0 --ensure-on-bed --slice 0 \
  --export-3mf job.3mf --outputdir "$JOB" \
  cad/exports/my_part.stl
```

Before printing, check the G-code:

- layer count and top Z;
- every object present;
- heater targets;
- `G28` and then `M420 S1` at the start;
- heaters and fan off at the end;
- moves inside the bed.

Do not bypass endstops, thermal protection or levelling to get a job running.

### Orca CLI pitfalls

1. System profiles inherit from parents. To flatten one, merge the parents recursively, but **keep
   `inherits`, and `compatible_printers` on process and filament**, or Orca reports "process not compatible
   with printer".
2. Default bed type is Cool Plate (35 °C). Set `curr_bed_type` to "Textured PEI Plate" (60 °C).
3. A relative `--outputdir` produces the G-code but fails the 3MF export. Use an absolute path.
4. The CLI has no OpenGL, so the G-code carries no thumbnail. This is harmless.
5. The start G-code sets `G21 G90 M83` explicitly and caps the first travel at 50 mm/s.
6. **Layer 1 interior-first:** Orca 2.4.2 ignores `is_infill_first` on layer 1. Run
   `reorder_first_layer.py` in the job directory after slicing. It moves layer 1's bottom surface ahead of its
   walls, and checks that the extrusion events are unchanged. This is for flat parts with fine
   layer-1 detail, such as gear teeth.

## Print over USB

`usb-host/host.py` is the only program that owns the serial port. `control.py` sends speed, query,
pause and resume requests through the job's file queue, and never opens the port. Details are in
[`usb-host/README.md`](usb-host/README.md).

```sh
uv venv /tmp/neptune-print-venv && uv pip install --python /tmp/neptune-print-venv pyserial
export JOB PORT=/dev/cu.usbserial-XXXX     # from ls /dev/cu.*
python3 - <<'PY'
import os, subprocess
from pathlib import Path
job = Path(os.environ['JOB']).resolve()
with (job / 'stream.log').open('x') as log:
    p = subprocess.Popen(['caffeinate', '-i', '/tmp/neptune-print-venv/bin/python', '-u',
                          str(job / 'host.py'), '--job', str(job), '--port', os.environ['PORT']],
                         stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
(job / 'stream.pid').write_text(str(p.pid)); print('host PID', p.pid)
PY
```

**This starts a physical print.** Before running it, confirm the printer is idle, the bed is clear and
the job directory is new. Keep USB connected and the Mac lid open.

- The host numbers each line with a checksum, waits for every `ok` and handles resend requests. If it
  hits an error, it quick-stops and turns the heaters off.
- After a reset or disconnect there is no recovery. Never restart a host against a half-printed part.
- `printing` in `status.json` means the host is sending, which includes heating and homing.
  `completed` means every line was acknowledged. Neither tells you anything about print quality.
- Speed: `control.py --job JOB speed --percent 200` applies `M220` from 25 to 200 %. A pattern that
  worked: 100 % for the first 3 layers, then 200 %. Speeding a small part up 2.5× does not make it
  2.5× faster, because layer-time cooling limits it.
- Firmware queries (`M115`, `M105`, `M27`, `M119`, `M420 V`) need the port too. Never send them
  while a host owns the printer. `M27` reports SD printing only, so it does not prove the printer is idle.

## Print from the SD card

Slice as above, check the G-code, and hand the person the `.gcode`. Use this for long overnight parts.
