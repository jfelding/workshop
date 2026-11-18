# PLA fast, 0.4 mm nozzle (default)

The small-gears profile with Orca's stock Neptune 3 Pro speeds (user, 2026-11-11: the older speeds
were much too slow). Settings:

- speeds: 25 mm/s first layer, 60 outer walls, 100 inner walls and infill, 150 travel;
- acceleration: 1000 mm/s², 700 on outer walls;
- shell: 0.2 mm layers, 4 walls, 20 % gyroid;
- temperatures and plate: 210 / 60 °C on textured PEI.

On a 32 × 36 × 26 mm block it halved the estimate (2 h 19 m → 1 h 09 m).

Do not slow it down unless a print at these speeds has failed on that part. Do not push past it:
the acceleration is at the machine profile's limit and there is no input shaping.
