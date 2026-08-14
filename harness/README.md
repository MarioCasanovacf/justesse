# Calibration harness

This directory defines a runtime-independent experiment for evolving the skill.

1. Freeze one factual fixture and one surface contract.
2. Produce a baseline, a candidate, and a candidate without the personal flag.
3. Record the skill hash, profile flag, assumptions, render command, and QA command.
4. Replace variant names with blind specimen labels.
5. Score every hard gate and weighted dimension in `rubric.md`.
6. Reveal the variants only after scoring.
7. Promote reusable rules; never copy specimen-specific values into the skill.

The harness does not prescribe which model, agent, renderer, browser, slide library, or frontend
framework performs the work. Each runner must preserve the same frozen inputs and provide
replayable evidence appropriate to the artifact it produces.

Run the static profile contract:

```bash
python3 harness/validate_skill.py
```

Run the benchmark arithmetic validator, which checks that `contract.json` and `fixture.json` in
this directory are internally consistent (weekly rows sum to the recorded totals, driver counts
sum to the negative total, the eight frozen weeks match the declared period, and the semantic map,
hard gates, and rubric weights are structurally coherent):

```bash
python3 harness/validate_benchmark.py
```

Gate a profile declaration before designing against it. The repository ships the profile mechanism
and no profile, so a flagged run resolves its identity from the requester's declaration and from
nothing else. This refuses a declaration with any undeclared or non-concrete field, naming each one
so only those get re-asked:

```bash
python3 harness/validate_profile.py path/to/declaration.json
```

It enforces completeness and concreteness. It cannot detect a value borrowed from another profile
or from a published artifact; that stays a review gate, and `rubric.md` scores it.

<!-- Contributed 2026-08-12 from the operator's harness epic (T-318..T-329, killed as duplicate; PR-014). -->
