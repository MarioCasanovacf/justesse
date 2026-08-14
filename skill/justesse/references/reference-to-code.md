# Reference to Code

Use when screenshots, mockups, existing websites, sketches, or mood references inform an
implementation. Reproduce design intent, not accidental pixels.

## Read the evidence

1. Inventory visible structure: landmarks, grid, hierarchy, spacing rhythm, type roles, palette,
   surfaces, imagery, icons, states, and interaction clues.
2. Separate direct evidence from inference. A single desktop screenshot does not prove mobile
   behavior, hover states, sticky behavior, animation, semantic structure, or the font source.
3. Identify what the user wants transferred: exact composition, visual language, component
   behavior, mood, or selected details. Avoid copying protected branding or content outside scope.
4. Map each retained quality to the target project's existing tokens, components, assets, and
   layout primitives before creating new ones.

## Write the fidelity inventory before building

Before implementation, write down every major visible ingredient of the reference and the medium
that will carry it: existing project component, semantic markup and styling, authored vector,
project asset, supplied asset, or a disclosed placeholder. The element that never gets written down
is the element the build silently drops, and a fidelity gap discovered at review costs a rebuild
that a one-screen inventory would have prevented.

- Decide each medium from what the reference actually shows, not from what feels convenient in the
  current stack. Material with lighting, depth, texture, or a human figure is an image and needs a
  real asset or a disclosed placeholder; writing "vector" or "CSS" for it is not a medium choice
  but a quiet deletion of the reference. Countable geometry, diagrams, controls, and flat shape
  systems are authored vector or markup territory, and turning those into an image trades away
  states, responsiveness, and accessibility.
- A field or texture built from many small elements carries a quantity commitment. Note its
  approximate density and coverage; rebuilt at a tenth of the density it passes every checklist and
  still is not the reference.
- Type carries its own row: name the role and how close the available face actually is, and render
  one real headline against the reference before building on it. A visibly wider or lighter
  silhouette means every section built on it inherits the miss.
- Include the primary action's treatment as its own row. When the reference gives the main action a
  distinctive treatment, shrinking it to a border trick is the token-compliance version of
  fidelity.

Dropping an ingredient the inventory names is a scope decision for the user, made before building,
never a silent flattening after it.

## Translate, do not trace blindly

Preserve semantic HTML, reading order, keyboard behavior, responsive logic, real content, and target
contracts even when the reference does not expose them. Infer a flexible grid and spacing system
rather than freezing screenshot coordinates. Use content-driven breakpoints and test long, short,
missing, and localized values.

When a referenced font, icon, image, or library is unavailable or unauthorized, choose an honest
project-native substitute and report the difference. Do not install dependencies or scrape assets
merely to make a screenshot comparison closer.

## Validate fidelity

Compare at the reference viewport and representative narrow and wide widths. Assess hierarchy,
proportions, alignment, type roles, color relationships, asset treatment, and intended interaction.
Prioritize perceptual structure and product correctness over isolated pixel differences. List
known deviations and whether they are deliberate, constrained, or unresolved.
