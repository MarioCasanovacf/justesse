#!/usr/bin/env python3
"""Deterministic static checks for the conditional profile mechanism and the presentation path.

The skill ships the profile mechanism and no profile. These checks assert that the mechanism stays
generic, that activation cannot resolve to a bundled identity, and that the presentation-file
authoring contract is present and specific.
"""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "justesse"
CONTRACT = json.loads((Path(__file__).parent / "contract.json").read_text(encoding="utf-8"))
skill_text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
references = SKILL / "references"
required = {
    "profile-activation.md",
    "profile-declaration.md",
    "profile-data-semantics.md",
    "surface-translation.md",
    "decision-memo.md",
    "profile-calibration.md",
    "pptx-safe-html.md",
}
texts = {
    name: " ".join((references / name).read_text(encoding="utf-8").split())
    for name in required
}
checks: list[tuple[str, bool]] = []


def check(name: str, condition: bool) -> None:
    checks.append((name, bool(condition)))


linked = set(re.findall(r"\]\(references/([a-z0-9-]+\.md)\)", skill_text))
check("all seven mechanism references exist", all((references / name).is_file() for name in required))
check("all seven references directly linked", required <= linked)
check("profile flag in description", "personal:<name>" in skill_text.split("---", 2)[1])
check("exact flag routing", "exact `personal:<name>` flag" in skill_text)
check("profile separate from mode", "set the profile separately" in skill_text)
check("no implicit activation", "Never infer it" in skill_text)
check("generic brand neutrality", "keep the visual language" in skill_text and "brand-neutral" in skill_text)
check("generic light paper prohibited", "light paper canvas is not a default" in skill_text)
check("ships no bundled profile", "ships the profile\nmechanism and no profile" in skill_text or "ships the profile mechanism and no profile" in " ".join(skill_text.split()))
check("declaration gates design work", "before\nmaking any design decision" in skill_text or "before making any design decision" in " ".join(skill_text.split()))

# No personal payload may ship inside the skill tree. The declaration form is the one file allowed
# to carry literals, because a worked example is what makes a field answerable; everywhere else a
# literal is a bundled value a run could inherit. The form pays for that exemption by stating that
# copying an example is itself a non-answer.
FORM = "profile-declaration.md"
corpus = "\n".join(
    path.read_text(encoding="utf-8")
    for path in sorted(SKILL.rglob("*.md"))
    if path.name != FORM
).casefold()
check("every reference file is linked from the router", {path.name for path in references.glob("*.md")} == linked)
check("no reference outside the form ships a color value", not re.search(r"#[0-9a-f]{6}", corpus))
check("no reference outside the form ships a named type stack", not re.search(
    r"\b(didot|garamond|baskerville|helvetica|futura|inter|roboto)\b", corpus
))

activation = texts["profile-activation.md"]
check("activation scope", "personal:<name>" in activation and "never bundled with this skill" in activation)
check("no inference from a name", "Do not activate from a person's name" in activation)
check("declaration precedes application", "Declaration precedes application" in activation)
check("incomplete declaration blocks", "is a blocked task" in activation)
check("no borrowed values", "carrying a value from another profile" in activation)
check("profile conflict handling", "preserve the contract" in activation)

declaration = texts["profile-declaration.md"]
check("ten required fields", "Ten fields are required" in declaration)
for field in (
    "Identity", "Canvas", "Type roles", "Semantic color", "Action treatment",
    "Geometry", "Voice", "Exclusions", "Posture", "Evidence",
):
    check(f"declaration field {field.casefold()}", f"| {field} |" in declaration)
# Every field must be askable: a bare question gets a mood back where the form needs a measurement.
check("never ask a field bare", "Always ask with an example attached" in declaration)
check("form carries an example column", "| Example |" in declaration)
check("example fixes shape not answer", "It does not propose the answer" in declaration)
check("copying an example is refused", "Copying an example is itself a non-answer" in declaration)
check("example column flagged as a failure source", "the most likely source of this failure" in declaration)
check("worked examples are concrete", all(
    token in declaration for token in ("e.g. `atlas`", "e.g. `#FFFDF7`", 'Not "off-white"', 'Not "thin"')
))
check("every field carries a worked example", declaration.count("|") >= 10 * 5)
check("rejects non-answers", "Reject non-answers" in declaration)
check("rejects deferral", '"you decide"' in declaration)
check("rejects borrowed values", "A borrowed value" in declaration)
check("rejects underdetermined values", "a color family instead of a hex value" in declaration)
check("re-asks only failed fields", "Re-ask only for the fields that failed" in declaration)
check("applies structurally", "has not been applied" in declaration)

semantics = texts["profile-data-semantics.md"]
check("supplies no values of its own", "It supplies no values of its own" in semantics)
for role in ("positive", "warning", "negative", "neutral", "structure"):
    check(f"semantic role {role} sourced from declaration", f"Declared {role} value" in semantics)
check("direct labels required", "Direct label" in semantics)
check("non-color redundancy required", "Never ask hue to carry status alone" in semantics)
check("grayscale verification", "grayscale" in semantics)
check("CTA status collision", "Prevent CTA/status collision" in semantics)
check("action treatment resolves collision", "declared action treatment from field 5" in semantics)
check("semantic chart recipes", "Use semantic chart recipes" in semantics)
check("single visible grey", "never accompany it with a lighter, darker, or translucent grey data series" in semantics)
check("segment labels follow geometry", "Never place unequal segment values in equal-width label columns" in semantics)

surface = texts["surface-translation.md"]
check("dashboard translation", "within five seconds" in surface and "next action" in surface)
check("landing translation", "the author's authorship" in surface and "not as a fictional SaaS product" in surface)
check("report translation", all(word in surface for word in ("question", "data", "method", "findings", "limits", "decision")))
check("deck translation", "shrinking a dashboard into slides" in surface)
check("landing number alignment", "Align every displayed number to a common grid or baseline" in surface)

data = " ".join((references / "data-visualization.md").read_text(encoding="utf-8").split())
check("chart selection precedes styling", "Make the analytical question visible before styling the chart" in data)
check("single grey data encoding", "Use at most one grey data encoding" in data)
check("tabular lining numerals", "font-variant-numeric: tabular-nums lining-nums" in data)
check("no manual digit nudging", "do not manually nudge individual digits" in data)
check("unbroken ISO periods", "Keep each ISO date token unbroken" in data)

memo = texts["decision-memo.md"]
for index, stage in enumerate(("Situation", "Evidence", "Implication", "Decision", "Risk and next step"), 1):
    check(f"memo stage {index}", f"{index}. {stage}" in memo)
check("one claim per slide", "one defensible claim per slide" in memo)
check("one chromatic emphasis", "at most one primary chromatic emphasis" in memo)
check("no miniature dashboard", "not a miniature dashboard" in memo)
check("editable presentation section", "When the deliverable is an editable presentation file" in memo)
check("picture of a memo", "is a picture of a memo" in memo)
check("memo routes to authoring contract", "pptx-safe-html.md" in memo)

deck = texts["pptx-safe-html.md"]
memo_brief = CONTRACT["surface_briefs"]["decision_memo"]
canvas = memo_brief["canvas_pixels"]
check("canvas matches contract", f"{canvas['width']} × {canvas['height']} px" in deck)
check("canvas maps to slide inches", f"{memo_brief['slide_size']['width_inches']} × {memo_brief['slide_size']['height_inches']} in" in deck)
check("absolute px boxes only", "four absolute inline values" in deck)
for kind in ("text", "rect", "ellipse", "line"):
    check(f"authoring class {kind}", f"| `{kind}` |" in deck)
check("objects carry data-name", "data-name" in deck)
check("charts are native objects", "Chart marks are rectangles and lines" in deck)
check("runtime layout rejected", all(token in deck for token in ("flexbox", "grid", "media queries", "calc()")))
check("effects rejected", all(token in deck for token in ("box-shadow", "backdrop-filter", "clip-path", "mix-blend-mode")))
check("generated content rejected", all(token in deck for token in ("::before", "::after", "iframes")))
check("raster is the exception", "An image is the one element that is never manipulable" in deck)
check("silent flattening disclosed", "Disclose it; do not close the gap silently" in deck)
check("verify against the file", "Verify against the file, not against the HTML that produced it" in deck)
check("converter is not the contract", "not part of this skill's contract" in deck)

# Absorbed craft rules (impeccable tranche 1): deterministic presence checks. Promotion of these
# rules through the blind A/B remains a calibration run, not an assertion.
quality = " ".join((references / "interface-quality.md").read_text(encoding="utf-8").split())
reading = " ".join((references / "reading-surfaces.md").read_text(encoding="utf-8").split())
check("bounded verification in workflow", "Render and verify in bounded passes" in skill_text)
check("verification has a hard stop", "at most one more round" in " ".join(skill_text.split()))
check("built-result checks present", "Verify on the render" in quality)
check("browser surfaces themed", "The surfaces you did not draw still carry the design" in quality)
check("unearned defaults stay earnable", "the brief's own words can earn any of them" in quality)
check("reading mode linked", "reading-surfaces.md" in linked)
check("reading mode is comprehension-first", "Structure for comprehension first" in reading)
reference = " ".join((references / "reference-to-code.md").read_text(encoding="utf-8").split())
preflight = " ".join((references / "production-preflight.md").read_text(encoding="utf-8").split())
lenses = " ".join((references / "style-lenses.md").read_text(encoding="utf-8").split())
experience = " ".join((references / "experience-surfaces.md").read_text(encoding="utf-8").split())
check("fidelity inventory precedes building", "Write the fidelity inventory before building" in reference)
check("silent drops named", "silently drops" in reference)
check("extreme inputs are concrete", "not just the idea of them" in preflight)
check("amplification stays in vocabulary", "Amplifying within a lens" in lenses and "skeleton test" in lenses)
check("experience mode linked", "experience-surfaces.md" in linked)
check("experience mode recedes", "the interface recedes" in experience)
finishing = " ".join((references / "finishing.md").read_text(encoding="utf-8").split())
check("finishing linked and loaded last", "finishing.md" in linked and "Read [finishing.md](references/finishing.md) last" in skill_text)
check("finishing never a pardon", "never buys forgiveness" in finishing)
check("surface temperature is a decision", "Surface temperature is a decision" in finishing)
check("one watermark on the record", "The watermark principle" in finishing and "Name the move in the design read" in finishing)
check("emptiness is assigned, not left over", "Emptiness has to be assigned" in finishing and "equal distances so nothing groups" in finishing)
check("sparse surfaces are measured, not eyeballed", "measure each surface's top gap and bottom gap" in finishing)
check("an empty canvas asks for evidence before arrangement", "the fix is usually not a better arrangement of the space but the evidence that should have been on it" in finishing)
check("filling from evidence is not inventing content", "whether the values were already true before the layout needed them" in finishing)
check("comparison instrument named", "tools/diff_specimens.py" in finishing)
check("convergence is a failure", "convergence to one look, however refined, is a failure" in finishing)

calibration = texts["profile-calibration.md"]
check("three controlled variants", all(label in calibration for label in ("baseline A", "candidate B", "B-no-flag")))
check("identical frozen inputs", "Freeze one fixture" in calibration)
check("blind scoring", "blind specimen labels" in calibration)
check("provenance fields", all(field in calibration for field in ("skill path and hash", "profile flag", "render command", "QA command")))
check("declaration recorded in provenance", "the declaration record and its hash" in calibration)
check("no-flag negative control", "no-flag output remains brand-neutral" in calibration)
check("human gate retained", "the profile owner says they would publish" in calibration)
check("scored against the declaration", "never against the scorer's taste" in calibration)
check("no specimen leakage", "do not copy specimen-specific values into the skill" in calibration)

failed = [name for name, ok in checks if not ok]
if failed:
    for name in failed:
        print(f"FAIL: {name}")
    raise SystemExit(f"FAILED {len(checks) - len(failed)}/{len(checks)}")

print(f"PASS {len(checks)}/{len(checks)} named assertions")
