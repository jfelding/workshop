# PETG PRO fast, 0.4 mm nozzle, adaptive purge

A copy of [`petg-pro-fast-0.4`](../petg-pro-fast-0.4/). The process and filament are the same; only the
machine start G-code differs (2026-11-27, at the user's request). Instead of the fixed 100 mm purge line
along the front edge (Y 0.5, 30 mm of filament), the purge line goes next to the part:

- 10 mm in front of the first layer's bounding box (Orca's `first_layer_print_min/max`), centred on it in X;
- as long as the first layer is wide, clamped to 50–100 mm, with 0.3 mm of filament per mm of line (the
  stock ratio), so 15–30 mm of filament;
- kept 5 mm inside the bed's X edges. If the part starts less than 15 mm from the front edge, the line
  falls back to the stock Y 0.5.

Why: hot PETG oozes during the long travel from the front edge to the part and leaves a string or blob on
the first layer; the purge also stops wearing the same front strip of the textured PEI.

Uses Orca's `{local …}` placeholders (Orca 2.4.2). Checked on a coupon plate: the purge was drawn at
Y 85.7, X 90–140, in front of a first layer at Y 98.1–132.0, X 92.6–137.5, and the print moves were identical
to the stock-purge slice. No print outcome recorded yet.
