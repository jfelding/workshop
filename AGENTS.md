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

## Other people's models

This repo is public and as open as it can be: code is MIT, our own design files are CC BY 4.0.

- Publish someone else's model, or a part made from it, only when its licence allows redistribution. Read the
  licence on the model's page; "free to download" is not a licence. If it does not allow it, keep the file out
  of git and out of every upload, and have the README tell the reader where to download it.
- When it is allowed, credit it: author, title, link, licence and what was changed, in the project README and
  in a `vendor/<model>/README.md` beside the original file with its SHA-256.
- A part derived from such a model keeps that model's licence (a share-alike or non-commercial term carries
  over). Say so per part; do not let it restrict the parts that are our own.
- Measuring a model to fit against it is fine and needs no licence. Say where the number came from.

## Publishing a project

Hobby projects go on Printables, MakerWorld and Thingiverse. Keep it loose: these are experiments, not products.

- Short and sweet. Why I made it, how to print it, how to put it together, what I would change. Details live
  in the README; link it.
- Write it the way a person would. No sales pitch, no list of rules or warnings, no AI-sounding filler.
- The text lives in the project's `listing.md`, the live pages in `publish-state.json`. Sites differ a little
  (title limits, categories, tags); adapt and move on.
- Real photos first, then the part pictures.

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
