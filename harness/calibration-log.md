# Calibration log

One entry per controlled round. Specimens live under `specimens/` (untracked by design); each entry
records the hashes, commands, scores, and verdict needed to audit a round without shipping its
artifacts.

## Round 2 — 2026-08-14 — candidate: skill at `7c5c0dd` with `personal:meridian`

**Question.** Do the declared-profile mechanism and the rules absorbed since round 1 (impeccable
tranches 1–2, the finishing pass, the comparison instrument) produce work that beats the archived
baseline under the frozen fixture, without profile leakage or design convergence?

**Setup.** Fixture `subscriber-feedback-v1` (sha `cb786192…` per provenance). Baseline A: the
archived `specimens/variant-a` round-1 output (statuses as documented in `specimens/README.md`).
Candidate B: all four surfaces produced fresh under `personal:meridian`, a deliberately fictional
declaration (sha `dc4bea81…`) that passed `validate_profile.py` 10/10 — after the gate itself
rejected one field ("none" for motion) and re-asked it with its example, which is the mechanism
working. Negative control: `index.html` produced with no flag. Deck built through
`tools/html2deck.py` (5 slides, 81 native objects, 0 rasterized regions), renders at exactly
1600×900. Bounded verification: one batched inspection round (three findings: a clipped count
label, sub-legible small multiples at 390 px, one overclaiming deck footnote), one batched fix, one
confirming round, stop.

**Hard gates.** All eight pass. Notables: gate 4 (every flagged choice resolves from the complete
declaration) held by construction and by the gate run; gate 5 (control stays brand-neutral) and
gate 8 (anti-convergence) were executed by `tools/diff_specimens.py --expect-distinct` — flagged
landing vs. control: DISTINCT DESIGNS; candidate deck vs. baseline A deck: DISTINCT DESIGNS.

**Scores** (baseline A / candidate B):

| Dimension | A | B |
| --- | ---: | ---: |
| Structural profile fidelity (25) | 8 | 22 |
| Semantic data communication (20) | 14 | 18 |
| Surface translation (15) | 12 | 13 |
| Veracity and narrative rigor (15) | 12 | 15 |
| Hierarchy and legibility (10) | 8 | 8 |
| Accessibility and perception (10) | 7 | 9 |
| Production quality (5) | 4 | 5 |
| **Total** | **65** | **90** |

Delta +25 ≥ the +15 promotion threshold; per-surface comparison shows no B surface below its A
counterpart, with the personal landing the narrowest call (A's is visually richer; B's wins on
declaration fidelity, redundancy, and current disclosure).

Score rationale, briefly: A expresses a coherent system but traces to no declaration and lets its
accent green carry both status and decision emphasis; its stacked bars lean on adjacency with
printed values as backup; its disclosure predates the fixture rebrand. B traces every visual choice
to the meridian declaration, keeps five stable meanings with non-color redundancy on every status,
reserves the action treatment, and carries the current disclosure verbatim on every surface.

**Limitations, on the record.** The scorer built candidate B, so the blind is procedural
(specimen labels, rubric scored dimension-by-dimension against written criteria), not actual.
The meridian owner is fictional, so the rubric's human gate devolves to the harness operator:
**human gate pending — the operator has not yet marked the four pieces "I would publish this as
mine."** Promotion of the absorbed rules is provisional on that gate.

**Verdict.** Mechanism promoted: the declaration gate, the semantic sourcing, the anti-convergence
gate, and the presentation path all executed as designed and left replayable evidence. Rule
promotion provisional pending the human gate. No rule regression surfaced; no specimen-specific
value was copied into the skill.

**Round 2b — same day — token-emitter fidelity check.** After `tools/declaration2tokens.py`
landed, the three HTML surfaces were rebuilt consuming the emitted tokens by reference
(`--surface: var(--j-surface)` and so on; derived values such as panel tints and hairline colors
stayed outside the declaration's authority) and re-inventoried at both viewports.
`diff_specimens.py --expect-same` against the hand-transcribed originals: dashboard, personal
landing, and case-study report all report **SAME DESIGN, delta-free**. The emitter is a faithful
mechanical projection of the declaration; the transcription step, where drift used to live, is
gone. The deck path keeps literal values by design (the presentation-safe subset resolves
everything at authoring time) and was not part of this check.
