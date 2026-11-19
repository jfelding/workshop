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
