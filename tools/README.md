# Presentation tools

Reference implementation of the authoring subset in
[`../skill/justesse/references/pptx-safe-html.md`](../skill/justesse/references/pptx-safe-html.md).
They are a reference implementation, not part of the skill's contract: any converter that preserves
the subset and produces the same inspectable inventory satisfies it.

Both use only the Python standard library. There is nothing to install.

| Tool | Job |
| --- | --- |
| `html2deck.py` | Presentation-safe HTML to a PPTX whose every element is a native, editable object |
| `inspect_pptx.py` | A PPTX to an NDJSON object inventory: geometry, color, type, text, background, and any rasterized region |
| `inspect_html.mjs` | A rendered HTML surface to the same inventory shape, one slide per viewport |
| `diff_specimens.py` | Two inventories to a graded delta report and a design verdict that content cannot sway |
| `declaration2tokens.py` | A validated profile declaration to namespaced `--j-*` design tokens (CSS or JSON) |
| `check_layout.mjs` | A presentation-safe deck to a list of measured layout failures: text past its box, text on text, objects off the canvas |

```bash
python3 tools/html2deck.py deck.html deck.pptx
python3 tools/inspect_pptx.py deck.pptx > deck.inspect.ndjson
node tools/inspect_html.mjs page.html --viewports 1440x1000,390x844 > page.inspect.ndjson
node tools/check_layout.mjs deck.html --max-void 80
python3 tools/diff_specimens.py a.pptx b.pptx
```

The two `.mjs` tools are the ones with a runner-provided dependency: they need the `playwright`
package resolvable from the invoking directory plus an installed Chrome or Chromium (they prefer the
system Chrome channel, so no browser download is required). Install it with the download skipped,
which is what this repository pins:

```bash
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install
```

`inspect_html.mjs` renders the page at each requested
viewport and emits one "slide" per viewport, because a responsive surface at two widths is two
compositions of one design. With that, `diff_specimens.py` covers every surface in the harness
contract, not only decks, and the anti-convergence hard gate is executable across all of them. The
Python test suite stays hermetic: it does not exercise these tools, and the harness treats browser
capture as runner-provided evidence, same as renders and screenshots.

## Checking what the font decides

`check_layout.mjs` measures the one thing the subset cannot fix at authoring time. Every box is
declared in px, but a text box's declared height is a prediction: type is measured by the font, so a
title expected on one line wraps to two, overflows, and lands on the paragraph beneath it. The
overflow is in the presentation file as well as the browser, because a text box overflows rather
than shrinks, and it is invisible in the source.

Three failures, all measured: `overflow` (text taller than its declared box), `collision` (two text
objects overlapping once wrapped), and `escape` (an object outside the 1280x720 canvas). Shapes may
overlap anything and text may sit on a shape — a label inside a bar, a bar crossing its axis — so
only text against text counts. `--max-void N` additionally reports the largest empty band per slide
above a threshold; it is opt-in because how much space a surface should carry is a judgment an
identity declares, not a constant a tool knows.

This exists because the failure it catches survived a full verification round: the collision was
visible in a rendered slide, a reviewer looked at that slide, and the reviewer missed it. Attention
does not scale across five slides and three revisions; measurement does.

## Comparing specimens

`diff_specimens.py` pairs the objects of two inventories and grades every difference: color
perceptually (OKLab, with the delta printed even when it sits far below what a viewer could call
out), geometry to the pixel, type by size and family. Text differences are reported separately and
never sway the design verdict, because two specimens carrying different words on one layout are the
same design.

Both failure directions are exit codes. `--expect-same` fails on visible design deltas (a
regression check). `--expect-distinct` fails when two supposedly distinct identities produced one
design (the convergence check behind the harness's anti-convergence hard gate).

## What the converter guarantees

Text arrives as live text in a text box. Rules, panels, bars, ticks, and swatches arrive as shapes.
Charts are composed of individually named shapes and their labels, which is more editable than a
single chart object and far more editable than a picture. Nothing is rasterized, because nothing in
the subset needs to be.

Geometry round-trips exactly: 1 px on the 1280x720 canvas is 9525 EMU, so the canvas maps to the
13.333 x 7.5 in 16:9 frame with no rounding drift.

## What it refuses

A construct outside the subset raises `UnsupportedConstruct` naming the slide, the object, and the
offending declaration. It does not approximate, and it does not fall back to a picture. The whole
value of the contract is that this failure lands while the deck is being authored, not after the
recipient opens it and finds they cannot move a label.

Refused: runtime layout (flexbox, grid, floats, percentages, `auto`, `calc()`, margins, padding),
conditional rendering (media queries, state selectors), effects with no shape equivalent (gradients,
shadows, filters, transforms, container opacity, blend modes, clip paths), generated and external
content (`::before`, `::after`, background images, SVG, canvas, iframes), and raster images.

Substituting a picture for a region that failed to convert is a scope change, not a rendering
detail. Disclose it.

## Declaring is building

`declaration2tokens.py` closes the gap between passing the declaration gate and building: it emits
the declared values as namespaced `--j-*` custom properties (or flat JSON), so no one transcribes a
declaration by hand — and hand transcription is where the drift lives that `diff_specimens.py`
would otherwise catch later. The gate composes: an incomplete declaration is refused field by
field, and nothing is emitted. Surfaces consume tokens by reference (`--surface: var(--j-surface)`)
and keep their derived values — panel tints, hairline colors — outside the declaration's
authority. Verified in calibration round 2b: three surfaces rebuilt on emitted tokens re-inventory
as SAME DESIGN, delta-free (see `../harness/calibration-log.md`).

## Verifying, in the right direction

`inspect_pptx.py` parses the written file, not the HTML that produced it. It reports one record per
slide and per object, with the object's name, its px geometry, its color, and, for text, the exact
string the file holds. A `picture` record carries `"rasterized": true`, and the process exits
non-zero when any exists.

That direction is the point. A converter can claim it emitted native objects; only the file can show
it. `tests/test_deck_tools.py` asserts the round trip on both paths: the inventory a real deck
produces, and the rejection of each unconvertible construct.
