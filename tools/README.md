# Presentation tools

Reference implementation of the authoring subset in
[`../skill/justesse/references/pptx-safe-html.md`](../skill/justesse/references/pptx-safe-html.md).
They are a reference implementation, not part of the skill's contract: any converter that preserves
the subset and produces the same inspectable inventory satisfies it.

Both use only the Python standard library. There is nothing to install.

| Tool | Job |
| --- | --- |
| `html2deck.py` | Presentation-safe HTML to a PPTX whose every element is a native, editable object |
| `inspect_pptx.py` | A PPTX to an NDJSON object inventory, including any rasterized region |

```bash
python3 tools/html2deck.py deck.html deck.pptx
python3 tools/inspect_pptx.py deck.pptx > deck.inspect.ndjson
```

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

## Verifying, in the right direction

`inspect_pptx.py` parses the written file, not the HTML that produced it. It reports one record per
slide and per object, with the object's name, its px geometry, its color, and, for text, the exact
string the file holds. A `picture` record carries `"rasterized": true`, and the process exits
non-zero when any exists.

That direction is the point. A converter can claim it emitted native objects; only the file can show
it. `tests/test_deck_tools.py` asserts the round trip on both paths: the inventory a real deck
produces, and the rejection of each unconvertible construct.
