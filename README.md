# Justesse

A model-, runtime-, and vendor-independent design skill. It turns design taste into an inspectable
operating contract rather than a prompt tied to one agent. A deterministic calibration harness is
included as supporting infrastructure, not as the product itself.

The repository has two layers:

- [`skill/justesse/`](skill/justesse/) is the single canonical skill.
  It contains no provider metadata, API dependency, framework mandate, or engine-specific command.
- [`harness/`](harness/) contains the frozen fixture, semantic contract, blind A/B rubric, and
  deterministic checks used to evolve the skill without reducing taste to arbitrary preference.

## What it covers

The skill routes work by design problem rather than by software stack:

- marketing and conversion surfaces
- product UI, dashboards, and transactional flows
- preserve-mode and overhaul-mode redesigns
- reference-to-code work and visual review
- data visualization and numerical composition
- image concepts
- executive decision memos and editable presentation files

## Profiles are declared, never bundled

This repository ships the profile mechanism and no profile. There is no built-in personal design
system to inherit, and no named individual's palette, typography, materiality, or voice lives in
this tree.

A profile activates only when the request contains the exact flag `personal:<name>`. Activation
does not grant a visual system: it opens a ten-field declaration the requester must answer
concretely before any design decision is made. Unanswered fields cannot be filled by inference, by
another profile, or by anything in this repository's own examples and fixtures. Without the flag,
the skill stays brand-neutral.

Check a declaration before designing against it:

```bash
python3 harness/validate_profile.py path/to/declaration.json
```

The gate enforces completeness and concreteness. It rejects placeholders, deferrals such as "you
decide", borrowed values, and answers that name a mood where the form asks for a measurement.

## Use it from any agent

Give the executing agent access to the complete
[`skill/justesse/`](skill/justesse/) directory and instruct it to
use `SKILL.md` as the routing contract. A runtime may mount, copy, symlink, index, or inject that
directory through its own discovery mechanism, but the adapter must not rewrite the skill or add
new semantics.

Example request without the personal profile:

> Use the Justesse skill to redesign this dashboard. Preserve the existing stack,
> routes, data contracts, analytics, and accessibility behavior. Explain the design read and
> validate the result at narrow and wide sizes.

Example request with a declared profile:

> Use the Justesse skill with `personal:<name>` to create an executive decision memo and a personal
> case study. My declaration is at `./declaration.json`. Treat charts as evidence, preserve semantic
> color, and verify numeric alignment at actual size.

If that declaration is missing or incomplete, the correct response is to ask for the missing fields
and stop, not to design something plausible in the meantime.

The agent first selects an operating mode, then loads only the references linked for that mode.
Availability of browsing, image generation, motion libraries, or a particular frontend framework
is always conditional.

## Build an editable presentation

A slide the recipient can open but not edit is a picture of a memo. Interface HTML resolves its
layout at runtime; a slide canvas has no runtime, so interface HTML can only be photographed into a
deck, never carried into one. [`tools/`](tools/) closes that gap for the authoring subset defined in
[`pptx-safe-html.md`](skill/justesse/references/pptx-safe-html.md): absolutely positioned `text`,
`rect`, `ellipse`, and `line` objects on a fixed 1280x720 canvas.

```bash
python3 tools/html2deck.py deck.html deck.pptx
python3 tools/inspect_pptx.py deck.pptx
```

The converter emits OOXML directly using only the standard library, so text arrives as live text and
every mark arrives as its own shape. Constructs outside the subset — flexbox, percentages,
gradients, shadows, transforms, generated content — raise an error naming the element and the
offending declaration instead of flattening the region into a raster.

The inspector reads the inventory back out of the written file and reports any rasterized region.
That direction matters: a converter can claim it emitted native objects, but only the file can show
it. Verify against the file, not against the HTML that produced it.

Because the model writes the HTML once and every later iteration is a process start, rebuilding a
deck ten times costs what building it once costs.

## Validate the capability

The validation path uses only the Python standard library:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 harness/validate_skill.py
python3 harness/validate_benchmark.py
```

The tests verify structure, direct reference routing, provider neutrality, product-contract
preservation, explicit profile activation, the ten-field declaration gate, semantic chart color,
single-grey discipline, numeric alignment, the presentation authoring contract and its converter
round trip, upstream provenance, and the complete upstream MIT notice.

## Evolve taste through evidence

Use [`harness/rubric.md`](harness/rubric.md) to score blind specimens generated from the same
[`harness/fixture.json`](harness/fixture.json). Keep a no-flag negative control in every calibration
round. Promote a rule only when it survives the hard gates and does not leak a declared profile into
brand-neutral work.

Automated scoring is evidence, not authorship. The profile owner's judgment that they would publish
the result remains the final calibration input.

## Provenance and license

This work is inspired by
[`Leonxlnx/taste-skill`](https://github.com/Leonxlnx/taste-skill) at commit
`b17742737e796305d829b3ad39eda3add0d79060`. The complete upstream MIT notice is preserved at
[`skill/justesse/LICENSE.upstream`](skill/justesse/LICENSE.upstream).
The adaptation in this repository is distributed under the MIT License.
