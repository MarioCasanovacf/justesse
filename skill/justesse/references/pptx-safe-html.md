# Presentation-safe HTML

Read this when the deliverable is an editable presentation file and HTML is the authoring medium.
It defines the subset of HTML that converts to native, individually editable objects, and the
constructs that silently degrade into a flat picture.

The failure this prevents is specific. Interface HTML is written to reflow: it resolves its layout
at runtime, against a viewport, using rules a slide canvas does not have. A presentation file has no
runtime. Its layout is a set of absolutely positioned objects on a fixed canvas, resolved once at
authoring time. HTML written for the first target cannot be exported into the second; it can only be
photographed into it. Author for the slide canvas from the start.

## The canvas

One slide is a fixed 1280 × 720 px canvas, which maps exactly to the 16:9 presentation frame of
13.333 × 7.5 in at 96 px per inch. Every coordinate is an integer px offset from the slide's top
left corner. There is no responsive behavior, no breakpoint, and no overflow: an element positioned
outside the canvas is off the slide.

## The authoring subset

Each slide is one element carrying `class="slide"`, with an optional `background` hex value that
becomes the slide's canvas fill. Declare it: a slide with no background inherits whatever surface
the opening application defaults to, which is rarely the one the design assumed.

Each visual object inside the slide declares its kind through a class and its box through four
absolute inline values: `left`, `top`, `width`, `height`, all in px. Give every object a
`data-name`, which becomes its object name in the presentation file and makes the result
inspectable. Objects may sit inside plain wrapper elements; only the four classed kinds convert.

| Class | Becomes | Style properties carried |
| --- | --- | --- |
| `text` | Text box with live, editable, reflowable text | `font-size` px, `font-family`, `color` hex, `font-weight`, `font-style`, `text-align`, `line-height` |
| `rect` | Rectangle shape | `background` or `background-color` hex, `border` as `Npx solid #hex` |
| `ellipse` | Ellipse shape | `background` or `background-color` hex, `border` as `Npx solid #hex` |
| `line` | Straight line | `background` hex as the stroke color, `height` px as the stroke weight |

Everything a deck needs is expressible in these four. Rules, panels, bars, ticks, swatches, and
callout boxes are rectangles. Chart marks are rectangles and lines with their own `data-name`, and
every label is a text box anchored to the mark it describes. A chart built this way arrives as a set
of objects the recipient can recolor, renumber, and realign one at a time, which is more editable
than a single chart object and far more editable than a picture.

## Previewing the canvas

This subset is written for a canvas the browser does not assume. The geometry lives in the inline
styles the converter reads, but a browser also has to be told that those boxes are absolute and that
a slide is a fixed frame. Told nothing, it stacks every object in document flow, and the author
reviews a column of fragments instead of a slide. Put one stylesheet in the document head, carrying
the mechanics and nothing else:

```css
* { box-sizing: border-box; }
body { margin: 0; padding: 0; }
.slide { position: relative; width: 1280px; height: 720px; overflow: hidden; margin: 0 auto; }
.text, .rect, .ellipse, .line { position: absolute; margin: 0; padding: 0; }
.ellipse { border-radius: 50%; }
```

Geometry, never design. Every color, size, and typeface stays in the inline style where the
converter can see it. A conforming converter parses the inline styles of the classed kinds only and
ignores stylesheets entirely, so nothing written here can reach the presentation file. The preview
cannot drift from the deck, and the block cannot become a place to hide a value the converter would
have refused.

Give the page itself the same canvas fill the slides declare, set on the `body` element where a
value belongs, and leave no gutter between slides. A contrasting page color and a gap around each
slide turn the preview into a document viewer showing pages, which is a different artifact from the
one being authored: the deck has no page frame, no margin, and no color behind it, and a reviewer
who sees one starts judging the wrong composition. Flush and same-colored, the only seam is the
previous slide's footer meeting the next slide's header rule, which is how the deck reads anyway.
The `body` element is never converted, so a style attribute on it is ignored exactly like the
stylesheet.

Then look at the slides before converting, and look at all of them. Text is measured by the font,
not by the number the author estimated, so a title that was expected to fit can wrap to a second
line and land on the paragraph beneath it. That collision is in the presentation file too: a text
box overflows its declared height rather than shrinking to fit.

Do not rely on looking, though. This failure is measurable and therefore should be measured: text
taller than its declared box, two text objects overlapping once wrapped, and any object outside the
canvas are three checks a browser can run over every slide at once. Shapes may overlap freely and
text may sit on a shape, since a label inside a bar is composition; only text against text is a
collision. This repository's `tools/check_layout.mjs` is one implementation. Reviewing by eye is
what lets this defect through — not because reviewers are careless, but because attention does not
hold across every slide of every revision, and this is exactly the class of defect that hides in
the slides nobody opens twice.

## What does not convert

These constructs have no representation as a native object. Each one forces the whole region that
uses it to flatten into a raster, and a flattened region is no longer editable, searchable,
recolorable, or legible to assistive technology.

- Layout that resolves at runtime: flexbox, grid, floats, percentage or `auto` dimensions,
  `calc()`, margin collapse, and any position other than an absolute px box.
- Conditional rendering: media queries, container queries, and `:hover`, `:focus`, `:active`, or any
  other state selector.
- Effects with no shape equivalent: gradients of every kind, `box-shadow`, `text-shadow`, `filter`,
  `backdrop-filter`, `transform`, `opacity` on containers, `mix-blend-mode`, and `clip-path`.
- Generated and external content: `::before`, `::after`, `content`, background images, SVG, canvas,
  iframes, and web fonts that are not installed on the machine that opens the file.
- Raster images. An image is the one element that is never manipulable. Treat every image as a
  deliberate exception that must be justified in the delivery note, never as a convenience.

Substituting a picture for a region that failed to convert is a scope change, not a rendering
detail. Disclose it; do not close the gap silently.

## Acceptance

A presentation file meets this contract when every slide holds the expected object count, every text
region is a text box whose string matches the authored copy exactly, no region was rasterized, type
sizes hold at the delivered slide size, and the object inventory is reproducible from the file itself
rather than asserted. Verify against the file, not against the HTML that produced it.

A conforming converter and inspector are provided in this repository's `tools/` directory. They are
a reference implementation, not part of this skill's contract: any converter that preserves this
subset and produces the same inspectable inventory satisfies it.
