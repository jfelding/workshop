# CAD in code

Custom parts are **Python scripts** using [build123d](https://build123d.readthedocs.io/), not drawings
made in a GUI. One script per part: run it, and it writes STL and STEP. `workshop.measure`,
`workshop.fits` and `workshop.cad` are the shared pieces. The worked example is
`projects/dyson-ontrac-bose-qc-ultra-adapter`.

## Why code

Our parts are adapters, brackets, plates, clamps and fixtures, and real hardware dictates their
geometry. That is where a script beats a sketch:

- When a measurement turns out 0.4 mm off, you change one number and every part that depends on it rebuilds.
  Nobody has to hunt through constraints.
- The design history sits in git next to the reasoning.
- An agent can revise a part from a measurement without anyone narrating mouse movements.

The GUI still has a job. Open the STEP in Fusion or FreeCAD to inspect, measure and test-fit.
Open the STL in the slicer before every print. The code is where a part is *defined*; the GUI and
the slicer are where it is *checked*.

## The one rule

**A project's `cad/measurements.py` is the only place a physical dimension is written down.**
Parts read every value through `workshop.measure.mm()`. It refuses to build on a value that is `None`, and
names the missing value. An unknown dimension stays `None` and is never given a plausible-looking guess.
It goes into `inventory/to-measure.md` with how to measure it. Never estimate it from a photo. A part that
will not build costs you two seconds; a part built on an invented number costs you a print.

```python
# cad/measurements.py
COVER_RIM_DIAMETER = 40.0   # calipers, 3 places, 2026-11-03
COVER_RIM_HEIGHT = None     # see inventory/to-measure.md

# cad/fixture.py
from workshop.measure import dims
import measurements as m
dim = dims(m)
pocket_d = dim('COVER_RIM_DIAMETER') + 0.3
```

Choices are not measurements. A project's free choices (a wall thickness, a chosen angle) go in
the same file under their own heading, or in a `design.py`. Either way they have names, and the reason
for each one is in a comment.

Fit allowances come from `workshop.fits`, not from a number typed into a part:
`hole_for(6.0, 'running')` and `nut_pocket(5.2, 2.1, 'press')`. Fits for an unmeasured process raise
an error just as `mm()` does. See `materials/fits.md`.

## The loop

```
measure the hardware → measurements.py → rebuild → print → measure the print → fits/measurements → rebuild
```

People skip the second half. Printed holes come out small and printed shafts large, by an amount
that belongs to the printer, nozzle and material. **The first print of a new fit is a measurement.**

That does not mean a test coupon for every fit:

- Prefer a cheap real part that carries the fit. On one build, an 8-minute gear that has the one
  bore that matters is both the test and a part we keep.
- A hole that comes out tight is reamed by twisting a drill by hand. That is faster and more accurate than
  reprinting.
- Reprint only when the geometry is wrong, not the size.
- A coupon earns its place only where neither of these helps. Heat-set insert bores are the obvious case.

## Checking a part against the solid, not the picture

The render and the STL preview hide exactly the mistakes that matter. `workshop.cad.checks` answers
with numbers:

- **Intersect, don't eyeball.** For every keep-out the part must clear, model the keep-out as a solid, and require
  `overlap(part, keepout) == 0`. An adapter cleared its keep-out in the render, but had buried
  about 450 mm³ in the nut. `assert_clear([...])` checks a list and fails the build on any overlap.
- **Probe the thin places.** `probe(part, p0, p1)` measures the material actually there at each hole, edge and
  floor. Quote the number with the probe's name. Hole spacing is not wall thickness. A probe
  under-reports by about its own step.
- **Printability.** Export only one valid solid (`export()` refuses anything else). The part must fit the bed:
  `fits_bed(part, BED)`, where BED comes from the machine's README. `overhangs(part)` gives the area
  steeper than 45°. Choose the orientation by computing that area. For a pair of sensor brackets, lying them on
  their side cut it from 102 to 13 mm², and they needed no supports.
- **Check the STL too.** `workshop.cad.printability` reads the exported mesh the slicer will see.
  `mesh_check(stl, parts)` asserts it is watertight, with that many parts, all on the bed.
  `layers(stl)` slices it into 0.2 mm layers and fails on any island that starts in mid-air. It also
  reports the area outside the 45° cone of the layer below, which catches what a face-angle check
  misses, such as lettering recessed into a sloping face.
- **Round-trip the inputs once.** When a part is built from a vendor STEP, re-read the dimensions it
  depends on from that STEP and compare them with `measurements.py`. Pin the STEP with its SHA-256 in
  `vendor/`.

Past these checks, don't gold-plate the part.

### Gotchas that cost a print or an afternoon

- **Boolean order.** A union filled a mounting bore. Cut bores **last**.
- **Tessellated STEP files have no true cylinders.** Fit radii from the facets. A D-flat does not show
  in a radius histogram; it shows in the angular spacing of the vertices.
- **Watertight.** A gear STL had open edges where a filled channel met a faceted bore. Check every export.
- **Read a fit report as a printer would.** A 0.3 mm gap was read as "clear". The printer resolves about
  0.4 mm, and the cheeks splayed into the gear. Design printed gaps at **0.8 mm or more**.
- **Horizontal holes** use `teardrop()`, so the roof prints without support. Ream them.
- **Ball seats.** Seat a ball in a 90° cone, not a hemispherical cup. The cone centres the ball whatever the
  printed size, so print error only moves the ball along the axis.

## Motion

For a part on a joint:

- **Rotary joint, every angle at once.** `revolution_envelope(part, axis, center)` turns the moving part into a stack of
  cylinders that contain it at every angle. Intersect that stack with the fixed parts.
- **Sampled joint.** Use `sweep_angles(lo, hi, 1.0)`. Sampling every 10–30° missed contacts that 1° found.
  Contact between samples is still possible when (step × largest moving radius) exceeds the
  clearance; flag those pairs instead of passing them.
- **Find the hard stops by search.** Report the angle where the parts first meet. Do not assume a range.
- **Linear travel.** Sweep the moving part along its axis as a prism, and read the first contact directly.

A full check script for a two-axis mechanism covers: φ as a swept envelope, θ at 1° up to the stops, gear
mesh over one tooth pitch, planned contacts at zero overlap, walls probed and parts on the bed. The
command exits non-zero on any failure, so CI and agents can rely on it.

## Layout of a project's `cad/`

| File | Holds |
|---|---|
| `measurements.py` | Every physical dimension, with the date and how it was measured, or `None` |
| `<part>.py` | One printable part, in print orientation. Calls `workshop.cad.export.export()` |
| `layout.py` | Derived positions shared by several parts. Only arithmetic on measurements |
| `checks.py` / `fit_check.py` | Overlap, probes, motion. Exits non-zero on failure. Writes `exports/checks.json` |
| `exports/` | Generated; never edit it, regenerate it. Pictures (`*.png`), `checks*.json`, `*.stl` and `*.step` are committed; G-code and 3MF are not |

Run with `uv run python cad/<part>.py` from the project directory.

**Every part gets a picture.** `export()` writes `exports/<part>.png` beside the STL: two views (from above and
from below), shaded, outlined, titled with the part's name and size. For an STL made another way, run
`ws-preview exports/<part>.stl`. Commit the pictures and show each in the README's parts table, under a picture
of the whole thing (`exports/preview.png`). Without them nobody can tell which file is which part, and a
reviewer cannot see a wrong part without building it. `ws-check-pictures` enforces this in `check.sh` and CI.

## Sharing a helper

When two projects need the same function, move it into `src/workshop/cad/` through a PR with a test (see
`CONTRIBUTING.md`). Primitives take dimensions as arguments and never hold one.
