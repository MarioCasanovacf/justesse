import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "justesse"
SKILL = ROOT / "skill" / SKILL_NAME
REFERENCE_NAMES = {
    "brief-and-direction.md",
    "data-visualization.md",
    "interface-quality.md",
    "marketing-surfaces.md",
    "product-and-transaction.md",
    "redesign-preservation.md",
    "reference-to-code.md",
    "image-concepts.md",
    "style-lenses.md",
    "motion-patterns.md",
    "react-next-tailwind.md",
    "production-preflight.md",
    "reading-surfaces.md",
    "upstream-provenance.md",
    "profile-activation.md",
    "profile-declaration.md",
    "profile-data-semantics.md",
    "profile-calibration.md",
    "surface-translation.md",
    "decision-memo.md",
    "pptx-safe-html.md",
}
EXPECTED_FILES = {
    "SKILL.md",
    "LICENSE.upstream",
    "LICENSE.upstream-impeccable",
    *(f"references/{name}" for name in REFERENCE_NAMES),
}
UPSTREAM_URL = "https://github.com/Leonxlnx/taste-skill"
UPSTREAM_COMMIT = "b17742737e796305d829b3ad39eda3add0d79060"
IMPECCABLE_URL = "https://github.com/pbakaus/impeccable"
IMPECCABLE_COMMIT = "c8f476b330395031bc8f7a7aee8d848bc85c81e4"
UPSTREAM_LICENSE = """MIT License

Copyright (c) 2026 Leonxlnx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def split_frontmatter(text: str):
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise AssertionError("SKILL.md must start with YAML frontmatter")
    metadata = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if not separator or not key.strip() or not value.strip():
            raise AssertionError(f"invalid frontmatter YAML line: {line!r}")
        metadata[key.strip()] = value.strip()
    return metadata, text[match.end() :]


def normalized(path: Path):
    return " ".join(path.read_text(encoding="utf-8").split())


class JustesseTests(unittest.TestCase):
    def test_skill_structure_has_only_intentional_files(self):
        actual = {
            path.relative_to(SKILL).as_posix()
            for path in SKILL.rglob("*")
            if path.is_file()
        }
        self.assertEqual(actual, EXPECTED_FILES)
        self.assertFalse((SKILL / "scripts").exists())
        self.assertFalse((SKILL / "assets").exists())

    def test_frontmatter_is_valid_yaml_with_exact_keys(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        metadata, body = split_frontmatter(text)
        self.assertEqual(set(metadata), {"name", "description"})
        self.assertEqual(metadata["name"], SKILL_NAME)
        self.assertIsInstance(metadata["description"], str)
        self.assertIn("production-ready web interfaces", metadata["description"])
        self.assertIn("mobile image concepts", metadata["description"])
        self.assertIn("# Justesse", body)
        self.assertLess(len(text.splitlines()), 250)

    def test_one_canonical_skill_tree_exists(self):
        self.assertTrue(SKILL.is_dir())
        self.assertFalse((ROOT / ".agents").exists())
        self.assertFalse((ROOT / ".claude").exists())
        self.assertFalse((ROOT / ".gemini").exists())

    def test_core_has_no_vendor_or_runtime_dependency(self):
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(SKILL.rglob("*"))
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".json"}
        ).casefold()
        for vendor in (
            "openai",
            "anthropic",
            "chatgpt",
            "claude",
            "codex",
            "gemini",
            "agents/openai.yaml",
        ):
            with self.subTest(vendor=vendor):
                self.assertNotIn(vendor, corpus)
        skill = normalized(SKILL / "SKILL.md")
        for phrase in (
            "independent of the model, agent runtime, command-line tool, vendor",
            "Runtime-specific discovery",
            "must not change the skill's semantics",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)

    def test_router_links_every_reference_directly_and_only_once_per_target(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        linked = set(re.findall(r"\]\(references/([a-z0-9-]+\.md)\)", text))
        self.assertEqual(linked, REFERENCE_NAMES)
        self.assertEqual(
            {path.name for path in (SKILL / "references").glob("*.md")},
            REFERENCE_NAMES,
        )
        self.assertFalse(
            [path for path in (SKILL / "references").rglob("*") if path.is_dir()]
        )

    def test_mode_lock_covers_all_supported_work(self):
        skill = normalized(SKILL / "SKILL.md")
        for phrase in (
            "Lock the operating mode",
            "Marketing / conversion",
            "Product / task",
            "Transactional flow",
            "Redesign: preserve",
            "Redesign: overhaul",
            "Reference to code",
            "Visual review",
            "Reading / documentation",
            "Image concept",
            "do not silently switch modes",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)

    def test_core_is_stack_neutral_and_preserves_product_contracts(self):
        skill = normalized(SKILL / "SKILL.md")
        for phrase in (
            "existing framework, package manager",
            "design system",
            "data and API contracts",
            "state semantics",
            "routes, forms, analytics",
            "consent and legal behavior",
            "accessibility, SEO",
            "Overhaul mode is not permission to break them",
            "Reuse installed dependencies",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill)

    def test_dashboards_and_multistep_transactions_are_first_class(self):
        skill = normalized(SKILL / "SKILL.md")
        product = normalized(
            SKILL / "references" / "product-and-transaction.md"
        )
        self.assertIn("including dashboards", skill)
        self.assertIn("multi-step flows", skill)
        for phrase in (
            "overview, exceptions, detail, and actions",
            "units, time range, freshness",
            "step sequence, branching, validation, side effects, persistence",
            "idempotency",
            "destructive actions",
            "resumed-session states",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, product)

    def test_motion_and_image_tools_are_conditional(self):
        skill = normalized(SKILL / "SKILL.md")
        images = normalized(SKILL / "references" / "image-concepts.md")
        self.assertIn(
            "Use image generation, image search, or browsing only when available, "
            "authorized, and necessary",
            skill,
        )
        self.assertIn("Motion libraries are conditional", skill)
        self.assertIn("Image tooling is optional", images)
        self.assertIn("clearly labeled placeholder", images)

    def test_profile_is_explicit_conditional_and_semantic(self):
        skill = normalized(SKILL / "SKILL.md")
        activation = normalized(SKILL / "references" / "profile-activation.md")
        semantics = normalized(SKILL / "references" / "profile-data-semantics.md")
        self.assertIn("exact `personal:<name>` flag", skill)
        self.assertIn("stays brand-neutral", skill)
        self.assertIn("light paper canvas is not a default", skill)
        self.assertIn("Do not activate from a person's name", activation)
        for phrase in (
            "Declared positive value",
            "Declared warning value",
            "Declared negative value",
            "Declared neutral value",
            "Declared structure value",
            "It supplies no values of its own",
            "Prevent CTA/status collision",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, semantics)

    def test_repository_ships_the_mechanism_and_no_profile(self):
        """No named individual's design system may ship inside the skill tree.

        The declaration form is exempt: it carries worked examples, which is what makes a
        field answerable at all. It pays for the exemption by refusing copies of them.
        """
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(SKILL.rglob("*.md"))
            if path.name != "profile-declaration.md"
        )
        self.assertNotRegex(corpus, r"#[0-9A-Fa-f]{6}")
        self.assertNotRegex(
            corpus.casefold(),
            r"\b(didot|garamond|baskerville|helvetica|futura|inter|roboto)\b",
        )
        self.assertIn(
            "ships the profile mechanism and no profile",
            normalized(SKILL / "SKILL.md"),
        )

    def test_the_form_asks_with_a_worked_example_for_every_field(self):
        """A bare question returns a mood where the form needs a measurement."""
        declaration = normalized(SKILL / "references" / "profile-declaration.md")
        self.assertIn("Always ask with an example attached", declaration)
        self.assertIn("| Example |", declaration)
        for example in ("e.g. `atlas`", "e.g. `#FFFDF7`", "e.g. `1`"):
            with self.subTest(example=example):
                self.assertIn(example, declaration)
        for counterexample in ('Not "off-white"', 'Not "thin"'):
            with self.subTest(counterexample=counterexample):
                self.assertIn(counterexample, declaration)
        self.assertIn("It does not propose the answer", declaration)
        self.assertIn("Copying an example is itself a non-answer", declaration)
        # Ten field rows, each with an example cell of its own.
        rows = [
            line
            for line in (SKILL / "references" / "profile-declaration.md")
            .read_text(encoding="utf-8")
            .splitlines()
            if re.match(r"\A\| \d+ \|", line)
        ]
        self.assertEqual(len(rows), 10)
        for row in rows:
            with self.subTest(row=row.split("|")[2].strip()):
                self.assertEqual(row.count("|"), 5)
                self.assertTrue(row.rsplit("|", 2)[1].strip())

    def test_activation_opens_a_declaration_it_cannot_answer_itself(self):
        skill = normalized(SKILL / "SKILL.md")
        activation = normalized(SKILL / "references" / "profile-activation.md")
        declaration = normalized(SKILL / "references" / "profile-declaration.md")
        self.assertIn("An active flag opens a required declaration", skill)
        self.assertIn("before making any design decision under the profile", skill)
        self.assertIn("is a blocked task", activation)
        self.assertIn("An unanswered field is unanswered", activation)
        self.assertIn("Ten fields are required", declaration)
        for field in (
            "Identity",
            "Canvas",
            "Type roles",
            "Semantic color",
            "Action treatment",
            "Geometry",
            "Voice",
            "Exclusions",
            "Posture",
            "Evidence",
        ):
            with self.subTest(field=field):
                self.assertIn(f"| {field} |", declaration)
        for rejection in (
            "Reject non-answers",
            "A borrowed value",
            "An underdetermined value",
            "Re-ask only for the fields that failed",
        ):
            with self.subTest(rejection=rejection):
                self.assertIn(rejection, declaration)

    def test_presentation_authoring_contract_is_specific(self):
        deck = normalized(SKILL / "references" / "pptx-safe-html.md")
        memo = normalized(SKILL / "references" / "decision-memo.md")
        self.assertIn("1280 × 720 px canvas", deck)
        self.assertIn("13.333 × 7.5 in", deck)
        for kind in ("text", "rect", "ellipse", "line"):
            with self.subTest(kind=kind):
                self.assertIn(f"| `{kind}` |", deck)
        for rejected in (
            "flexbox",
            "media queries",
            "box-shadow",
            "backdrop-filter",
            "::before",
            "clip-path",
        ):
            with self.subTest(rejected=rejected):
                self.assertIn(rejected, deck)
        self.assertIn("An image is the one element that is never manipulable", deck)
        self.assertIn("Verify against the file, not against the HTML that produced it", deck)
        self.assertIn("is a picture of a memo", memo)
        self.assertIn("pptx-safe-html.md", memo)

    def test_data_visualization_uses_geometry_and_semantic_color(self):
        skill = normalized(SKILL / "SKILL.md")
        data = normalized(SKILL / "references" / "data-visualization.md")
        semantics = normalized(SKILL / "references" / "profile-data-semantics.md")
        surface = normalized(SKILL / "references" / "surface-translation.md")
        self.assertIn("Data visualization", skill)
        for phrase in (
            "A graph is evidence, not texture",
            "Anchor every numeric label to the mark or segment it describes",
            "Use at most one grey data encoding",
            "font-variant-numeric: tabular-nums lining-nums",
            "do not manually nudge individual digits",
            "Keep each ISO date token unbroken",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, data)
        for phrase in (
            "Use semantic chart recipes",
            "never accompany it with a lighter, darker, or translucent grey data series",
            "Never place unequal segment values in equal-width label columns",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, semantics)
        self.assertIn("Align every displayed number to a common grid or baseline", surface)

    def test_mobile_multiframe_image_contract_is_explicit(self):
        images = normalized(SKILL / "references" / "image-concepts.md")
        for phrase in (
            "platform conventions, safe areas and system regions",
            "navigation model, keyboard behavior, typography, spacing, radii, and icon",
            "Map the logical flow",
            "design bible across every screen",
            "raw screens or device mockups",
            "never force a phone frame",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, images)

    def test_deliverable_completeness_and_placeholder_contract(self):
        skill = normalized(SKILL / "SKILL.md")
        preflight = normalized(
            SKILL / "references" / "production-preflight.md"
        )
        self.assertIn("Enumerate every requested deliverable", skill)
        self.assertIn("cross-check every requested deliverable", skill)
        self.assertIn("truly missing external assets or dependencies", skill)
        self.assertIn("dimensions, role, and replacement next step", preflight)

    def test_no_brittle_upstream_recipe_is_mandated(self):
        corpus = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(SKILL.rglob("*.md"))
        )
        forbidden = (
            "must use React",
            "must use Tailwind",
            "must use GSAP",
            "always use dark mode",
            "never use an em dash",
            "never use an en dash",
            "Math.random",
            "one image in every section",
            "one image per section is required",
        )
        for phrase in forbidden:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase.casefold(), corpus.casefold())

    def test_upstream_provenance_and_full_license_are_pinned(self):
        provenance = (
            SKILL / "references" / "upstream-provenance.md"
        ).read_text(encoding="utf-8")
        self.assertIn(UPSTREAM_URL, provenance)
        self.assertIn(UPSTREAM_COMMIT, provenance)
        self.assertIn("License: MIT", provenance)
        self.assertEqual(
            (SKILL / "LICENSE.upstream").read_text(encoding="utf-8"),
            UPSTREAM_LICENSE,
        )
        self.assertIn(IMPECCABLE_URL, provenance)
        self.assertIn(IMPECCABLE_COMMIT, provenance)
        self.assertIn("License: Apache-2.0", provenance)
        apache = (SKILL / "LICENSE.upstream-impeccable").read_text(encoding="utf-8")
        self.assertIn("Apache License", apache)
        self.assertIn("Version 2.0, January 2004", apache)
        self.assertIn("Copyright 2025 Paul Bakaus", apache)

    def test_absorbed_craft_rules_are_present_and_scoped(self):
        """Tranche 1 of the impeccable absorption: distilled rules, original prose.

        Deterministic assertions here; blind A/B promotion per profile-calibration.md
        remains a separate specimen-producing run.
        """
        skill = normalized(SKILL / "SKILL.md")
        quality = normalized(SKILL / "references" / "interface-quality.md")
        reading = normalized(SKILL / "references" / "reading-surfaces.md")
        # Bounded verification: batched rounds with a hard stop, not an open QA loop.
        self.assertIn("Render and verify in bounded passes", skill)
        self.assertIn("confirm with at most one more round", skill)
        self.assertIn("spends the budget without converging", skill)
        # Built-result checks, including the browser surfaces nobody draws.
        self.assertIn("Verify on the render", quality)
        self.assertIn("a check on the built result, not an intention", quality)
        self.assertIn("The surfaces you did not draw still carry the design", quality)
        # Unearned defaults stay defaults, never bans: the brief can earn them back.
        self.assertIn("Unearned defaults", quality)
        self.assertIn("not bans: the brief's own words can earn any of them", quality)
        self.assertIn("ghost card", quality)
        # Reading mode: comprehension first, chosen per surface.
        self.assertIn("Structure for comprehension first", reading)
        self.assertIn("Assume arrival mid-page", reading)
        self.assertIn("not from the product", reading)


if __name__ == "__main__":
    unittest.main()
