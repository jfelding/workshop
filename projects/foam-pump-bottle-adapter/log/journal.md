# Journal

## 2026-11-19 Project started

From the workshop repo's templates/project.

## 2026-11-19 Brainstorm

Four photos from Jacob (in `images/`). Read of the problem: the brown bottle's narrow neck passes the bracket
hole but the foaming pump's thread is much wider; the clear square bottle fits the pump but its neck does not
pass the hole. Sketched three concepts (`concepts.md`): nested thread sleeve, stacked step-up adapter,
two-part through-hole coupler. No dimensions taken from the photos.

## 2026-11-19 First measurements

Jacob, calipers: black bracket hole 32.7, stainless bracket (same kind) 33.0; brown neck 27.5 over threads,
bore 21.3; clear neck 39.0 in grooves, about 42.15 over threads; pump A (translucent head) 31.45 widest below
the collar; pump B (all white) 21.1. Pump B does not screw onto the clear bottle. Concept 4 (clip-on fork)
was dropped at Jacob's request before measuring. Consequence: pump A cannot enter the brown neck and leaves
no room for a tube through the hole; pump B on the brown bottle is the route to pursue.

Third pump (C), Jacob's favourite: collar 52 OD, body below the threads 32. Too wide for the brown neck; passes the hole by 0.35 mm per side. Concept 5 (slide-on saddle) written into concepts.md for it.

Pump C is the generic pump sold with "apothecary" amber glass foaming dispensers (same as the one listed at
glennavesoap.com/products/apothecary-glass-foaming-soap-dispenser; listing text: about 8 fl oz, 2 1/2 in
diameter, 5 3/8 in tall with pump). Jacob owns the matching amber glass body; it is not at home, has a wide
opening and does not pass the bracket hole. No dimensions taken from the listing.

Pump C (black) does not screw onto the clear square bottle: the bottle's thread is slightly too narrow for it. So the saddle (concept 5) for pump C on the clear bottle is also a step-up: clear-neck thread below, pump C thread on top, measured from the pump's collar.

More from Jacob: pump C inside at its threads a bit more than 43.85 (awkward angle), collar wall about 2.25, collar depth about 14.6; clear neck bore 33.75, neck height 21.25, at most two thread ridges above each other. Saddle sketched (concepts/5-slide-on-saddle.svg).

Bracket sheet 1.55 (black), 1.35 (stainless); ring outer width about 50 on both. Clear neck pitch about 3.25 (hard to measure). Modelled `pump_c_gauge` (stepped plug, 43.2 to 45.2) to find pump C's inner thread diameter, since calipers cannot reach it.

Jacob cannot print the gauge now. New concept 6, hanging collar, needs no pump thread: collar under the ring hooked over its edge, bottle neck clamps against the ring, pump drops in. Modelled as a draft (`cad/hanging_collar.py --draft`), checks pass. Replaces concept 5.

Collar reshaped for looks: the outside is one plain cylinder (57 mm), lips fade out towards the back, chamfered base. `cad/illustrate.py` renders it in place from six angles; bottle body and pump head in those pictures are scenery, not measurements.

Jacob: the open fork is wrong for the glass body (agreed, withdrawn), and the holder should be minimally visible. Sketched concept 7: spine behind the bottle, foot under the base, closed neck loop under the pump collar.

## 2026-11-22
Jacob wants the holder for the amber glass bottle with the black foam pump. A web search gave only seller
figures (body 64-65 mm, 110 mm tall, 165 mm with pump, neck 43 mm, inner or outer unknown, sellers disagree
43 vs 45). None is a measurement, so no CAD yet: listed the calipers work in `inventory/to-measure.md` and
recorded the choice of concept 7 in `log/decisions.md`.

## 2026-11-22 Amber holder modelled from estimates
Jacob asked for a printable holder now, from estimates, to print, test and adjust. Estimates went into a
separate `EST_*` block in `cad/measurements.py`, each with its source and range; measured values untouched.
A fixed loop round the neck turned out to depend on exactly the unknowns (the bottle can only be tilted in if
the neck length and diameter are right within a few mm), so the loop became a loose ring round the base of the
pump collar with a dovetail key in a channel at the top of the spine. It is sized from the measured 52.0 collar
and never touches the neck. The holder is one 30 mm wide profile printed on its side, so all bending runs along
the layers. `cad/amber_checks.py` checks both parts against a stand-in bottle and pump: no overlap installed,
on the way in and out, or with the spout turned and pushed; and for bodies 62 to 68 mm and heights 107 to 113 mm.
Holder 54.5 cm³, ring 3.4 cm³ (both changed later the same day, below), no supports, no bridges, nothing steeper than 45°. Not printed.

## 2026-11-22 Amber holder strength
Jacob's loads: full bottle 6 N, a 30 N push on the pump head, a 20 N knock; PLA 45 MPa along the layers, 25 MPa
across, SF 3 or more. `cad/amber_strength.py` (in `check.sh`) does the beam hand-calcs on sections probed from the
solid. The 3 × 4 mm ring failed (30.7 MPa in hoop bending, SF 1.5) and is now 4 × 5 mm (14.1 MPa, SF 3.2). The
brace under the foot turned out unnecessary (root 12.2 MPa with Kt 1.5, SF 3.7) and was removed: holder now
109 × 87 × 30 mm, 46.3 cm³; ring 63 mm across, 4.9 cm³. All fit checks still pass.

## 2026-11-22 Amber holder glued, not screwed
Jacob will glue it up with montagelim, so the screw holes are gone; the flat back is the glue pad. Glue joint
check in `cad/amber_strength.py`: 30 × 109 mm, peak tension 0.066 MPa plus 0.011 MPa shear, SF 6.5 against a
deliberately low 0.5 MPa. With the holes gone the holder has no overhangs at all. A wider back plate (Jacob's
offer) was not needed and would fight the side-on print.

2026-11-22 (slicing). Sliced both parts with `pla-fast-0.4` (stock speeds, textured PEI 60 C, 210 C), no supports,
STLs as exported (holder on its side, ring upside down). Holder: 150 layers to Z 30, 32.1 g, Orca estimate 2 h 04 min.
Ring: 80 layers to Z 16, 5.4 g, 24 min. G-code in `scratch/amber_*-20261122/`, copied to the SD card as
`amber_holder.gcode` and `amber_ring.gcode`. Print the ring first (it is quick and tests the fit on the pump collar).

## 2026-11-22 (first holder print)
Jacob printed the holder in PLA and sent photos of the spine's top end. The dovetail channel's sloped roof flank
(the 50 degree overhang, printed on its side) came out ragged with sagged blobs; the opposite flank and the
floor are clean, the layers and the rest of the body look good. Jacob does not want to reprint: the channel
can be cleaned with a hobby knife or small file, and the ring's key is made slimmer to allow for it.
Ring change: `KEY_EXTRA_SLACK = 0.5` per side on top of the fits slide play (0.4 -> 0.9 per side). Everything
else, including the holder STL, is unchanged. Resliced as `scratch/amber_ring-v2-20261122` (23 min, 5.1 g) and put on
the SD card as `amber_ring.gcode`; the first slice is kept as `amber_ring_v1.gcode`. Next time the holder is
printed: the channel's roof flank will need a shallower angle (flare 1.2 gives 50 degrees from flat) or a
sacrificial support; then drop `KEY_EXTRA_SLACK`.
