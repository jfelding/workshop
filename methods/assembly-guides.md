# Assembly guides (IKEA-style)

The guides are HTML pages generated from Python, one per stage of a build. They have numbered steps with a short instruction each, a drawing for each step, and a
"You need" sheet of parts at the top. People build from them on a phone or a laptop at the bench.
`workshop.guides` holds the style and the page kit, and `workshop.cad.render` draws CAD solids in the
same style. The largest build made this way so far has 13 chapters, from mechanical work through soldering to a
first power-on.

## What makes them readable

These rules came from the user's feedback during that build:

- **One action per step.** The instruction is a single short sentence in plain words: "Push the pin through
  until it stops." Put any explanation in a `warn()` box, not in the step.
- **Every step has a drawing.** A step that is hard to picture in words gets a CAD drawing, not more
  words. One guide switched four steps from words to CAD drawings, and the user found them clearer.
- **Colour means the same thing everywhere** (`KEY`): **yellow** is what you handle in this step,
  **grey** is already fitted, **white** is context. The CAD renderer uses the same three groups:
  `'hi'`, `'done'` and `'other'`.
- **Flat fills, black outlines, no shading.** Hidden edges are dashed only where they matter.
- **"You need" cards** show each part with a count and the size that tells it apart: "M3 × 8,
  self-tapping" or "M5, 14.5 mm across".
- **Page width 780 px.** A wider page was tried and rejected. Drawings scale down on a phone (`FIT` script).
- **Keep the guide about the current design.** When the design changes, change or delete the step; never add "outdated" notes.
- **Status per chapter** on the index page ("Done", "Next", "Proposed"), so a builder knows what is real.

## Making a chapter

```python
# guide/ch01_base.py
from workshop.guides.style import *          # page, step, warn, Parts, svg, txt, arrow, nut, washer, …
from workshop.cad.render import View, render, callout

P = Parts()
P.card(4, f'<g transform="translate(70,40)">{nut(0,0,22)}</g>' + txt(70, 82, "M3", cls="lbl s"), "nut")

def drawing():
    v = View((1, -1, 0.8))          # direction toward the viewer; z up
    body, (w, h) = render([(plate, 'hi'), (frame, 'done')], v,
                          notes=[callout((0, 0, 10), 40, -30, "this edge up")])
    return svg(f"0 0 {w:.0f} {h:.0f}", body, "Plate on the frame, edge up")

def build(nav=""):
    body = P.sheet() + step(1, "Lay the plate on the frame, this edge up.", drawing())
    body += step(2, "Drop a nut into each pocket.", "", extra=warn("Flat side down."))
    return page("Base", "Plate and frame. 15 minutes.", body, nav)
```

```python
# guide/build.py
from workshop.guides.book import Chapter, write_book
import ch01_base, ch02_frame
write_book("guide/html", "Fixture assembly", [
    Chapter("01-base", ch01_base, "Base", "Done"),
    Chapter("02-frame", ch02_frame, "Frame", "Next"),
], made_by="workshop")
```

For a drawing kept as a separate file, set `workshop.guides.style.VIEWS` to its directory and use
`view(name)`. Hand-drawn SVG is fine for parts and gestures, and quicker than CAD for a hand
holding a screwdriver. Use CAD renders wherever a position or orientation has to be exact.

Electronics chapters add `workshop.guides.electronics`:

- `wire()`, `pin()` and `Driver` (a stepper-driver pinout);
- `cap()`, `resistor()` and `meter()` (a multimeter in beep, volts or ohms mode);
- `iron()` (a soldering iron);
- `board_strip()`;
- `yes()` / `no()` for photos of a good joint next to a bad one.

## The second approach: build123d SVG scenes

A one-page guide can use build123d's own `ExportSVG` scenes and a static `template.html`. That is simpler, gives line drawings with no fills, and needs no OCP calls. It suits a
one-page guide. For a multi-chapter build with a parts sheet and the colour key, use `workshop.guides`.

## Publishing

The HTML is self-contained except for one Google Font. Commit the generated HTML next to its source, so
that someone can open it from the repo without running Python. Regenerate the HTML in the same commit as
any CAD change that shows in it.
