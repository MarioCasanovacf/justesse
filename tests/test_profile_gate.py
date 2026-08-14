"""Tests for the profile declaration gate.

Activating `personal:<name>` opens a ten-field declaration. These tests hold the gate to its one
job: a declaration passes only when every field is answered concretely, and the plausible ways of
not answering — placeholders, deferrals, moods where a measurement was asked for — are refused
rather than accepted and quietly improvised over.

The complete declaration below is deliberately fictional and lives only in this file. Nothing in
this repository ships a profile a design run could inherit.
"""

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))

import validate_profile  # noqa: E402


COMPLETE = {
    "identity": {
        "name": "atlas",
        "owner": "Atlas Research Cooperative",
        "scope": ["quarterly research notes", "internal decision memos"],
        "purpose": "Present bounded quantitative research without implying commercial claims.",
    },
    "canvas": {"surface": "#FFFDF7", "ink": "#121212", "dark_variant": None},
    "type_roles": {
        "display": {"family": "Source Serif 4", "fallback": "Georgia, serif", "availability": "installed"},
        "prose": {"family": "Source Serif 4", "fallback": "Georgia, serif", "availability": "installed"},
        "ui": {"family": "Source Sans 3", "fallback": "system-ui, sans-serif", "availability": "installed"},
        "data": {"family": "Source Code Pro", "fallback": "ui-monospace, monospace", "availability": "licensed"},
    },
    "semantic_color": {
        "positive": {"hex": "#1F5F3F", "redundancy": ["direct label", "upward marker"]},
        "warning": {"hex": "#8A5A12", "redundancy": ["direct label", "hatched fill"]},
        "negative": {"hex": "#7A1C1C", "redundancy": ["direct label", "downward marker"]},
        "neutral": {"hex": "#5F5F5F", "redundancy": ["direct label", "dashed line style"]},
        "structure": {"hex": "#121212", "redundancy": ["axis or baseline", "direct total label"]},
    },
    "action_treatment": "A single ink-outlined button with an underlined label, never a status fill.",
    "geometry": {
        "corner_radius_px": 0,
        "hairline_px": 1,
        "emphasis_rule_px": 3,
        "spacing_base_px": 8,
        "elevation": "No shadow at any level; separation comes from rules and spacing.",
    },
    "voice": {
        "person": "first person singular for authored statements",
        "heading_case": "sentence case",
        "register": ["precise", "restrained", "impersonal"],
        "refuses": ["exclamation marks", "superlatives", "brand-we"],
    },
    "exclusions": [
        "gradients",
        "glow and glass effects",
        "automatic dark mode",
        "spring and bounce motion",
        "stock photography of people",
    ],
    "posture": {"density": "balanced, one evidence module per fold", "motion": "none beyond focus states"},
    "evidence": {
        "unit": "stated on every axis and every displayed total",
        "period": "ISO week range, unbroken",
        "source": "named dataset and capture date in the caption",
        "uncertainty": "interval bands on every estimated series",
    },
}


def without(path):
    """A copy of COMPLETE with one dotted path removed."""
    declaration = copy.deepcopy(COMPLETE)
    parts = path.split(".")
    target = declaration
    for part in parts[:-1]:
        target = target[part]
    del target[parts[-1]]
    return declaration


def replacing(path, value):
    """A copy of COMPLETE with one dotted path replaced."""
    declaration = copy.deepcopy(COMPLETE)
    parts = path.split(".")
    target = declaration
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = value
    return declaration


class CompleteDeclarationTests(unittest.TestCase):
    def test_a_fully_answered_declaration_passes(self):
        self.assertEqual(validate_profile.validate(COMPLETE), [])

    def test_the_gate_covers_exactly_the_ten_documented_fields(self):
        reference = (ROOT / "skill" / "justesse" / "references" / "profile-declaration.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Ten fields are required", reference)
        self.assertEqual(len(validate_profile.REQUIRED_FIELDS), 10)
        self.assertEqual(set(validate_profile.REQUIRED_FIELDS), set(COMPLETE))

    def test_a_dark_variant_is_accepted_when_declared_concretely(self):
        declaration = replacing("canvas.dark_variant", {"surface": "#101010", "ink": "#F2F2F2"})
        self.assertEqual(validate_profile.validate(declaration), [])


class MissingFieldTests(unittest.TestCase):
    def test_every_top_level_field_is_required(self):
        for field in validate_profile.REQUIRED_FIELDS:
            with self.subTest(field=field):
                problems = validate_profile.validate(without(field))
                self.assertTrue(any(problem.startswith(field) for problem in problems))

    def test_every_type_role_is_required(self):
        for role in ("display", "prose", "ui", "data"):
            with self.subTest(role=role):
                problems = validate_profile.validate(without(f"type_roles.{role}"))
                self.assertIn(f"type_roles.{role}: required role is undeclared", problems)

    def test_every_semantic_role_is_required(self):
        for role in ("positive", "warning", "negative", "neutral", "structure"):
            with self.subTest(role=role):
                problems = validate_profile.validate(without(f"semantic_color.{role}"))
                self.assertIn(f"semantic_color.{role}: required role is undeclared", problems)

    def test_the_dark_variant_answer_cannot_simply_be_omitted(self):
        problems = validate_profile.validate(without("canvas.dark_variant"))
        self.assertTrue(any(problem.startswith("canvas.dark_variant") for problem in problems))


class NonAnswerTests(unittest.TestCase):
    def assertRefused(self, declaration, field):
        problems = validate_profile.validate(declaration)
        self.assertTrue(
            any(problem.startswith(field) for problem in problems),
            msg=f"expected {field} to be refused; got {problems}",
        )

    def test_placeholders_are_refused(self):
        for placeholder in ("TBD", "n/a", "", "  ", "placeholder", "todo", "-"):
            with self.subTest(placeholder=placeholder):
                self.assertRefused(replacing("identity.owner", placeholder), "identity.owner")

    def test_deferrals_are_refused(self):
        for deferral in (
            "you decide",
            "up to you",
            "use your judgment",
            "whatever fits",
            "honestly, you decide what looks right",
        ):
            with self.subTest(deferral=deferral):
                self.assertRefused(replacing("posture.density", deferral), "posture.density")

    def test_borrowed_values_are_refused(self):
        for borrowed in ("same as before", "same as the last deck", "like the other profile"):
            with self.subTest(borrowed=borrowed):
                self.assertRefused(replacing("action_treatment", borrowed), "action_treatment")

    def test_a_color_family_instead_of_a_hex_value_is_refused(self):
        for value in ("dark green", "forest", "#GGGGGG", "rgb(31,95,63)", "#1F5"):
            with self.subTest(value=value):
                self.assertRefused(
                    replacing("semantic_color.positive.hex", value), "semantic_color.positive.hex"
                )

    def test_a_mood_where_a_measurement_was_asked_for_is_refused(self):
        for value in ("tight", "8", "8px", None, 8.5, -8):
            with self.subTest(value=value):
                self.assertRefused(
                    replacing("geometry.spacing_base_px", value), "geometry.spacing_base_px"
                )

    def test_a_semantic_value_without_redundancy_is_refused(self):
        self.assertRefused(
            replacing("semantic_color.negative.redundancy", []), "semantic_color.negative.redundancy"
        )

    def test_fewer_than_five_exclusions_is_refused(self):
        self.assertRefused(replacing("exclusions", ["gradients", "glow", "glass", "bounce"]), "exclusions")

    def test_a_register_that_is_not_three_adjectives_is_refused(self):
        self.assertRefused(replacing("voice.register", ["precise", "restrained"]), "voice.register")

    def test_an_unrecognized_font_availability_is_refused(self):
        self.assertRefused(
            replacing("type_roles.ui.availability", "probably installed"),
            "type_roles.ui.availability",
        )

    def test_a_non_object_declaration_is_refused(self):
        for value in ([], "atlas", 3, None):
            with self.subTest(value=value):
                self.assertTrue(validate_profile.validate(value))


if __name__ == "__main__":
    unittest.main()
