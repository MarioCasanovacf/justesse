# Profile declaration

When `personal:<name>` is active, the requester must decree the profile. This file is the required
form. Ask for every unanswered field in one consolidated request, wait for concrete answers, and do
not begin design work until the declaration is complete. Record the completed declaration with the
deliverable so the same flag resolves to the same system on the next run.

Ten fields are required. A profile is declared only when all ten hold concrete values.

## Always ask with an example attached

Never ask a field bare. A bare question invites a mood where the form needs a measurement, and then
the whole exchange is spent re-asking. Attach a worked example to every question, in the field's own
answer shape, so the requester can see the grain of answer expected before they write one:

> **Profile name** — the short handle the flag resolves to, e.g. `atlas`.
> **Base surface** — the canvas color as a hex value, e.g. `#FFFDF7`. Not "off-white".
> **Hairline weight** — the thin rule weight in px, e.g. `1`. Not "thin".

The example fixes the shape of the answer. It does not propose the answer. Copying an example is
itself a non-answer: these values exist to be recognized, not adopted, and a declaration that echoes
this file has declared nothing.

## The ten fields

| # | Field | Required answer | Example |
| ---: | --- | --- | --- |
| 1 | Identity | Profile name, owner, the artifact scope the flag is authorized for, and one sentence naming what the profile is for. | name `atlas`; owner Atlas Research Cooperative; scope quarterly research notes and internal decision memos; purpose "present bounded quantitative research without implying commercial claims" |
| 2 | Canvas | Base surface color as a hex value, foreground ink color as a hex value, and either the two hex values of a dark variant or an explicit statement that none exists. | surface `#FFFDF7`; ink `#121212`; dark variant none |
| 3 | Type roles | Display, prose, UI, and data/notes. For each: family name, fallback stack, and availability stated as installed, licensed, or substitute-required. | display Source Serif 4, fallback `Georgia, serif`, installed; data Source Code Pro, fallback `ui-monospace, monospace`, licensed |
| 4 | Semantic color | Positive, warning, negative, neutral, and structure. For each: one hex value and at least one non-color redundancy that carries the same meaning. | positive `#1F5F3F` with a direct label and an upward marker; neutral `#5F5F5F` with a direct label and a dashed line style |
| 5 | Action treatment | How a primary action is rendered, stated so it cannot be confused with any of the five semantic roles on the same surface. | "an ink-outlined button with an underlined label, never a status fill" |
| 6 | Geometry | Corner radius in px, hairline and emphasis rule weights in px, elevation posture, and the spacing base unit in px. | radius `0`; hairline `1`; emphasis rule `3`; spacing base `8`; elevation "no shadow at any level, separation comes from rules and spacing" |
| 7 | Voice | Grammatical person, heading letter case, register in three adjectives, and the constructions the profile refuses. | first person singular; sentence case; precise, restrained, impersonal; refuses exclamation marks, superlatives, brand-we |
| 8 | Exclusions | At least five named visual or verbal effects the profile rejects outright. | gradients; glow and glass; automatic dark mode; spring and bounce motion; stock photography of people |
| 9 | Posture | Density and motion, each chosen from a bounded set the requester states. | density "balanced, one evidence module per fold"; motion "none beyond focus states" |
| 10 | Evidence | What must accompany a displayed number: unit, period, source, and how uncertainty is shown. | unit on every axis and total; ISO week range, unbroken; named dataset and capture date in the caption; interval bands on every estimated series |

## Reject non-answers

An answer is concrete when it can be applied without a second interpretation. Reject and re-ask when
a field arrives as any of the following. Re-ask with the example attached, as above.

- A placeholder, a "to be defined", an empty value, or a field marked not applicable when the form
  requires it.
- A deferral: "you decide", "use your judgment", "whatever fits", "the usual", or silence treated as
  assent.
- A borrowed value: "same as the last deck", "like the other profile", or a value lifted from this
  skill's own examples, references, or harness fixtures. The Example column above is the most likely
  source of this failure, so check answers against it before accepting them.
- An underdetermined value: a color family instead of a hex value, a range instead of a number, a
  mood instead of a typeface, or an adjective where the form asks for a measurement.
- A reference to an external artifact the requester has not supplied, when resolving it would mean
  inferring the system from that artifact rather than reading a declaration.

Re-ask only for the fields that failed. Do not re-open fields already answered concretely, and do
not expand the form beyond these ten.

## Apply the declaration structurally

Once declared, express the profile structurally rather than by pasting its tokens onto a generic
composition. The declared values set the vocabulary; the composition still has to earn coherence
through hierarchy, measure, spacing, and evidence. A profile applied as a color swap and a font
swap has not been applied.

Hold the declaration stable across surfaces. Read
[profile-data-semantics.md](profile-data-semantics.md) for how the five semantic values must behave
once declared, and [surface-translation.md](surface-translation.md) for carrying one declared
worldview across different surface jobs.
