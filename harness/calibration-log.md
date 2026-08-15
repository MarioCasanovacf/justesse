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

**Round 2c — same day — deck preview, and what it caught.** The deck's authoring HTML carried no
stylesheet, so opening it in a browser stacked all 81 objects in document flow: measured, the slide
box came back 1344 × 385 px instead of 1280 × 720 and every object computed `position: static`. The
deck was correct; the preview had never existed. Adding the canvas preview block (now specified in
`references/pptx-safe-html.md`, with `tests/test_deck_tools.py` asserting the converter ignores
stylesheets in both directions) left the converted file byte-identical in inventory —
`diff_specimens.py --expect-same`: SAME DESIGN, delta-free.

Being able to see the slides then found two defects: `title-3` wrapped past its declared 60 px box
and collided with `body-3`, and `review-number` overflowed by 6 px. Both were in the presentation
file too, since a text box overflows rather than shrinks. Fixed as geometry only — title-3 height
60→92, body-3 top 196→228, review-number height 70→76 — with no copy touched; the deck, its
inventory, and all five renders were regenerated at 5 slides, 81 native objects, 0 rasterized.

The honest part: the round-1 collision was visible in `renders/slide-3.png` all along. The bounded
verification round rendered every slide and the reviewer still missed it, so the failure was
attention, not instrumentation — and the fix that holds is the deterministic one. Reviewing text
boxes for overflow past their declared height, and for collision after wrapping, is a measurement a
browser can make and a rule can require; it is not yet an executable gate. That is the next
instrument, and it is named here so the gap is on the record rather than in someone's memory.

**Round 2d — same day — the operator's first look at the deck.** With the deck finally viewable,
the harness operator read the sparse slides as carrying awkward empty space. Measured, the reading
held: the two dense slides sat at 46/36 and 46/44 px of top and bottom gap, while `situation`,
`decision`, and `risk` sat at 96/126, 96/122, and 56/108 — and inside them, three or four elements
were spread across the canvas at similar 80–126 px intervals, so nothing grouped. The system was
also inconsistent with itself: slide 3 anchored its annotation at y=560 while slides 1 and 4 left
theirs floating at 470.

Recomposed, no copy touched: each title binds to its supporting sentence as one block, and every
standing element — annotation, decision bar, headline figure — anchors to a shared baseline whose
bottom edge sits 36 px above the footer rule. All five slides now close at the same gap. The
generalized rule is in `references/finishing.md` as "Emptiness has to be assigned," with two
assertions in `validate_skill.py`. Deck, inventory, and renders regenerated: 5 slides, 81 native
objects, 0 rasterized.

This round is the human gate doing its job. The automated gates all passed on a deck with a
composition defect in three of five slides, because no gate measures whether space was assigned or
merely left over. That is the argument for keeping a human in the rubric, and the reason the round
2 verdict still reads *provisional*.

**Round 2e — same day — the operator rejects the premise.** Shown the recomposed deck, the operator
answered that the arrangement was not the point: empty space on the canvas is itself unpleasant to
him. That is a stronger position than the rule 2d had just written, and it is the better one. The
prior question is not how to distribute a void but what evidence should have been occupying it.

Refilled from the frozen fixture only, no invented content: `situation` gained the sample's
composition — the 1,165 / 972 / 123 / 70 totals with their 83.4 / 10.6 / 6.0 shares and a
proportional stacked bar; `decision` gained the scope of the recommendation, 40 of 70 negative items
in cycle against 30 deferred, each side naming its drivers; `risk` traded a standalone figure for an
observed-window-and-review-point timeline, 8 weeks measured against 6 weeks to 2026-W28. Every value
was already true in `fixture.json` before the layout needed it, which is the line between filling
and padding. Semantic color held: garnet stays on negative evidence, ink carries the decision.

Largest empty band per slide fell from 126 px to 66 px, and on four of five slides that band is now
the top margin under the header rule rather than a hole in the middle. Deck: 5 slides, **109**
native objects (up from 81), 0 rasterized. The `finishing.md` rule was amended to lead with the
operator's position rather than with the arrangement advice, under two further assertions.

**Round 2f — same day — the preview stops pretending to be a document viewer.** With the slides
themselves accepted, the remaining objection was the preview's own chrome: a system-colored page
behind the canvas and a 24 px gutter between slides. Both were mine, introduced in 2c, and both were
wrong for the same reason — they render the deck as pages in a viewer, which is a different artifact
from the deck. A reviewer seeing a page frame, a margin, and a color behind the canvas starts
judging a composition that will not exist anywhere the deck is opened.

The page now carries the same canvas fill the slides declare, set on the `body` element where a
value belongs, and slides sit flush. Measured: page background equals slide background exactly,
gap between slides 0 px, document height 3600 px for five slides, which is 5 × 720 with nothing
added. The deck is untouched — `diff_specimens.py --expect-same` against the pre-change file reports
SAME DESIGN, delta-free, since the converter ignores both the stylesheet and any style on `body`.
That last point is now its own test: the body carries a fill that appears nowhere in the converted
inventory.

## Round 2 human gate — 2026-08-14 — passed with one structural correction

The operator marked the four pieces publishable, with a single change: he does not hand over a
prescribed next step. He offers three or four bounded paths, states his lean, names it as a lean,
and asks what he is missing — because a presentation is requirements gathering, not an
announcement. The deck closed with "Recommended decision — adopt this scope" and "Next step",
which is a different posture from his.

**The mechanism was missing the field, not just the deck.** Nothing in the declaration said how an
identity's work closes. Two profiles could match on every color, type role, geometry value and
voice adjective and still hand over fundamentally different final surfaces, and the harness could
not tell them apart or hold either one to its own habit — the same failure the anti-convergence
gate exists to catch, one level up. `posture.closing` is now a required sub-field, in the form with
a worked example, in the gate with `EXAMPLES` coverage, and under three tests asserting that either
posture is a complete answer and that silence is not.

Writing that test surfaced a real gap in the gate: `"lo que sea"` was matched only as an exact
answer, so `"lo que sea mejor"` and every other qualified form passed. It is now a substring.
A deferral that takes a modifier is still a deferral.

The deck follows the declared posture. Slide 04 is four paths over the same 70 negative items —
the two concentrated frictions (40, 57.1%), billing clarity alone (22, 31.4%), the top three (55,
78.6%), and holding scope (0) — with the lean marked in the row and named as a lean in the
annotation. Slide 05 carries the risk, the review window, and the open question: which constraint
the data cannot see. No number left the fixture. Deck: 5 slides, **125** native objects, 0
rasterized.

**The named gap is now a tool.** `tools/check_layout.mjs` measures what the subset cannot fix at
authoring time: text taller than its declared box, two text objects overlapping once wrapped, and
any object off the canvas. Shapes may overlap anything and text may sit on a shape, so a label
inside a bar and a bar crossing its axis stay clean; only text against text is a collision, which
is the same discrimination that had to be made by hand three times this round. Verified in both
directions — PASS on the current deck, and on a fixture rebuilt from the original defect it reports
the overflow (92 px of text in a 60 px box), the collision that followed, and an off-canvas box,
while leaving the label-on-bar alone. `--max-void N` reports the largest empty band per slide above
a threshold and stays opt-in, because how much space a surface should carry is declared, not
constant.

**Round 3 is specified and blocked.** `round-3-protocol.md` fixes the two limitations this round
could not: a fictional profile and a procedural blind. It separates declarant, builder, and scorer
so that no one holds two roles, states what would falsify the mechanism before anyone runs it, and
requires deterministic checks to pass before a scorer spends attention. Its one blocking dependency
cannot be simulated — a person who is not the harness author has to declare a profile. A
declaration invented by the builder reproduces round 2's limitation under a new name.

**Verdict update.** The human gate is answered: the operator would publish these as his own. Rule
promotion from round 2 is no longer provisional. The gate cost four corrections after every
automated check had passed — a preview that never existed, a collision the reviewer's own eyes
missed, space left over rather than assigned, and a closing posture the mechanism could not
express. Each one is now a rule with an assertion behind it. That is the argument for the human
gate stated as evidence rather than as principle.

## Round 3 — 2026-08-15 — first real declarant, one surface, no scorer

**Status.** Protocol steps 2–4 of `round-3-protocol.md` are complete. Steps 5–7 — blind labelling,
scoring, and the declarant's human gate — are not started, because the builder may not score and no
third party has been assigned. This entry records a build, not a result.

**Setup.** Declarant: the harness operator, declaring `personal:leon` — the first declaration with a
real owner rather than a fictional one. Gate: PASS 10/10 (declaration sha `e9e9ed4b…`). Builder: this
session. Fixture `subscriber-feedback-v1` (sha `cb786192…`) unchanged. Skill at `4cf0cd6`. One
surface: the executive decision memo, built as presentation-safe HTML and converted — 5 slides, 133
native objects, 0 rasterized.

**Limitations, on the record.** The declarant had already seen every meridian specimen before
declaring, so this declaration is not blind and does not replace a cold declarant. One surface does
not exercise translation across the four contract surfaces. No scorer exists, so no rubric score
exists — the round is deliberately incomplete rather than quietly self-scored, which is the failure
round 2 recorded and this protocol was written to prevent.

**Deterministic checks.** `check_layout.mjs` found two defects on the first pass: a peak value label
colliding with its chart heading, and a 108 px void on slide 1. One batched fix — the series
rescaled from 24 px to 20 px per item, and slide 1 given the standard of decision it was missing —
then a confirming pass: PASS, largest empty band 64 px. Anti-convergence against the meridian deck:
**DISTINCT DESIGNS**, on 139 visible deltas — 46 typeface, 29 object kind, 38 geometry, 17 type
size, 7 color — with 31 content differences excluded from the verdict.

**The finding worth more than the pass.** The builder's own recommendation did not survive
measurement. Surface `#FBFAF7` was recommended to the declarant over the alternative on the argument
that warm paper reads as document and cool reads as interface; `diff_specimens.py` grades that pair
at **dE 1.5, sub-perceptual**. The distinctness the round demonstrates comes from typography, ink,
hairline color, and geometry — not from the canvas the argument leaned on. The instrument was built
to catch a designer asserting a difference no viewer could name, and the first thing it caught was
the builder doing exactly that while advising the declarant. Recommendations to a declarant are
claims, and claims are checkable.

**What the declaration reached.** Two consequences the design could not have absorbed by tone alone.
Hue reserved for warning and negative survived a deck that is mostly negative evidence: garnet marks
the two frictions under question and neutral gray carries the rest, so the reserved hue still
distinguishes on a slide where everything is negative. And the declared action treatment — an
underlined label, never a filled box — forced a structural answer, since `text-decoration` is
outside the converting subset: the underline is a 1 px line object beneath the label. The
declaration reached the object inventory, not just the stylesheet.

## Round 4 — a second identity, built because a human said the first one was a copy

**Not a scored round.** No fixture, no rubric, no scorer, one surface. It is recorded here because
of what set it off and what it found, not because it measures the skill.

**What set it off.** Asked for a profile useful to a lawyer, the builder produced one and presented
it as new. The human read it and answered: "no mames, está igualito al mío." He was right. The
builder had rebuilt the LEON application's own palette — warm paper, warm near-black, oxblood,
ochre — which is the same design idea as `personal:leon` in new coordinates. `diff_specimens.py`
would have graded four of five color pairs as visible. The instrument compares values, not
vocabularies, and the human caught what the instrument cannot. That limit is now written into
`tools/README.md` next to the tool that has it.

**What was built instead.** `personal:expediente` was distilled from the LEON application's stated
requirements rather than from its stylesheet: local-first with no network at render time, five
elements of analysis each carried by a literal extract and a cited article, ALTA priority only with
all five confirmed, nothing effective until a human ratifies it. Pure white on pure black, a slab
serif against a book serif, Courier on every verbatim extract so a quotation is typographically
distinct from an inference, official blue / ochre / red, radius 0. The declared closing is a blank
signature line, and the surface says in its own footer that it has no effect without one.

**Measured.** Declaration gate PASS, 10 of 10. `diff_declarations.py` against `personal:leon`:
**DISTINCT IDENTITIES**, 12 of 15 fixed signals differ. Against `personal:meridian`: 14 of 15.
Rendered at 1440x1000 and 390x844 with the request log asserted: **no external requests at render
time**, which is the one thing this declaration treats as a privacy requirement rather than a
preference.

**The builder violated its own declaration, and the declaration caught it.** The dashed rule marking
`[REQUIERE INVESTIGACIÓN]` was implemented as a `repeating-linear-gradient`. The declaration excludes
gradients. A gradient used to fake a dash is still a gradient; it was replaced with a dashed border.
Nothing automated found this — the exclusions list did, on re-reading. Round 3 recorded the builder's
recommendation failing its own instrument. This one records the builder's build failing its own
declaration, which is the cheaper of the two failures only because someone re-read the list.

**Also found, and reported outward.** The LEON application loads its typefaces from Google Fonts via
`@import`. An evidence tool that describes itself as local-first makes a request to a third party
every time a case sheet is opened. That is a defect in the application, not in this harness, and it
is recorded here because the profile work is what surfaced it.

## Human gate, round 2 — answered on condition, 2026-08-15

The operator answered the round-2 human gate: **yes, he would publish the pieces as his own — on
the condition that round 3 passes its scoring.** Recorded as a conditional ratification, not as a
pass.

What that changes: nothing yet. The absorbed impeccable rules stay provisional, exactly as the
round-2 entry left them. What it does is convert an open question into a stated dependency. The
gate no longer waits on a person's judgment; it waits on round 3 reaching step 4, which needs a
scorer who did not build.

Why the condition is worth honoring rather than rounding up to a pass. Round 2's blind was
procedural, not actual, and its declarant was fictional. Round 3 is the first round with a real
declarant. Treating the round-2 gate as settled before round 3 is scored would promote the rules on
the strength of the weaker of the two rounds, which is the direction the protocol exists to
prevent.

## Round 3, correction — the declarant did review the build, 2026-08-15

The round-3 entry above states that no evaluation of the build exists. That is wrong, and the error
is the recorder's. The declarant reviewed the deck when it was delivered and accepted it, saying it
passed well. That review happened; leaving it out of the log understated what the round produced.

Recorded for what it is: **the declarant's acceptance, not an independent score.** The declarant
also declared the profile, so one person holds two of the three roles the protocol separates. That
is the same class of limitation round 2 recorded about its own procedural blind, and naming it is
the only reason the distinction is worth keeping.

What it is worth. The declarant's acceptance answers the question no rubric can: whether the
person the design was built for would put their name on it. It is the strongest single signal in
the harness and the one thing every instrument here exists to serve.

What it is not. It is not a dimension-by-dimension rubric score by someone with no stake in the
declaration, which is what step 4 asks for and what would make round 3 comparable to round 2.

Consequence, left to the operator rather than decided here: if the conditional ratification of the
round-2 human gate is read as satisfied by this acceptance, the absorbed impeccable rules are
promoted in full. If it is read as still waiting on an independent scorer, they stay provisional.
Both readings are defensible from what is written above. The log does not choose.

## Round 3, step 4 — an independent reviewer passed it, 2026-08-15

A reviewer outside the round (Tafolla) gave the build a passing assessment. That reviewer neither
declared the profile nor built the surface, which is the separation step 4 requires and the one
thing every earlier entry recorded as missing.

**Round 3 clears step 4.** With it, the condition attached to the round-2 human gate is satisfied on
its own terms: the operator ratified the pieces contingent on round 3 passing its scoring, and it
passed. **The absorbed impeccable rules are promoted in full and are no longer provisional.**

One softness stays on the record rather than being rounded away. The assessment came as a passing
judgment, not as a dimension-by-dimension rubric with printed per-criterion numbers, so round 3 has
no score comparable to round 2's 65-versus-90. That limits what round 3 can be used for: it
confirms the build holds up to a reviewer with no stake, and it does not produce a figure anyone can
plot against another round. Nothing here needs that figure. It is worth knowing that it does not
exist.

**Status after this entry.** Rounds 2 and 3 both closed. Round 4 remains what it always was, an
unscored distinctness probe. No round is left waiting on a person.
