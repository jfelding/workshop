# Equipment

One directory per machine, holding its rules, facts, saved settings and the software that drives it.
A new machine starts as a copy of [`_template/`](_template/).

| Machine | Kind | Driven by |
|---|---|---|
| [Elegoo Neptune 3 Pro](neptune-3-pro/) | FDM printer (fused-filament, the usual hobby 3D printer) | OrcaSlicer CLI plus `usb-host/` over USB, or the SD card |

## Who may do what

| Action | Agent alone | Needs a person's word |
|---|---|---|
| Slice, check G-code, write profiles | yes | |
| Open the printer's serial port | only if no host is running | |
| Start a print | | yes, after the bed is checked |
