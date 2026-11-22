# Journal

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
