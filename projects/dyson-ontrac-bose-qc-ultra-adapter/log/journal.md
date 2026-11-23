# Journal

## 2026-11-22 Wide Bose half (not printed)

New part `bose_half_wide` (`cad/bose_half_wide.py`): `bose_half` (frame mesh plus the mirrored pin pockets) with a flat
rim added only outside the frame's oval, between the oval and the outline of `dyson_half_wide` (same `outline()`, so
`COVER_RADIUS` and `OUTLINE_BLEND_RADIUS` are shared). Read from the frame mesh: glue face z = 0, flat plate to z = 2.0,
outer wall vertical and sharp, no edge treatment, so the rim has 0.3 mm chamfers on both outer edges and reaches 0.4 mm
into the plate for a clean union. The owner checked the earcup by eye: room at the sides. Fit otherwise unverified.
- Glued wide pair: overlap 0.0 mm³, outline mismatch 0.0 mm, pins clear, stack 9.7 mm, bulge 41.49 mm on both sides of both
  halves. Volume added vs `bose_half`: 320.6 mm³; proven material removed 0.0; nothing added inside the oval less 0.5 mm.
- First layer 2356 mm², overhang area 10.24 mm² (unchanged), no islands in mid air, 83.0 x 96.5 x 5.0 mm.
- Proven parts unchanged: `dyson_half` 4885.608 mm³, `bose_half` 4649.710 mm³, STLs byte-identical.
- Pictures: `exports/bose_half_wide.png`, `exports/preview_wide.png` (`preview.png` still the published pair).

## 2026-11-22 Detent test part sliced to SD

`dyson_half_detent` (wide plate plus bumps, one copy) sliced with `pla-fast-0.4` in OrcaSlicer: 23 layers,
6.16 g, 25m 48s estimated. On the SD card as `dyson_detent.gcode`; job record in
`scratch/dyson-half-detent-20261122-1638/`. Not printed yet. Trial-fit on the Bose earcup before gluing.

## 2026-11-22 Looked for reference geometry of the original lock

Searched for a model or photo of the Dyson side, to improve on the wedge-only lock. Nothing is built or
changed yet.

- No 3D model of the cushion ring or the earcup lugs exists on Thingiverse, MakerWorld, Thangs, Cults3D,
  GrabCAD, Yeggi or STLFinder (Printables' list would not load). The only OnTrac hit is this adapter.
  AliExpress and Alibaba sell no third-party OnTrac cushions, only Zone pads shown from the front.
- Dyson's instructions: "Push down and twist clockwise, until it clicks into place"; anticlockwise to
  remove. So the original has a detent of some kind. A Dyson community reply reportedly says Zone and
  OnTrac cushions share the connection (search snippet only, page not read).
- One photo shows the bare earcup: "dyson-ontrac-earcups-removed-2" in
  https://www.androidpolice.com/dyson-ontrac-review/ (4480 x 2520; not copied here, it is their photo).
  Read from it, not measured:
  - four black lugs with outward lips, two long and two short, alternating;
  - the long lugs are long thin ribs along most of the slot with the hooked part only at one end; ours
    are 9 mm hooks in all four slots;
  - the short lugs are compact blocks with an overhanging top;
  - no separate spring, clip or magnet can be made out. Possible detent features, unconfirmed: a small
    pip at one end of a short lug's top face, a small tick halfway along one long rib, a step in the
    other long rib.
- Still unknown: what makes the click. The mating feature must be on the cushion ring, so a close-up of
  a slot and the underside of its ledge would settle it.

- Later the same day, two better photos: the right earcup bare
  (`~/code/3d-projects/dyson-ontrac-bose-qcu-adapter/images/dyson-ontrac-cup-right-no-cushion.jpg`) and the
  cushion back straight on (`~/Downloads/PXL_20261117_153821423~2.jpg`). Read from them, not measured:
  - cushion: each ledge is a bar along the outer edge of its slot, standing proud of the ring, with a
    raised cap at both ends. It is fixed at both ends, not a spring arm. The grey dots in the long slots
    look like glue or stake points in the fabric, not detent holes;
  - earcup: the short lugs are T-shaped (lip wider than stem); the long lugs are a thin rail with a wider
    lip over part of the length. Each lug sits in an outlined, apparently recessed window in the face;
  - no spring part on either side. Working guess for the click: the proud ledge bar drops into the
    recessed window beside the lug at the end of the twist. Unproven.
  - Idea for the adapter: a low ramped bump on the relief step that a ledge bar's end cap rides over just
    before home. Needs the bar's end angles and radial span first (`inventory/to-measure.md` when started).

## 2026-11-18 Published

Cleaned up for publication: only the working version is kept. The Dyson half was rewritten from CadQuery
to build123d on the workshop library and compared with the STL that was printed and is in use: volume
4885.6 against 4885.9 mm³, 0.30 mm³ present in one and not the other, 0.002 mm³ the other way (mesh
rounding at the bore). The Bose half is identical to the printed one (difference 0.0 mm³ both ways).

## 2026-11-17 It works

Twelfth test print. Printed in PLA on the Neptune 3 Pro (`pla-fast-0.4`), glued, fitted to both ears.
The cushions drop on, twist about 16° and clamp. What the eleven before it taught is in
`methods/lessons.md` in the repo root: the plate must not rest on the cushion's proud ledge blocks, a
sloped lip underside lets go, a barbed lip does not print, the long slots need a thinner stem (1.4 mm),
and the Bose half's pin pockets must be mirrored because that half is turned over for gluing.

## 2026-11-16 Measured

Cushion slots measured with calipers; Bose frame measured from Dr. Watt's model. Left and right
cushions confirmed identical. Values in `cad/measurements.py`.

## 2026-11-22 Detent test variant, from photo values (not printed)

Added `cad/dyson_half_detent.py`: `dyson_half.make()` unchanged plus a low ramped bump on the relief step
under each of the two LONG ledge bars. Exported as `dyson_half_detent`; `dyson_half.stl` is byte-identical to
before (volume 4885.608 mm³). Owner-approved exception to "never guess from a photo": the bar angles and radii
are read from `PXL_20261117_153821423~2.jpg`, listed in `inventory/to-measure.md`.

- Photo scale 28.22 px/mm from `SLOT_OPPOSING_SPAN`; slot chords come out 33.3 (measured 33.5) and 22.0 (22.4).
  The photo is turned +47.5° from `SLOT_ANGLES` with the same handedness (scatter ±1°; mirrored it is 18°).
- Bars: about 15.5° (10 mm) long, 14.5° (short), starting at each slot's closed end, radii about 38.1-39.3 mm.
  Bump on the long pair only: the short slots are where the plate is narrowest.
- Finding: the bars are about as long as the twist (15.5° against 16°), so any bump in their path is under a bar
  at drop-on, and the wedge leaves the cushion only 0.2 mm of lift 6° before home and 0 at home. The bar clears the
  relief by 0.2 mm. So: bump 0.4 mm (0.2 mm interference), crest 7° before home, click about 6° before the stop;
  a bump at home itself cannot be passed. Sweep in `exports/checks.json` (`detent_sweep`): interference 0.2 mm
  from drop-on to 6.5° before home, zero from 5.5° on, margin to the wedge slack 0.065 mm (assumes a 0.8 mm
  ledge slab). Untested.

## 2026-11-22 Wide plate test variant (not printed)

New part `dyson_half_wide` (`cad/dyson_half_wide.py`): the proven hooks, seat and pin holes under a new outline, the
Bose oval united with a circle of `COVER_RADIUS` (hard ring 41.1 + 0.4) and a 40 mm blend fillet, so the plate
covers the cushion's hard ring at the sides. `dyson_half_detent` is now built on it. `dyson_half.stl` is
byte-identical (4885.608 mm³; everything above the seat top is identical in the wide part, 284.929 mm³ both).
- Ring read from the cushion photo at 72 angles (28.22 px/mm): circular, centre within 0.1 mm of the slot circle, radius 41.13,
  scatter 0.12 (41.0-41.4); uncertainty +/-0.4. Photo-derived, in `inventory/to-measure.md`.
- Overhang beyond the oval: max 2.5 mm at the short axis, about 72° of arc on each side. 83.0 x 96.5 x 4.7 mm.
- The narrow oval ends 0.1 mm inside the short bars' outer face (-0.09/-0.14 mm), which is the "does not cover the ring"
  complaint in numbers; the wide plate leaves 2.2 mm. The bars clear the plate everywhere in the sweep (0 mm³).
- Judged from `on-earcup.jpg`, `worn-pair.jpg`, `adapter-in-cushion.jpg`: nothing on the Bose earcup at that height that the
  bulge would hit (the cup shell is about the cushion's width). Unverified.
- First layer 3033 mm² (2868 narrow), overhang 10.80 mm² (unchanged), no islands in mid air.

## 2026-11-22: first detent slice had no bumps

Checked the G-code of the first `dyson_half_detent` slice: nothing was extruded at radius 38.2 to 39.0 on
layers z 1.4 and 1.6. The profile uses the classic wall generator with thin-wall detection off, so a
0.8 mm wide feature (under two 0.42 mm lines) is dropped. Widened the bumps to the full bar span, 38.1 to
39.3 (1.2 mm). Re-sliced into `scratch/dyson-half-detent-20261122-b`: both bumps now print as an outer-wall
loop on both layers; 23 layers, 6.16 g, 25m48s. The first file (`dyson_detent.gcode`) prints a plain wide
plate and should be replaced. Lesson: after slicing a small feature, check the G-code for extrusion there.

## 2026-11-23 Spring latch (not printed)

The owner printed the wide plate with the detent bumps: fits well, no lock at all. New parts `dyson_half_latch`
(`cad/dyson_half_latch.py`) and `bose_half_latch` (`cad/bose_half_latch.py`); `dyson_half` is unchanged (4885.608 mm³).
- One pawl per short slot: arm r 34.8 to 37.4, 17.4 mm long, 1.8 thick, cut free by a 0.8 mm U-slit; tooth 1.2 mm
  above the seat, lock face 62°, back face 75°, 2.1 mm wide (narrowed to r 35.3 at the tip, see below).
- Calculated (PLA 2500 MPa assumed): 1.79 N/mm, 2.14 N to press a tooth flat, peak strain 1.07 %, tip drop 1.33 mm
  against a 1.6 mm pocket. Untwist force at the tooth 5.6 N at friction 0.3 (4.5 at 0.2, 10.4 at 0.5), 0.40 N·m.
- Sweep, cushion face against the part, drop-on to the hard stop: both teeth flat from drop-on; A fully up from 0.87°
  before home, B from 0.73° after; both up at the hard stop (2.39° past). At nominal home B is still pressed 0.9 mm.
- The Bose frame's clips are not symmetric: one reaches r 34.65 under a pawl tip. First pocket cut 0.6 mm³ out of
  it. Fixed by narrowing the tooth to r >= 35.3 and stepping the pocket's inner wall to 34.75 there: 0 mm³.
- Sign slip caught by the sweep: the cushion's solid face is on the low-angle side of the slot's closed end, so a
  tooth placed "behind the wall" rises later, not earlier.
- Printability: 4957.9 mm³, first layer 2963 mm², overhang 10.80 mm² (as the wide plate), no islands. Bose half
  4640.3 mm³, pockets remove 330.0 mm³, roofs are bridges (186 mm²).
- The pins let the halves go together either way round, but the staggered teeth put the two arms 181.6° apart.
  Each pocket is therefore the envelope of both arms; the arm sweep is checked against the Bose half both ways (0 mm³).
- Sliced with stock `pla-fast-0.4` into `scratch/dyson-half-latch-20261123` (23 layers, 5.98 g, 26m48s) and
  `scratch/bose-half-latch-20261123-b` (25 layers, 5.63 g, 27m05s; the folder without `-b` has the earlier, one-way pockets, do not print it). G-code checked: both teeth extruded on every
  layer z 2.0 to 3.2 (5.6 mm of line on the top one), nothing extruded in the slits, arm top at z 1.8; the Bose
  pockets are empty from z 0.2 to 1.6 (2 x 99 mm²) and roofed at 1.8. The slicer turns the part 90° on the bed,
  and the Bose half prints mirrored (glue face down): a G-code check by angle has to allow for both.
