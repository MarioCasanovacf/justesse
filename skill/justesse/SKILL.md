---
name: justesse
description: Design, redesign, implement, or visually review distinctive production-ready web interfaces, executive decision memos, editable presentation files, and mobile image concepts while preserving product constraints and the existing stack. Use for marketing and conversion pages, product and dashboard UI, transactional or multi-step flows, preserve-mode or overhaul-mode redesigns, reference-to-code work, visual quality audits, and web or mobile image concept direction. Apply a named personal profile only when the exact personal:<name> flag is explicit and its declaration is complete; this skill ships no profile of its own and stays brand-neutral without one.
---

# Justesse

Turn a brief, repository, or visual reference into coherent production UI. Treat taste as contextual
judgment under constraints, not as a preferred framework, aesthetic, or component recipe.

This is a declarative, reference-only capability. Its design reasoning, rules, and acceptance
criteria must remain independent of the model, agent runtime, command-line tool, vendor, and
hosting environment that execute it. Runtime-specific discovery may expose this directory, but it
must not change the skill's semantics or be required by its workflow.

## Lock the operating mode

Choose one primary mode before making design decisions. State it in the design read and do not
silently switch modes. If two modes imply materially different deliverables and the request does
not resolve them, ask one focused question. A task may name a secondary mode, but the primary mode
controls the workflow and acceptance bar.

| Mode | Primary outcome | Required reference |
| --- | --- | --- |
| Marketing / conversion | Communicate value and move an audience toward one measurable action | [marketing-surfaces.md](references/marketing-surfaces.md) |
| Product / task | Help a user understand state and complete recurring work, including dashboards | [product-and-transaction.md](references/product-and-transaction.md) |
| Transactional flow | Complete a consequential or multi-step action safely and recoverably | [product-and-transaction.md](references/product-and-transaction.md) |
| Redesign: preserve | Improve quality while keeping recognizable brand and product contracts | [redesign-preservation.md](references/redesign-preservation.md) |
| Redesign: overhaul | Establish a new visual language while retaining unapproved-to-change contracts | [redesign-preservation.md](references/redesign-preservation.md) |
| Reference to code | Translate supplied visual evidence into the target project's native implementation | [reference-to-code.md](references/reference-to-code.md) |
| Visual review | Diagnose hierarchy, coherence, usability, responsiveness, and production risk | [interface-quality.md](references/interface-quality.md) |
| Reading / documentation | Help a reader understand something through docs, guides, articles, help, or changelogs | [reading-surfaces.md](references/reading-surfaces.md) |
| Experience / showcase | Put a visitor inside portfolio, gallery, or exhibition work while the interface recedes | [experience-surfaces.md](references/experience-surfaces.md) |
| Image concept | Define or produce art direction that serves the interface | [image-concepts.md](references/image-concepts.md) |
| Data visualization | Turn measures, comparisons, distributions, relationships, and uncertainty into inspectable evidence | [data-visualization.md](references/data-visualization.md) |
| Executive decision memo | Turn bounded evidence into a conclusion-led presentation for a decision-maker | [decision-memo.md](references/decision-memo.md) |

After selecting the primary mode, set the profile separately. This skill ships the profile
mechanism and no profile. Activate `personal:<name>` only when that exact flag is explicit in the
request or project instructions. Never infer it from a person's name, an artifact type, or this
skill's availability. Without the flag, keep the visual language, voice, palette, materiality, and
surface color brand-neutral; a light paper canvas is not a default.

An active flag opens a required declaration rather than granting a visual system. Obtain concrete
answers to all ten fields in [profile-declaration.md](references/profile-declaration.md) before
making any design decision under the profile, and never fill an unanswered field by inference or by
borrowing a value from another profile, from this skill's examples, or from its harness fixtures.
Ask every field with a worked example attached, in that field's own answer shape; a bare question
returns a mood where the form needs a measurement.

## Core workflow

1. **Inspect before proposing.** Read the relevant project files, representative screens and
   components, package and build configuration, design tokens, data shapes, routes, tests, and
   supplied references. Identify what is real, what is inferred, and what remains unknown.
2. **Frame the brief.** Read [brief-and-direction.md](references/brief-and-direction.md). Record the
   audience, user job, business goal, content and brand evidence, constraints, primary mode, and
   success signal. Enumerate every requested deliverable before implementation. Prefer one
   defensible interpretation over a collage of trends.
3. **Declare the design read.** In one compact statement, name the mode, audience, product job,
   visual direction, density, and motion posture. Distinguish decisions from assumptions.
4. **Preserve the product contract.** Keep the existing framework, package manager, component
   conventions, design system, data and API contracts, state semantics, routes, forms, analytics,
   consent and legal behavior, accessibility, SEO, content meaning, tests, and performance budgets
   unless the user explicitly authorizes a change. Overhaul mode is not permission to break them.
5. **Implement natively.** Reuse installed dependencies and established primitives. Express the
   direction in the project's own framework and styling model. Do not introduce React, Tailwind,
   GSAP, another design system, dark mode, a font, or any dependency merely because this skill
   mentions a visual possibility.
6. **Resolve the whole state space.** Design responsive layout plus applicable loading, empty,
   partial, error, success, disabled, permission, offline, validation, and destructive-action
   states. For dashboards and flows, protect data legibility, task continuity, and recovery.
7. **Render and verify in bounded passes.** Build fully first. Then inspect representative narrow
   and wide viewports and real content extremes together in one batched round when preview tooling
   exists, comparing hierarchy, reading order, overflow, contrast, focus, interaction feedback,
   and contract preservation. Fix everything that round shows in one batch, confirm with at most
   one more round, and stop polishing: an open-ended self-QA loop spends the budget without
   converging, and the bound covers the whole cycle, screenshots, defect scans, micro-edits, and
   rebuilds alike. Do not call a mockup production-ready without proportionate build, test, and
   visual evidence.
8. **Preflight delivery.** Read [production-preflight.md](references/production-preflight.md), fix
   applicable failures, cross-check every requested deliverable, and report checks that could not
   run.

## Reference routing

Load only what the active mode needs; every reference is directly linked here.

- Always read [brief-and-direction.md](references/brief-and-direction.md),
  [interface-quality.md](references/interface-quality.md), and
  [production-preflight.md](references/production-preflight.md).
- Read [marketing-surfaces.md](references/marketing-surfaces.md) for marketing, campaign,
  editorial-conversion, pricing, launch, or other acquisition surfaces.
- Read [reading-surfaces.md](references/reading-surfaces.md) for documentation, guides, articles,
  help, changelogs, and long-form pages whose job is comprehension.
- Read [experience-surfaces.md](references/experience-surfaces.md) for portfolios, galleries,
  showcases, and exhibition pages where the work itself leads.
- Read [product-and-transaction.md](references/product-and-transaction.md) for application UI,
  dashboards, data-dense workspaces, forms, checkout, onboarding, settings, and multi-step flows.
- Read [data-visualization.md](references/data-visualization.md) whenever a surface contains a KPI,
  chart, analytical figure, metric comparison, table of numbers, or date/period display.
- Read [redesign-preservation.md](references/redesign-preservation.md) whenever an existing surface
  changes, in either preserve or overhaul mode.
- Read [reference-to-code.md](references/reference-to-code.md) when screenshots, mockups, websites,
  or other visual examples are implementation inputs.
- Read [image-concepts.md](references/image-concepts.md) only when imagery is part of the brief or
  image concept is the selected mode.
- Read [style-lenses.md](references/style-lenses.md) when the brief lacks a visual vocabulary or
  competing directions need to be separated.
- Read [react-next-tailwind.md](references/react-next-tailwind.md) only when the inspected project
  already uses React, Next.js, or Tailwind, or the user explicitly authorizes that stack for
  greenfield work; it is not the portable default.
  <!-- Contributed 2026-08-12 from the operator's harness epic (T-318..T-329, killed as duplicate; PR-014). -->
- Read [decision-memo.md](references/decision-memo.md) for an executive memo, decision deck, or any
  conclusion-led slide sequence.
- Read [pptx-safe-html.md](references/pptx-safe-html.md) before laying out the first slide whenever
  the deliverable is an editable presentation file rather than a page.
- Read [surface-translation.md](references/surface-translation.md) when one worldview must carry
  across a dashboard, authored landing page, case study, report, and presentation.
- With the exact `personal:<name>` flag, read
  [profile-activation.md](references/profile-activation.md) and
  [profile-declaration.md](references/profile-declaration.md) first, then
  [profile-data-semantics.md](references/profile-data-semantics.md) once the declaration is
  complete. Do not load or apply them otherwise.
- Read [profile-calibration.md](references/profile-calibration.md) only when running a controlled
  profile comparison, negative control, blind review, or promotion decision.
- Read [upstream-provenance.md](references/upstream-provenance.md) only for attribution, auditing,
  redistribution, or upstream comparison.

Do not recursively load unrelated files from references.

## Conditional capabilities

Use image generation, image search, or browsing only when available, authorized, and necessary.
For image work, prefer existing repository assets, then user-provided assets, then an authorized
tool. Otherwise deliver a specific concept brief or clearly labeled placeholder without claiming
it is final art. Use placeholders only for truly missing external assets or dependencies; specify
each placeholder's dimensions, role, and replacement next step. Do not fabricate product
screenshots, customers, metrics, logos, or endorsements.

Use motion only when it clarifies hierarchy, feedback, continuity, or narrative. Prefer the
project's existing mechanism and the lightest adequate technique. Preserve content without motion,
honor reduced-motion preferences, avoid scroll capture, and clean up observers, listeners, and
timelines. Motion libraries are conditional implementation choices, never a requirement. Escalate to
[motion-patterns.md](references/motion-patterns.md) only when a native CSS transition is no longer
adequate and the work needs layered choreography, scroll storytelling, or a dedicated animation
engine.
<!-- Contributed 2026-08-12 from the operator's harness epic (T-318..T-329, killed as duplicate; PR-014). -->

## Delivery contract

Deliver the implemented or reviewed surface together with the mode and design read, preserved and
intentionally changed contracts, verification evidence, and any placeholders or unresolved risks.
For a review-only request, prioritize findings by user impact and cite the affected screen or
component; do not mutate the project unless asked.
