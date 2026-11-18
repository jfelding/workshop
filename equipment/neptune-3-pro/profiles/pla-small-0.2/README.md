# PLA small, 0.2 mm nozzle

The saved profile for the 0.2 mm nozzle (0.10 mm layers, solid infill): small exact parts. Provenance of the original job (six M3 spacers):

> `cad/m3_spacer.py`: plain ring, 4.50 mm tall, 3.40 mm screw clearance, chosen 7.00 mm
> outside diameter (standard M3 washer footprint). Dimensions in `measurements.py`.
> Each part is one valid solid, with 1.80 mm radial wall and zero screw keep-out overlap.
> User requested six and explicitly prefers 4.6 to 4.4 if layer rounding is necessary.
> This slice hits 4.50 mm exactly: 45 × 0.10 mm layers, no rounding.
>
> Six separately named copies in one plate, flat, no supports/brim. 0.2 mm nozzle,
> three walls, solid infill, three skin layers, 0.10 mm elephant-foot compensation.
> PLA 210/60 °C; retained faster speeds: outer 50 / inner 62.5 / infill 75 /
> travel 125 mm/s, 500 mm/s², 2 mm³/s flow cap. First-layer base 37.5 mm/s;
> 50% first three layers, then automatic 100%. Nozzle/filament unchanged from preceding job.
>
> Orca 2.4.2 estimate 30m 0s, 0.95 g; allow about 35 min with cold heating.
> Preflight confirms six printable objects in the 3MF, 45 layers, last layer Z 4.50 mm,
> bounded moves, saved mesh after home, heaters/fan off ending. Toolpaths inspected.
>
> Started 2026-10-09 12:45:44 local, host PID 70461, `/dev/cu.usbserial-113240`.
> Job `scratch/neptune-m3-spacers-45-20261009`. User authorized print and clean plate.
> Use job `control.py`; keep Mac lid open and USB connected.
> Host completed 2026-10-09 13:15:53, actual 30 m 09 s; heaters off.
> Physical height/fit remain unreported.
