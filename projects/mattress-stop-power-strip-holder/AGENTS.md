# AGENTS.md

Read the workshop repo's `AGENTS.md` first. Its machine rules (print only when asked) apply here. Then read `README.md`, `log/status.md` and `log/todo.md`.

## This project

Hold an Elworks 6-way power strip and a DewertOkin CLASSIC bed remote on the mattress stop of an adjustable bed. Done when the strip and remote stay put through daily plugging and unplugging.

## Rules

- Dimensions are still constants at the top of the scripts (see `log/decisions.md`); port them to `cad/measurements.py` and `workshop.measure.mm()` at the next redesign. An unmeasured value goes in `inventory/to-measure.md`.
- Fits come from `workshop.fits`. When you measure a new fit, add it to the workshop repo.
- Logging: `log/journal.md` (append, dated), `log/decisions.md` (made choices),
  `log/status.md` (snapshot), `log/todo.md` (next, ordered). See methods/agent-workflow.md.
- **Pictures, always.** Every part has a 3D picture (`exports/<part>.png`, written by `workshop.cad.export`
  or `ws-preview`), committed and shown in the README's parts table, with `exports/preview.png` of the whole
  thing at the top. A file name alone tells a person nothing. `./check.sh` fails without them. Re-export
  and commit the pictures whenever a part changes.
- Photos of the real thing go in `images/`, as JPEG.
