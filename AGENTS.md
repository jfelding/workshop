# AGENTS.md

The working agreement for AI agents in this workshop repo. Read `README.md` for the map. Read the
README of every machine you are about to touch. A project under `projects/` has its own `AGENTS.md`;
read that too. Where the two disagree, the project's file wins for that project.

## The user

The user is comfortable with electronics and software but is not a professional engineer in either.
- Spell a term out the first time, e.g. "Arachne (Orca's variable-width wall generator)".
- Say briefly *why* a choice matters.
- Do not dumb the engineering down.

Units are metric and prices are in DKK. Be direct and decisive. Do not hedge everything.

## Machines: what needs a person

- **Neptune 3 Pro.**
  - Start a print only when a person asks, after they confirm the bed is clear.
  - Never open the serial port while a host is running or a print is going (`equipment/neptune-3-pro/README.md`).
  - Leave running prints alone.
  - Slice at stock speeds.
- Never bypass endstops, thermal protection, interlocks or limit switches. Flag anything that would.

## Designing parts

- Follow `methods/cad-in-code.md`. Every physical dimension comes from the project's `measurements.py` through
  `workshop.measure.mm()`.
- An unmeasured value stays `None` and goes into `inventory/to-measure.md`. Never guess it from a photo or a web page.
  Measure interfaces from vendor STEP files.
- Size fits with `workshop.fits`. If it raises `Uncharacterised`, say so, and propose a cheap real part to measure
  the fit. Do not invent a number.
- Check against the solid: overlap volume, wall probes, motion sweeps, bed fit and overhang area.
  Report the numbers.
- **Pictures, always.** A person cannot tell `clamp_side_plus_y.stl` from `clamp_lever.stl` by name. Every
  exported part gets a 3D picture beside it (`exports/<part>.png`, from above and below, titled with name and
  size). `workshop.cad.export` writes it; for an STL written another way, call `workshop.cad.preview.preview`
  or run `ws-preview`. Commit the pictures. Each project README opens with a picture of the whole thing
  (`exports/preview.png`) and has a parts table showing every part's picture. Re-export and commit when a part
  changes. `ws-check-pictures` (in every `check.sh`; CI runs the `--committed` form) fails without them.
- Look at the pictures you made before you report a part as done.
- Look at photos of the real hardware before reasoning about physical fit. Ask for a photo when it would settle
  a question faster. Use JPEG only (`tools/images.sh`).

## Changing this repo

- See `CONTRIBUTING.md`.
- `src/workshop/` changes go through a PR with a test and a CHANGELOG entry.
- Knowledge files, new profiles and lessons may go straight to main.
- Never edit a proven profile; copy it.
- When you learn something reusable while working in another repo, add it here: a number in `materials/`
  and `fits.py`, or a lesson in `methods/lessons.md`. Use the right tag and a date.
- Keep files under 800 lines (`ws-check-file-sizes`). Give a new feature its own module.
- Keep docs about the current state. History goes in `log/journal.md` (append with a heredoc) and choices
  go in `log/decisions.md`.
- Several agents may work at once. Commit only your own paths, and re-read a shared file just before editing it.
- If it matters and was only said in chat, write it into a file.
