# Executive decision memo

Build an executive memo as a conclusion-led argument, not a miniature dashboard. Use five slides
when the brief does not specify another bounded sequence:

1. Situation — state the decision context and why it matters now.
2. Evidence — show the smallest sufficient comparison with direct annotation.
3. Implication — explain what the evidence changes and what it cannot establish.
4. Decision — name the recommended bounded action and its owner or scope.
5. Risk and next step — expose uncertainty, measurement, timing, and the next review point.

Write a takeaway title and one defensible claim per slide. Give each slide one dominant visual idea,
at most one primary chromatic emphasis, and enough empty space for the claim to lead. Label charts
directly; include period, units, source, and limits in readable type. Do not use dashboard tiles,
ornamental cover art, repeated navigation chrome, or a dense appendix disguised as body slides.

Render every slide at full size and inspect for clipping, contrast, minimum text size, and whether
the decision remains clear when charts are viewed in grayscale.

## When the deliverable is an editable presentation file

A slide the recipient can open but not edit is a picture of a memo. When the brief asks for a
presentation file rather than a page, every element the recipient would reasonably want to move,
retype, recolor, or realign must arrive as a native object in that file: text as text, rules and
bars and panels as shapes, and chart marks as individually addressable shapes.

Design for that outcome from the first layout decision, not as an export step afterward. A composition
built on runtime reflow, responsive breakpoints, hover state, or effects that only exist in a browser
cannot be carried across, and discovering that at export time means redesigning under deadline. Read
[pptx-safe-html.md](pptx-safe-html.md) before laying out a deck destined for a presentation file; it
defines the authoring subset that converts and the constructs that do not.

Under an active profile, apply the declared canvas, type roles, geometry, semantic mapping, and voice
from the declaration. Keep the recommendation in the declared action treatment when a status color is
already carrying critical evidence.
