# __NAME__

Owner: __OWNER__. Started __DATE__.

![The assembled thing](exports/preview.png)

<What it is, who it is for, and what "done" looks like, in a paragraph.>

## Parts

One row per printed or cut part, with its picture, so anyone can tell which file is which.
`workshop.cad.export` writes `exports/<part>.png` beside every STL; commit it.

| Picture | Part | File | How many | Notes |
|---|---|---|---|---|
| <img src="exports/example_part.png" width="200"> | Example block | `exports/example_part.stl` | 1 | bore for the shaft, captive M3 nut |

## Build

```sh
uv run python cad/example_part.py     # writes exports/example_part.{stl,step,png}
./check.sh                            # every check; run before committing
```

## Printing

<Profile from the workshop repo's equipment/neptune-3-pro/profiles/, orientation, what to ream.>
