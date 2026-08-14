# Justesse · profile A/B rubric

Score blind specimens before revealing A or B. A score is evidence, not a substitute for the
profile owner's final judgment. Any failed hard gate blocks promotion regardless of total.

| Dimension | Points | What earns full credit |
| --- | ---: | --- |
| Structural profile fidelity | 25 | Every visual and verbal choice traces to a field of the completed declaration, and the composition expresses that declaration structurally through hierarchy, measure, spacing, and evidence. It does not merely paste declared tokens onto a generic layout, and it invents nothing the declaration did not state. |
| Semantic data communication | 20 | Status meanings are stable, perceptually separable, directly labeled, and reinforced without color. Ink structures evidence rather than impersonating a status. |
| Surface translation | 15 | The deck concludes, dashboard supports action, landing establishes authorship and capability, and report demonstrates. They share a worldview without sharing one layout. |
| Veracity and narrative rigor | 15 | Every claim is supported by the frozen synthetic fixture, units and period agree, limitations are visible, and descriptive evidence is not presented as causality. |
| Hierarchy and legibility | 10 | Purpose, reading order, comparison, exception, and next step are immediately legible at the required sizes. |
| Accessibility and perception | 10 | Contrast, keyboard/reading order where applicable, direct labels, grayscale interpretation, and narrow-width behavior remain usable. |
| Production quality | 5 | Requested artifacts, provenance, responsive renders, slide renders, and QA commands are complete and replayable. |
| **Total** | **100** | |

## Per-surface judgment

- **Dashboard:** state, change, exception, and action are understood in five seconds; color is not
  asked to carry the chart alone.
- **Decision memo:** situation → evidence → implication → decision → risk/next step; one claim and
  at most one dominant chromatic emphasis per slide. When the deliverable is a presentation file,
  every element is a native editable object and no region was rasterized.
- **Personal landing:** the author's way of thinking is visible without pretending Subscriber
  Feedback is a commercial product or client engagement.
- **Case study/report:** question, data, method, findings, limits, and decision form one argument;
  figures are evidence, not decoration.

## Fine-grained comparison

Where paired specimens have object inventories, run `tools/diff_specimens.py` before scoring. Its
graded deltas (surface temperature, geometry to the pixel, type size and family) are evidence for
the scorer, not a substitute for judgment, and its convergence verdict executes the hard gate that
the flagged variant and the no-flag control must be measurably distinct designs rather than one
design carrying different words.

## Promotion rule

Promote B only when all hard gates pass, its total exceeds A by at least 15 points, no surface
scores lower than its A counterpart, and the no-flag negative control remains brand-neutral.
Automated evaluation must leave the final human gate pending until the profile owner explicitly
says all four pieces are work they would publish as their own.
