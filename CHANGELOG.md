# Changelog

Versions of the `workshop` library (`src/workshop`). Knowledge files and projects are not versioned.

## Unreleased

- `workshop.fits`: first PETG process, `('neptune-3-pro', 'petg', 0.4)`. Hole shrink 0.15 mm (measured), and
  side-entry nut slots under a bridged ceiling: `slot_tight` (+0.1 AF, +0.4 height, measured) and `slot`
  (+0.3 AF, +1.0 height, untested). No `clearance` or `press` pocket for PETG yet (`materials/fits.md`).
- `cad` extra: build123d now comes from upstream `dev` through `[tool.uv.sources]`, locked at `ce36536f` in
  `uv.lock` (was 0.13.0 from PyPI). See `methods/cad-in-code.md`, "Keeping build123d current".

## 0.1.0 (2026-11-18)

First public version.

- `workshop.measure`: `mm()` and `dims()` refuse to build on an unmeasured dimension.
- `workshop.fits`: fit allowances per machine, material and nozzle, each with its evidence.
- `workshop.cad`: geometry primitives, `export` (one valid solid, with a picture), solid checks
  (`overlap`, `probe`, `overhangs`, `fits_bed`, motion envelopes), STL printability checks
  (`mesh_check`, `layers`), part pictures (`preview`, `ws-preview`) and guide-style renders.
- `workshop.guides`: the assembly-guide page kit.
- Tools: `ws-check-file-sizes`, `ws-check-pictures`, `ws-archive-logs`.
