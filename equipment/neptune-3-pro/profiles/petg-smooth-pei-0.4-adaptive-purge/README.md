# PETG PRO, smooth PEI, 0.4 mm nozzle, adaptive purge

A copy of [`petg-pro-fast-0.4-adaptive-purge`](../petg-pro-fast-0.4-adaptive-purge/) for the **smooth PEI
plate with glue stick**. It was set up with the user on 2026-11-27, after large PETG first layers (a monitor-mount
spacer, 84 × 73 mm) kept lifting off the plate and riding up on the nozzle. Speeds, walls, retraction length and the
adaptive purge are unchanged.

| Setting | Source profile | This profile | Why |
|---|---|---|---|
| `curr_bed_type` | Textured PEI Plate | High Temp Plate (Orca's smooth PEI) | the plate actually used |
| Bed, layer 1 / after | 70 / 70 °C | 85 / 80 °C | better first-layer grip on smooth PEI (user's trial) |
| Nozzle, layer 1 / after | 230 / 230 °C | 240 / 235 °C | hotter first layer bonds better (user's trial) |
| `first_layer_flow_ratio` (with `set_other_flow_ratios` 1) | 1 | 0.95 | less surplus on the 0.5 mm-wide first layer for the nozzle to plough into random blobs |
| `reduce_infill_retraction` | 1 | 0 | every travel over 1 mm retracts and lifts 0.4 mm. With 1, ~1,500 travels per spacer crossed the infill at layer height, oozing; PETG built up on the nozzle and dropped as blobs (2026-11-27). Costs ~11 min on a spacer |

All the textured-plate temperatures are set to the same values, so a slice with the other bed type still gets
them. Checked in Orca 2.4.2: G-code has `M190 S85`, `M109 S240`, then `M104 S235` and `M140 S80` at layer 2.
Layer 1 extrudes 95.0 % of the source profile's amount, and layer 2 onward is the same amount (0.95 of nominal:
process 0.97 × filament 0.98). With `reduce_infill_retraction` 0 the spacer has 3,560 retractions instead of
1,531, and 1 travel over 2 mm without a lift instead of 1,479 (4 h 01 min instead of 3 h 49 min).

Prepare the plate: wash it with warm water and dish soap. Rub glue stick lightly over the part's area, then
spread it with a damp, wrung-out paper towel until only a faint haze is left. White streaks are too much and
float the PETG. Re-level with the bed hot.

No print outcome recorded yet. The whole routine (hot levelling, glue, nozzle wipe) is in `materials/petg.md`.
