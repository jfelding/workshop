# Power strip and remote holder for a bed's mattress stop

Owner: Jacob. Started 2026-10-31.

![The holder on the mattress stop, from the room and from behind](exports/preview.png)

Our adjustable bed has a mattress stop at the foot end: a cloth-covered steel bar on two legs that keeps the
mattress from sliding off when the bed tilts. I wanted a power strip and the bed's wired remote right there,
instead of on the floor. This holds an **Elworks 6-way power strip** (6-stikdåse u/jord, 39-306-1) on its
side, sockets facing the room and cord to the left, plus a cup for the **DewertOkin (OKIN) CLASSIC 27760**
handset on the right. It hangs on the stop's top bar by a lip and is pulled flat against it by magnets
through the cloth. Nothing on the bed or the strip is modified.

Status: printed and being fitted. Two fixes came out of the first print (below) and are not confirmed yet.

## How it works

- **Two flat pieces**, saddle and tail, because the whole thing is longer than the Neptune 3 Pro's
  225 mm bed. A drop-in bowtie key joins them; a second key hangs the cup off the saddle's other end.
- **The strip hangs on its own wall-mount holes.** The Elworks strip has two plus-shaped hanging holes in
  its base. A small bayonet adapter goes in each: push it through at 45°, turn it 45° and its head locks
  behind the plastic ([picture](exports/adapter.png)). The adapters' T-feet then drop into two vertical
  T-slots on the holder. The closed slot bottoms carry the weight, and in the slot the adapter can't turn,
  so it can't unlock. Lift the strip straight up to take it off.
- **Nothing covers the strip.** Its sides, sockets and cord are free; the slot faces and two pads take the
  push when a plug goes in.
- **Magnets, not clamps.** A printed insert slides up inside the stop's cloth cover, below the bar. Its
  magnets pair with three in the saddle, through the cloth. The lip on the bar carries the weight; the
  magnets only stop it tipping.

![Sections through an adapter and a socket](exports/side_profile.png)
![From the room](exports/side_front.png)

## Parts

STL and STEP files are in [`exports/`](exports/). Sizes are as printed (bounding box in print orientation).

| Picture | Part | File | How many | Notes |
|---|---|---|---|---|
| <img src="exports/side_saddle.png" width="240"> | Saddle | `side_saddle.stl` / `.step` | 1 | 148.0 × 26.6 × 55.2 mm, 45 cm³. Back plate, lip over the bar, 3 magnet bosses, near T-slot, key pockets to cup and tail |
| <img src="exports/side_tail.png" width="240"> | Tail | `side_tail.stl` / `.step` | 1 | 141.3 × 22.0 × 55.2 mm, 40 cm³. Reaches past the stop's end; flange and 45° gusset keep it stiff |
| <img src="exports/key.png" width="240"> | Bowtie key | `key.stl` / `.step` | 2 | 15.6 × 7.4 × 51.4 mm. Cup to saddle, saddle to tail |
| <img src="exports/cup.png" width="240"> | Remote cup, original case | `cup.stl` / `.step` | 1 | 58.6 × 44.9 × 72.0 mm, 47 cm³. Slit in the back wall so the cable drops in sideways |
| <img src="exports/mag_insert.png" width="240"> | Magnet insert | `mag_insert.stl` / `.step` | 1 | 105.0 × 35.5 × 6.2 mm. Slides up inside the cloth cover; 4 magnet pockets |
| <img src="exports/adapter_elworks.png" width="240"> | Strip adapter | `adapter_elworks.stl` / `.step` | 2 | 20.0 × 10.5 × 9.7 mm. Bayonet head 2.4 mm across the arms |
| <img src="exports/adapter_elworks_test_arm2.2.png" width="240"> | Strip adapter, narrow test head | `adapter_elworks_test_arm2.2.stl` | 0–1 | If the 2.4 head won't pass the plus |
| <img src="exports/adapter_elworks_test_arm2.6.png" width="240"> | Strip adapter, wide test head | `adapter_elworks_test_arm2.6.stl` | 0–1 | If the 2.4 head rattles |
| <img src="exports/adapter_offset_2.5.png" width="240"> | Offset adapter, 2.5 mm | `adapter_offset_2.5.stl` / `.step` | 2 | Fix for the printed holder's slot spacing (below) |
| <img src="exports/adapter_offset_2.0.png" width="240"> | Offset adapter, 2.0 mm | `adapter_offset_2.0.stl` | 0–2 | Test pair |
| <img src="exports/adapter_offset_3.0.png" width="240"> | Offset adapter, 3.0 mm | `adapter_offset_3.0.stl` | 0–2 | Test pair |
| <img src="exports/adapter_offset_0.0.png" width="240"> | Offset adapter, 0 mm | `adapter_offset_0.0.stl` | 0 | Reference: the offset design with no offset |

Also needed: 7 neodymium disc magnets, 10 × 5 mm (4 in the insert, 3 in the saddle). The insert's pocket at
x = −14 has no partner in the saddle (the near T-slot sits there), so leave it empty. Check each pair attracts
before gluing.

### Optional: slimmer remote case

The CLASSIC handset is 139.5 mm long, mostly empty plastic. This two-part case reuses its circuit board, both
button strips, the cable with its strain-relief boot and the three case screws, and is 86 × 50 × 23.8 mm.
It docks in its own shorter cup, with all six buttons usable while docked.

| | |
|---|---|
| <img src="images/remote-pcb-in-case.jpg" width="320"> | <img src="images/remote-pcb-and-button-strips.jpg" width="320"> |
| The original case opened: the board sits at the button end, the rest is cable run | Board and the two loose button strips |

![The slim shell, with the original parts inside](exports/remote_shell.png)

| Picture | Part | File | How many | Notes |
|---|---|---|---|---|
| <img src="exports/remote_front.png" width="240"> | Slim case, front (keypad) half | `remote_front.stl` / `.step` | 1 | 86.0 × 50.0 × 18.8 mm. Print first and dry-fit |
| <img src="exports/remote_back.png" width="240"> | Slim case, back half | `remote_back.stl` / `.step` | 1 | 86.0 × 50.0 × 9.2 mm. **Re-export after the dry fit** (see Assembly) |
| <img src="exports/cup_slim.png" width="240"> | Remote cup, slim case | `cup_slim.stl` / `.step` | 1 | 58.6 × 46.3 × 57.0 mm. Replaces `cup.stl` |

![The slim case docked in its cup](exports/remote_slim_fit.png)

Button marks are engraved one layer deep between the rows: a circle for head, a line for legs, both for the
middle button. Fill them with epoxy or nail polish and wipe flush.

## Printing

Elegoo Neptune 3 Pro, 0.4 mm nozzle, OrcaSlicer, Elegoo PLA at 210/60 °C on the textured PEI sheet:
4 walls, 25 % gyroid, a 5 mm brim on plates with tall parts. No supports anywhere.

- Saddle and tail **upside down**, top edge on the bed (about 8 h 15 min for the pair).
- Cup standing (about 4 h). Insert flat, room face down. Keys lying on one wide end.
- Adapters foot down.
- Slim case halves outer face down. PETG on a smooth sheet is nicer here: it takes alcohol wipes.

PLA is fine for the holder: nothing in it is a spring. PETG is tougher if it gets knocked.

The T-slots print vertically, and small vertical holes come out about 0.2 mm under size on this printer,
so the adapter feet (0.4–0.5 mm total clearance) may be snug.

## Assembly

1. **Print one adapter first** (10 minutes). Push it through a plus hole at 45° and turn it 45°. If it won't
   go in, use the 2.2 mm head; if it rattles, the 2.6 mm one. Then pull hard: the strip's plastic behind the
   head is the weakest link.
2. Press the magnets into the insert and the saddle (pockets face the room on both).
3. Slide the insert up inside the stop's cloth cover, between the legs, magnets towards the room.
4. Push a key into the saddle–tail pocket and lower the tail onto it. Push the other key up into the cup until
   it stops, then lower the cup beside the saddle so the key drops into the saddle's pocket.
5. Hang the saddle's lip over the bar so the magnets find each other.
6. Lock the two adapters into the strip with their feet across the strip, then lower it in from above so the
   feet drop into the slots.
7. Drop the remote in cable end down; the cable goes in through the slit, so the plug never has to pass.

For the slim case: lay the front half face down, put in both button strips, lower the board onto them over the
centre tube and measure how far its underside stands above the rim (about 1.3 mm expected). Put that number in
`DRYFIT_D` in `cad/remote_shell.py`, run it, and print the back half it writes.

## Changes after the first print

- **Slot spacing.** In the printed holder the two T-slots sit about 5 mm closer together than the strip's
  plus holes (estimated from a photo). Rather than reprint the holder, the offset adapters carry the foot
  sideways on a 2 mm plate: use a matched pair, feet pointing towards each other, each offset by half the
  error. The strip then stands 2 mm further out and rests on the two plates. Print the 2.0/2.5/3.0 pairs
  (about 55 minutes) and keep the pair that drops in.
- **Cup joint.** The first cup's key pocket was closed at the bottom, so pushing the remote down slid the cup
  off its key. The cup's pocket is now open at the bottom with a roof at the key's top, so the cup hangs from
  the key.

## Checks

`holder_side.py` builds the whole assembly and reports (2026-11-23 run):

- **Overlaps, all 0.00 mm³:** saddle and tail against the stop with a 13 mm sleeve, saddle/cup, saddle/tail,
  insert/saddle, keys, strip/holder, adapters/holder, adapters/strip, and the strip lowered in from 1 to 39 mm
  above.
- **Holds:** pulling 0.5 mm to the room (88 mm³ of contact), pushing to the stop (694), sliding 1 mm either way
  (131), dropping 0.5 mm (31) and tipping 2° face down (291) are all blocked.
- **Adapters:** the head passes the plus and turns 0–45° with no overlap; pulled 0.3 mm it bears on the wall,
  9.8–10.9 mm² behind the wall depending on head width. Offset adapters: 0.00 mm³ against the strip.
- **Slim case:** no overlap between the halves or with the board, switches, button strips or boot. In its cup:
  no overlap with the cup or the stop, 48 mm stands above the rim, the boot hangs 26 mm below.
- **Original remote in `cup.stl`** (`fit_remote.py`, needs the manufacturer STEP): 70.7 mm above the rim, the
  boot hangs about 25 mm below the cup, 0.59 mm³ of overlap with the cup. Make sure there is room under it.

## Source

Python with [build123d](https://build123d.readthedocs.io/). `./check.sh` rebuilds every part into `exports/`
and runs the checks.

| Script | What |
|---|---|
| `cad/strip.py` | Measured model of the Elworks strip |
| `cad/rail.py` | T-slot profile and the T-foot that sits in it |
| `cad/adapter.py` | Bayonet and offset adapters, with their fit checks against the plus hole |
| `cad/holder.py` | The stop's dimensions, joint blocks, keys, cups |
| `cad/holder_mag.py` | Magnet insert, bosses and pockets, top lip |
| `cad/holder_side.py` | Saddle and tail; the fit, lowering and hold checks; `side_assembly.step` |
| `cad/remote_shell.py`, `cad/cup_slim.py` | Slim remote case and its cup |
| `cad/fit_remote.py` | Original remote in `cup.stl`, from the manufacturer STEP |
| `cad/render_side.py`, `cad/preview.py` | The pictures above |

`exports/side_assembly.step` and `exports/side_strip_placed.step` open together as the assembled holder with
the strip in place.

### Measurements

- **Elworks 39-306-1 strip** (calipers, 2026-11-02): body 284 long without the strain relief, 44.5 wide, 35.85
  from base to socket face. Six sockets Ø38, 14 deep, pitch 44.27; first socket edge 19.7 from the cord end,
  last 4.95 from the far end. Plan corners R 12.5. Plus holes on the centreline, centres 60.65 from the cord
  end and 46.75 from the far end; 9.5 across, arm ends about Ø3, round middle about Ø6.4, through a 2 mm wall
  into a pocket about 10 wide and 3.65 deep.
- **DewertOkin CLASSIC 27760**, from DewertOkin's STEP: body 50.0 × 23.5 × 139.5, stadium section, a
  strain-relief boot about 10 across running 29 beyond the cable end. Buttons 15.0 apart across, rows 23.5
  apart. Board (calipers, 2026-11-02): 1.70 thick, switches stand 9.9 above it, centre hole Ø9; button strips
  41.9 across.
- **Mattress stop:** 8 mm steel rod, top bar just over 126 long, the upright 58 visible. The cloth sleeve is
  modelled as 12 mm and checked at 11 and 13.

Still estimated, not measured: see [`inventory/to-measure.md`](inventory/to-measure.md).

This project predates the workshop's `measurements.py` convention: its dimensions are constants at the top of
`strip.py`, `holder.py`, `holder_mag.py`, `adapter.py` and `remote_shell.py`.

## Credits and licence

Our own design, CC BY 4.0. DewertOkin's STEP of the CLASSIC handset was used only to measure the remote; it is
not redistributed (see [`vendor/dewertokin-classic/`](vendor/dewertokin-classic/README.md) for where to get it).
