# Changelog

Versions of the `workshop` library (`src/workshop`). Knowledge files and projects are not versioned.

## Unreleased

## 0.1.0 (2026-11-18)

First public version.

- `workshop.measure`: `mm()` and `dims()` refuse to build on an unmeasured dimension.
- `workshop.fits`: fit allowances per machine, material and nozzle, each with its evidence.
- `workshop.cad`: geometry primitives, `export` (one valid solid, with a picture), solid checks
  (`overlap`, `probe`, `overhangs`, `fits_bed`, motion envelopes), STL printability checks
  (`mesh_check`, `layers`), part pictures (`preview`, `ws-preview`) and guide-style renders.
- `workshop.guides`: the assembly-guide page kit.
- Tools: `ws-check-file-sizes`, `ws-check-pictures`, `ws-archive-logs`.
