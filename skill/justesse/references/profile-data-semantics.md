# Profile data semantics

Field 4 of the declaration supplies five hex values and their non-color redundancies. This file
governs how those declared values must behave. It supplies no values of its own.

| Meaning | Source | Required non-color redundancy |
| --- | --- | --- |
| Positive / success | Declared positive value | Direct label plus an upward or affirmative marker |
| Warning | Declared warning value | Direct label plus a warning marker or annotation |
| Negative / critical | Declared negative value | Direct label plus a downward or critical marker |
| Neutral | Declared neutral value | Direct label plus distinct position, pattern, or line style |
| Structure / reference / total | Declared structure value | Axis, rule, baseline, reference, or total plus a direct label |

Keep each meaning stable across every flagged surface. Use color sparingly. Never ask hue to carry
status alone: add text labels and at least one redundant sign, shape, pattern, line style, position,
or annotation. Verify grayscale interpretation, contrast, and legibility at the required viewport or
slide size. The structure value organizes evidence; it is not another status series.

Prevent CTA/status collision. On a surface where the negative value communicates critical state, do
not also use it for a primary action, link emphasis, or decorative highlight. Use the declared
action treatment from field 5 instead. Likewise, do not turn the positive, warning, or neutral value
into a CTA color. One chromatic role must not imply two meanings on the same surface, and decorative
color must never compete with the evidence.

## Use semantic chart recipes

Choose the chart from the analytical question before assigning color.

| Question | Preferred treatment |
| --- | --- |
| One bounded KPI | Set the value in the structure color unless it carries status; use a status color only when the label states that same status. Include unit, period, and comparison. |
| Positive / neutral / negative composition | Prefer a 100% stacked bar with stable order, direct labels anchored to their actual segments, and a textual total. Use the three declared status values plus a redundant marker or pattern. Never place unequal segment values in equal-width label columns. |
| Status over time | Prefer small multiples when lines would overlap. If one plot is materially clearer, use direct end labels and distinct solid / dashed / dotted lines or marks in addition to semantic color. |
| Target or threshold | Prefer a bullet chart or position-on-scale plot. Draw the target or baseline in the structure color and color the observed value only when its status is known. |
| Ranked drivers or exceptions | Prefer sorted horizontal bars. Use the structure color for neutral magnitude, the negative value only for critical drivers, and the warning value only for items requiring attention. |
| Deviation around zero | Use a diverging bar with a zero line in the structure color, the positive value for favorable deviation, and the negative value for unfavorable deviation. |
| Uncertainty | Add intervals, bands, whiskers, or ranges. Never imply certainty through a saturated solid shape. |

A donut is acceptable only for a single snapshot with no more than three directly labeled parts when
exact cross-category comparison is not the main task. Otherwise use a stacked bar or table. Do not
use gauges, radar charts, 3D charts, decorative area fills, or dual axes.

For nominal categories without positive, warning, negative, or neutral meaning, do not recycle the
semantic palette as arbitrary decoration. Use the structure color with direct labels and clearly
different markers, line styles, positions, or small multiples. If more than three neutral series
would make those encodings hard to scan, split the view or use a table instead of introducing a
rainbow.

Use no more than one grey data encoding in a chart. Render the declared neutral at full strength and
never accompany it with a lighter, darker, or translucent grey data series. Faint structural rules
are acceptable only when they cannot be mistaken for data. If another neutral comparison is
required, change its line style, marker, position, or use small multiples instead of adding grey.
