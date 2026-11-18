# AGENTS.md

Read the workshop repo's `AGENTS.md` first. Its machine rules (print only when asked) apply here. Then read `README.md`, `log/status.md` and `log/todo.md`.

## This project

<The question or goal, in two sentences. The one measure that says the work moved.>

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
