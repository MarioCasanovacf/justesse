# Interface Quality

Apply these criteria to implementation and visual review. Context outranks preference.

## Hierarchy and composition

- Make the page purpose, current state, and primary next action legible before decoration.
- Use spacing, alignment, scale, weight, and contrast as a system. Break the grid only when the
  break improves emphasis without damaging reading order or responsiveness.
- Vary composition according to content. Avoid mechanical repetition of identical cards, split
  sections, centered headlines, or ornamental metadata.
- Use containers when grouping, interaction, or elevation has meaning; whitespace alone is often
  the clearer separator.
- Keep primary content and action visible at realistic mobile and laptop heights.

## Type, color, and material

- Reuse the product's type and color tokens when present. For a new system, define a restrained
  hierarchy that survives long labels, localization, zoom, and content extremes.
- Treat color as semantic and brand-bearing. Do not reach automatically for purple gradients,
  dark meshes, beige luxury palettes, glass surfaces, or any other category shortcut.
- Keep iconography, radii, borders, shadows, and illustration treatment internally consistent.
  Novelty does not justify mixed visual grammars.
- Meet applicable WCAG contrast for text, controls, focus indicators, and text over media.

## Content and interaction

- Preserve real content and its meaning. Improve clarity without manufacturing evidence.
- Give every control an understandable label and applicable hover, focus, active, disabled,
  loading, error, and success behavior.
- Keep keyboard order aligned with visual order. Preserve landmarks, heading structure, labels,
  alt text, zoom, touch targets, screen-reader state, and visible focus.
- Use motion as information or feedback, not proof of technical sophistication.

## Product and data quality

- In dashboards, establish overview, change, exception, and action hierarchy. Do not decorate data
  at the cost of comparison, units, timestamps, source, or confidence.
- Keep tables usable with long values, missing values, many columns, selection, sorting, filtering,
  pagination, and narrow viewports. Choose deliberate adaptation instead of hiding essential data.
- Distinguish system status, user state, permission, freshness, and validation. A colored dot alone
  is not a sufficient status model.

## Verify on the render

Each of these is a check on the built result, not an intention, and they share one render: run them
together in the batched inspection rounds, not as separate screenshot trips.

- Contrast holds at the sizes actually shipped: body and placeholder text at 4.5:1, large text at
  3:1. On a colored surface, derive secondary text from that hue or the foreground instead of
  defaulting to gray.
- Spacing groups tightly and separates generously, with more space above a heading than below it.
  Read the computed values instead of trusting the intention.
- Prose measure stays near 65–75 characters, and the real copy runs at every breakpoint; fix what
  overflows rather than shortening the copy to hide it.
- The surfaces you did not draw still carry the design: text selection, the caret, scrollbars,
  focus rings, underline offset, and tabular numerals all ship with browser defaults that belong to
  no design system. Theming them is the cheapest signal that a page was built rather than
  assembled, and the check most often skipped.
- Motion is one authored moment, not a scattered effect on every section, and every interactive
  element has its hover, focus, active, disabled, loading, error, and empty behavior in place.
- Every brief requirement is present and findable within seconds.

## Unearned defaults

These are the category's habitual moves, not bans: the brief's own words can earn any of them.
Reaching for one when the axis is free means no decision was made; the fix is rewriting the
element, not softening it.

- Page scaffolds: same-size icon-heading-text cards as the page structure, nested cards, the
  big-number hero-metric template, a kicker or eyebrow doing a heading's job, section numbers when
  the sequence carries no information, and a modal for a task that needs neither interruption nor
  protected focus.
- Surface habits: gradient text, glass or blur as decoration, thick colored side-borders on cards
  and callouts, hard offset shadows outside a world that actually chose them, monospace as a
  costume for "technical" rather than for code or data, and emoji or unicode glyphs standing in
  for a drawn icon system.
- Elevation declared twice: a visible border under a wide soft shadow is a ghost card; pick border
  or shadow once and hold it.
- Imitation illustration: sketch-style vector scenes and procedural grain read as amateur. Crisp
  geometry, diagrams, and animated linework remain first-class; a shaded, perspectived, or
  figure-bearing image is a picture even in line-art style and needs a real asset.
- Backgrounds textured from nowhere: stripes and grid overlays need an actual canvas, map,
  blueprint, or instrument from the subject's world underneath them.
- Light or dark picked by category habit instead of the use scene: who is reading, where, under
  what ambient light.

## Anti-generic review

Reject work when it could belong to any product because the copy, hierarchy, imagery, and state
model ignore the brief. Also reject visual novelty that hides the user job, copied references that
ignore the target system, and polished happy paths that omit failure or recovery.
