# Profile declaration

When `personal:<name>` is active, the requester must decree the profile. This file is the required
form. Ask for every unanswered field in one consolidated request, wait for concrete answers, and do
not begin design work until the declaration is complete. Record the completed declaration with the
deliverable so the same flag resolves to the same system on the next run.

Ten fields are required. A profile is declared only when all ten hold concrete values.

| # | Field | Required answer |
| ---: | --- | --- |
| 1 | Identity | Profile name, owner, the artifact scope the flag is authorized for, and one sentence naming what the profile is for. |
| 2 | Canvas | Base surface color as a hex value, foreground ink color as a hex value, and either the two hex values of a dark variant or an explicit statement that none exists. |
| 3 | Type roles | Display, prose, UI, and data/notes. For each: family name, fallback stack, and availability stated as installed, licensed, or substitute-required. |
| 4 | Semantic color | Positive, warning, negative, neutral, and structure. For each: one hex value and at least one non-color redundancy that carries the same meaning. |
| 5 | Action treatment | How a primary action is rendered, stated so it cannot be confused with any of the five semantic roles on the same surface. |
| 6 | Geometry | Corner radius in px, hairline and emphasis rule weights in px, elevation posture, and the spacing base unit in px. |
| 7 | Voice | Grammatical person, heading letter case, register in three adjectives, and the constructions the profile refuses. |
| 8 | Exclusions | At least five named visual or verbal effects the profile rejects outright. |
| 9 | Posture | Density and motion, each chosen from a bounded set the requester states. |
| 10 | Evidence | What must accompany a displayed number: unit, period, source, and how uncertainty is shown. |

## Reject non-answers

An answer is concrete when it can be applied without a second interpretation. Reject and re-ask when
a field arrives as any of the following.

- A placeholder, a "to be defined", an empty value, or a field marked not applicable when the form
  requires it.
- A deferral: "you decide", "use your judgment", "whatever fits", "the usual", or silence treated as
  assent.
- A borrowed value: "same as the last deck", "like the other profile", or a value lifted from this
  skill's own examples, references, or harness fixtures.
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
