# AGENTS.md

Read the workshop repo's `AGENTS.md` first. Its machine rules (print only when asked) apply here. Then read `README.md`, `log/status.md` and `log/todo.md`.

## This project

A one-head version of DrJones's print-in-place Oral-B head case (CC BY 4.0, vendor/oralbox2/), made by cutting one
lane out of the two-head file. Done when a printed case opens and closes cleanly and holds a head without rattling.

The part is cut from a mesh, not modelled: change it in `cad/single_case.py` and keep the credit in the README.

## Rules

- Every physical dimension is in `cad/measurements.py`, read through `workshop.measure.mm()`. An unmeasured
  value is `None` and listed in `inventory/to-measure.md` (methods/cad-in-code.md).
- Fits come from `workshop.fits`. When you measure a new fit, add it to the workshop repo.
- Logging: `log/journal.md` (append, dated), `log/decisions.md` (made choices),
  `log/status.md` (snapshot), `log/todo.md` (next, ordered). See methods/agent-workflow.md.
- **Pictures, always.** Every part has a 3D picture (`exports/<part>.png`, written by `workshop.cad.export`
  or `ws-preview`), committed and shown in the README's parts table, with `exports/preview.png` of the whole
  thing at the top. A file name alone tells a person nothing. `./check.sh` fails without them. Re-export
  and commit the pictures whenever a part changes.
- Photos of the real thing go in `images/`, as JPEG.
