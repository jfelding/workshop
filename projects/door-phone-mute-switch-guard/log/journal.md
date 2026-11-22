# Journal

## 2026-11-19 Project started

From the workshop repo's templates/project. Photo of the switch in `images/door-phone-mute-switch.jpg`: a
miniature panel toggle with a hex nut, on the flat side face of the handset, close to its rear edge.
Wrote `cad/guard.py`. Dry run on made-up numbers in a scratch directory only, to see the script work end to
end; no measurement has been taken and nothing was exported into the project.

## 2026-11-19 First measurements, fewer asked for

Jacob: thread about 5.7, nut 2.1 thick and 9 across flats, 1.5-1.7 of thread showing past the nut. He asked
for only the strictly needed measurements. Redesigned so the cup holds the nut in a hex well and is its own
wrench: no tool diameter, no collar height (the spare thread covers the 1.2 floor, 0.3 left), no edge distance.
Left: lever tip height and lever swing span. The first dry run's keep-out check failed with the lever modelled
as a full-width cylinder; it pivots in the collar, so it is now a cone.

## 2026-11-19 Lever measured, first build

Jacob: tip 15 mm from the face with the lever centred; at both ends of the throw the tip stays inside the
nut's outline. Swing span entered as an upper bound of 10.4 (the nut across corners). Built: Ø15.2 × 18 mm,
bore Ø12.0, lever 0.8 mm per side from the bore and 3.0 below the rim, 0 mm² overhang, watertight.

## 2026-11-22
Sliced the guard for the Neptune 3 Pro with `pla-fast-0.4` (stock speeds), job dir `scratch/guard-20261122`.
Orientation as modelled: floor on the bed, open end up, no supports. 90 layers to Z 18, 1.74 g, Orca estimate
15 m 22 s. Part centred at X/Y 115. Copied to the SD card as `doorguard.gcode`. Not printed yet. The installed
OrcaSlicer is 2.2.0 and has no `--logfile` flag, so the README's slice command needs that flag dropped.
