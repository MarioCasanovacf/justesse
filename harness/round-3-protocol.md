# Round 3 protocol — the first round with a real declarant

Round 2 answered whether the mechanism works. It could not answer whether it works *for someone*,
because its profile was fictional and its blind was procedural: the same party built the candidate
and scored it. Round 3 exists to close exactly those two gaps, and nothing else. Do not widen it.

Round 3 is blocked until a person who is not the harness author declares a profile. That is the
only blocking dependency, and it cannot be simulated: a declaration invented by the builder
reproduces round 2's limitation under a new name.

## Roles

Three roles, and no person holds two of them.

| Role | Does | Must not |
| --- | --- | --- |
| **Declarant** | Answers the ten fields, including `posture.closing`. Owns the identity. | See any candidate before scoring is complete. |
| **Builder** | Produces the four surfaces from the declaration and the frozen fixture. | Score. Choose the fixture. Ask the declarant leading questions. |
| **Scorer** | Applies `rubric.md` dimension by dimension against written criteria. | Have built either specimen. Know which specimen is which. |

If only two people are available, the declarant may score, because the declarant is the one party
whose judgment the rubric actually wants; the builder may never score. If only the builder is
available, there is no round 3 — record that and stop rather than running a third procedural blind.

## Procedure

1. **Declare.** The declarant fills the form in `skill/justesse/references/profile-declaration.md`
   without seeing any specimen, prior deck, or example beyond the form's own worked examples. Run
   `python3 harness/validate_profile.py <declaration>.json`. Every rejection goes back to the
   declarant verbatim; the builder does not answer a field on their behalf, and does not soften a
   rejection into a suggestion. A field the declarant will not answer is the finding, not an
   obstacle.
2. **Freeze inputs.** Record the declaration sha256, the skill commit, and the fixture sha256 in a
   provenance file before building anything.
3. **Build.** The builder produces the four contract surfaces under `personal:<name>` plus the
   no-flag control, using only `harness/fixture.json` for fact. Bounded verification applies: one
   batched inspection round, one batched fix, one confirming round, stop.
4. **Measure before judging.** Run `tools/check_layout.mjs` on the deck, `tools/inspect_pptx.py` and
   `tools/inspect_html.mjs` for inventories, and `tools/diff_specimens.py --expect-distinct` for the
   anti-convergence gate against both the control and the round 2 candidate. A round that fails a
   deterministic check does not proceed to scoring; it is fixed and re-measured first, because a
   scorer's attention is the scarce resource and should not be spent on what a tool already knows.
5. **Label blind.** A third party relabels the specimens so the scorer cannot tell candidate from
   baseline. Record the mapping outside the scorer's reach.
6. **Score.** The scorer applies `harness/rubric.md` and records per-dimension reasoning, not only
   totals. The reasoning is the audit trail; a bare number cannot be checked later.
7. **Human gate.** The declarant answers one question about each surface: *would you publish this
   as your own?* Not "is it good". A yes with reservations is a no with the reservation named — the
   reservation is the finding, and round 2 produced four rules that way.
8. **Record.** Append to `harness/calibration-log.md`: hashes, commands, scores, the human gate
   answer, and — required, not optional — the limitations that remain. A round that reports no
   limitations has not looked hard enough.

## What round 3 is testing

- **Does a stranger's declaration produce a design that is recognizably theirs?** The declarant is
  the only person who can answer that, and the answer is not a score.
- **Does the gate hold against a real person's vagueness?** Round 2's declarant was the harness
  author, who knew what the gate wanted. Real deferrals are the point of the field, and every one
  the gate lets through is a defect in the gate.
- **Do two real declarations diverge?** The anti-convergence gate has only ever run against one
  real identity and one control. Two declarants make it a real test: same fixture, same builder,
  same tools, measurably different surfaces, or the mechanism is decoration.

## What would falsify the mechanism

State this before running, so the result cannot be reinterpreted afterward:

- The declarant does not recognize the work as theirs, though the gate passed 10/10.
- Two independent declarations produce surfaces `diff_specimens.py --expect-distinct` cannot
  separate.
- The declarant cannot answer a required field concretely, and the field turns out not to matter to
  the design — which would mean the form is asking for ceremony.

Any of these is a finding worth more than a passing round. Record it in the log with the same weight
a pass would get.
