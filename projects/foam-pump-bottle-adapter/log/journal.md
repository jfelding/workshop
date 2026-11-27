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

2026-11-22 (ring v3). Jacob: the ragged channel flank is the right side seen from above when the holder hangs
(front view, looking at the wall) = design +x = the roof flank when printed on its side, as inferred. The key is
now slimmer on that flank only: `KEY_EXTRA_SLACK` 0.8 mm normal to the flank on +x, the -x flank back at the
fits slide play 0.4 (v2 had 0.5 extra on both flanks). Key back depth is back to full. `check.sh` passes, no
overlaps. Resliced as `scratch/amber_ring-v3-20261122` (25 min, 5.3 g): SD card `amber_ring.gcode` is v3,
`amber_ring_v2.gcode` the symmetric one, `amber_ring_v1.gcode` the original.

2026-11-22 (ring, 100% infill). Jacob printed the first ring geometry (symmetric 0.4 mm key; the one-sided v3 key
is not used) with 100% infill: the job copy of `pla-fast-0.4` with `sparse_infill_density` 100%, job
`scratch/amber_ring-solid-20261122`, 5.85 g, 23 min 32 s (20% was 5.35 g, 23 min 39 s). Stock speeds, nothing else changed.
On the SD card as `amber_ring.gcode`. The STL is the one from commit 2418c5a; the branch's current `amber_ring.stl`
still carries the v3 one-sided key (`KEY_EXTRA_SLACK` 0.8).

## 2026-11-24 Amber holder v2 from measurements
Jacob: the printed holder and ring were too big in basically every dimension. With the bottle in hand he measured
body 65.0, table to collar underside 104 (pump on), collar 52.5 at its bottom edge, bare neck under the collar 43.5,
glass thread 44.0 (pump off), bare neck 17 mm tall. The 104 explains the ring: v1 put the ring's underside at 95,
so it hung round the ~43 neck with a 55 bore. Jacob proposed putting the ring on the neck under the collar instead.
v2: ring bore `hole_for(44.0, 'running')` = 44.5, wall 4, 6 tall, top 1 mm under the collar; air round the body
1.5 (was 3 plus a +3 allowance); channel flare 1.7, depth 3.5, roof 60° from flat; `KEY_EXTRA_SLACK` 0. Holder
112 × 81 × 30 mm, ring 52.5 across. `check.sh` passes; numbers in `log/status.md`. Not printed, not committed.

2026-11-24 (ring v2, sturdier). Jacob: on the first parts the key was slightly too small for the channel, so the
ring hung, and it sat slightly low; the space between ring and key was empty. Now: a solid trapezoid web from the
ring's back (40 mm wide) to 0.5 mm short of the spine face (26 wide), 9 mm tall, around the key; key 0.1 mm per
side oversize (`KEY_OVERSIZE`) and 0.5 mm long (`KEY_EXTRA_LENGTH`), filed to fit; checks use the key as filed
(`ring_fitted`). Ring 4.8 -> 7.7 cm³, key neck SF 9.1. Print the ring at 100% infill. Fit note added to
materials/fits.md (0.4 per side too loose for a load-carrying dovetail).

2026-11-24 (ring brace). Jacob meant the empty corner under the web, between the key's hanging lower end and the
web's underside (his marked screenshot). Added a triangular brace there, 16 mm wide, 1.2 horizontal per 1 vertical
(prints as a buttress upside down); web kept. Ring 8.2 cm³. check.sh passes, no overlaps.

2026-11-24 (slicing v2). `pla-fast-0.4`, stock speeds, textured PEI 60 C, 210 C, no supports, STLs as exported.
Holder: job `scratch/amber2_holder-20261124`, 150 layers to Z 30, 31.7 g, Orca 2 h 04 min. Ring: job
`scratch/amber2_ring-20261124`, job copy with `sparse_infill_density` 100%, 83 layers to Z 16.6, 9.8 g, 38 min.
G-code checked (G28 then M420 S1, 60/210, heaters and fan off at the end, moves inside the bed) and copied to the SD
card as `amber2_holder.gcode` and `amber2_ring.gcode`; the v1 files `amber_*.gcode` are still on the card.

## 2026-11-26 Ring v2 print: hits the shoulder, key too fat
Jacob printed `amber2_ring` and tried it (photos `images/amber2-ring-*.jpg`, pump off). (1) The web and brace on the
wall side hit the glass lower down, so the ring sits tilted, higher at the wall. (2) He had to file a lot off the key
(0.1 per side oversize) before it went into the channel. Cause of (1): the checks drew the shoulder as a straight
cone from z 78 to 87 on `AMBER_NECK_BARE_HEIGHT` 17. The photo shows the ring only a few mm above where the glass
starts to widen and a domed shoulder, so the 17 is doubted. The brace reached z 87 at r 25-33 and the web z 94.
Fix (v3 ring): brace and the 3 mm web drop removed; the web is now as tall as the ring, so nothing of the ring sits
below its underside inside the 65 body outline (checked: 0 mm³), and the shoulder's curve no longer matters as long
as the bare neck is at least 7. New checks: flat-shelf worst-case shoulder, and ring volume under its underside
inside the body. Ring 8.2 -> 6.4 cm³. Key unchanged until Jacob calipers the filed key. check.sh passes. Not sliced.

2026-11-26 (ring bore follows the neck). Jacob: the glass already curves out within the ring's own 6 mm height, so a
straight bore sits on its bottom edge. New measured table `AMBER_NECK_PROFILE` ((mm below collar, OD), ...), None
for now. When set, the bore follows it at the running fit's clearance (`hole_for(od, 'running')`), never narrower
than the 44.5 that passes the thread, and the stand-in glass uses the same points. New checks: wall at the ring's
underside (fails under 1.6, 4 perimeters) and whether the bore follows the neck. Tried with a made-up test profile
(not saved): bore 48.75 at the underside, wall 1.88, zero overlaps. Printed upside down the flare opens upwards,
so no overhang. With None the bore is straight and the build prints a note.

2026-11-26 (ring v3 from estimates). Jacob: no more measuring; adjust from estimates and print a few times if needed.
`EST_AMBER_NECK_PROFILE` from his two photos (scale from the ring, about 22 px/mm in the side view): 43.5 neck for the
first ~5 mm under the collar, then a band about 46.5 across and 5 tall right under the ring (the v2 ring's front was
sitting on its top edge), then a dome out to 65 about 26 below the collar. The bore follows it at the running fit plus
`NECK_PROFILE_MARGIN_UP` 1 mm: 44.5 at the top, 47.0 at the underside, wall 2.75. Checks with the whole profile 1 mm
higher (glass 0.4 mm short of lifting the ring) and 1.5 lower: zero overlap. Key `KEY_OVERSIZE` -0.15 (play per side;
v1 -0.4 hung, v2 +0.1 needed heavy filing); checks and strength now use the key as printed. Ring 6.0 cm³, hoop SF 3.1
(was 4.7, thinner wall at the flare), the rest unchanged. Sliced with the v2 ring's job settings (100% infill, stock
speeds): `scratch/amber3_ring-20261126/plate_1.gcode`, 83 layers, 7.18 g, 31 min 22 s; G28 then M420 S1, 60/210,
heaters and fan off at the end, moves inside the bed. Orca's 3MF export failed (exit 243); the G-code is complete.
SD card not mounted, so not copied.

### 2026-11-26 Ring v4 from the bare-bottle close-ups
Jacob said the v3 bottle model was not good enough and sent two close-ups of the bare bottle (`images/amber-neck-bare-2331.jpg`,
`-2332.jpg`). Traced the silhouettes from the background-removed PNGs. The measured 43.5 neck and 65 body only fit
the photos with a pinhole camera about 65 mm from the axis (a phone close-up), and both photos give the same distance,
so the perspective is corrected with it; depth is anchored on the glass rim, collar underside 14.6 below. The two photos
agree within 0.4 mm in depth. No 46.5 band exists: v3 would have jammed on the shoulder. New `EST_AMBER_NECK_PROFILE`,
ring 4.5 tall and 54.5 across, wall 2.5 at the underside. Projected the model back onto both photos
(`images/amber-neck-model-overlay-*.jpg`): the profile sits on the glass edge from the neck to the full body. check.sh
passes, zero overlap, also with the profile 1 mm higher and 1.5 lower. Hoop SF 3.4. Sliced `scratch/amber4_ring-20261126`,
29 min, 6.3 g, 100% infill.

### 2026-11-26 Ring v4 printed; v5
Key: perfect fit at 0.15 per side play. With the pump on the bottle lifted 2.0 mm before catching the ring (model 1.25)
and was loose. Calibrated the neck profile 0.75 lower, cut the upward margin to 0.3 and made the ring 6.5 tall (2 more
down the shoulder), wall 5.5. Modelled lift 0.5 (0.2 with the profile 0.3 higher, 1.5 with it 1 lower), zero overlap,
wall 1.95 at the underside, hoop SF 7.6 with the tapered section summed (`amber_strength.py`). Sliced
`scratch/amber5_ring-20261126`, 37 min, 9.0 g.

### 2026-11-26 Shim for ring v4
Jacob would rather add to the printed v4 than reprint the ring. `cad/amber_shim.py`: v5's bottom 2 mm as a loose ring
(55.5 across, bore 45.4 at the top to 51.6 at the bottom, same cutter as v5), slid on before v4; the shoulder pushes it
against v4's flat underside, so v4 + shim behaves as v5 (modelled lift 0.5). Sliced `scratch/amber_shim-20261126`,
6 min, 1.5 g. To print tomorrow.

### 2026-11-27 Shim printed: works, but loose
Copied to the SD card as `amber_shim.gcode`; Jacob printed and fitted it under v4. It works okay, not amazingly. The
diameter is a touch large: the 44.5 bore has to pass the 44.0 glass thread, so it has 0.5 radial play on the 43.5 neck.
A taller shim would only push the ring (and key) up. Next: a split ring that snaps over the thread and closes on the neck.

### 2026-11-27 Split-ring gauge
`cad/amber_split_gauge.py`: four 3 mm rings with the ring's 5.5 wall and a 2 mm slot, bores 43.2-43.8, tied on one
plate. Spreading the 43.2 one over the 44.0 thread strains it about 0.2 % (PLA yields at 2-3 %). No grip fit for a
split PLA ring on glass in `workshop.fits`, hence the gauge.
