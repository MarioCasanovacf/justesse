"""Tests for the declaration-level convergence check.

Convergence is cheaper to catch before anyone builds. These assert the two things that make the
check trustworthy: that it grades only what a declaration actually fixes, and that prose — voice,
posture, action treatment — never rescues a pair that agrees on every fixed value.
"""

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests"))

import diff_declarations  # noqa: E402

from test_profile_gate import COMPLETE  # noqa: E402


def verdict(a, b):
    _, distinct, total = diff_declarations.compare(a, b)
    return distinct, total


class ConvergenceTests(unittest.TestCase):
    def test_a_declaration_does_not_diverge_from_itself(self):
        distinct, total = verdict(COMPLETE, copy.deepcopy(COMPLETE))
        self.assertEqual(distinct, 0)
        self.assertEqual(total, 15)

    def test_prose_alone_never_makes_two_identities_distinct(self):
        """Different register, different closing, same design — still one identity."""
        other = copy.deepcopy(COMPLETE)
        other["identity"]["name"] = "twin"
        other["voice"]["register"] = ["playful", "loud", "warm"]
        other["posture"]["closing"] = "three or four bounded paths with my lean stated as a lean"
        other["action_treatment"] = "a solid filled bar with a reversed label, never an outline"
        distinct, _ = verdict(COMPLETE, other)
        self.assertEqual(distinct, 0)

    def test_a_sub_perceptual_recolor_does_not_count_as_divergence(self):
        """The failure this catches: nudging a hex and calling the result a second identity."""
        other = copy.deepcopy(COMPLETE)
        surface = other["canvas"]["surface"]
        other["canvas"]["surface"] = "#FFFDF8" if surface != "#FFFDF8" else "#FFFDF6"
        distinct, _ = verdict(COMPLETE, other)
        self.assertEqual(distinct, 0)

    def test_type_and_geometry_changes_do_count(self):
        other = copy.deepcopy(COMPLETE)
        other["type_roles"]["data"]["family"] = "Courier New"
        other["geometry"]["spacing_base_px"] = COMPLETE["geometry"]["spacing_base_px"] + 2
        distinct, _ = verdict(COMPLETE, other)
        self.assertEqual(distinct, 2)


class ExitCodeTests(unittest.TestCase):
    def run_main(self, a, b, *flags):
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for index, declaration in enumerate((a, b)):
                path = Path(tmp) / f"{index}.json"
                path.write_text(json.dumps(declaration), encoding="utf-8")
                paths.append(str(path))
            return diff_declarations.main(["diff", *paths, *flags])

    def test_expect_distinct_fails_on_a_twin(self):
        twin = copy.deepcopy(COMPLETE)
        twin["identity"]["name"] = "twin"
        self.assertEqual(self.run_main(COMPLETE, twin, "--expect-distinct"), 1)

    def test_expect_distinct_passes_on_a_real_divergence(self):
        other = copy.deepcopy(COMPLETE)
        other["identity"]["name"] = "other"
        other["canvas"]["ink"] = "#000000"
        other["semantic_color"]["positive"]["hex"] = "#0B4F9E"
        other["semantic_color"]["negative"]["hex"] = "#C1121F"
        other["semantic_color"]["warning"]["hex"] = "#B26B00"
        other["semantic_color"]["neutral"]["hex"] = "#4A4A4A"
        other["semantic_color"]["structure"]["hex"] = "#000000"
        for role in ("display", "prose", "ui", "data"):
            other["type_roles"][role]["family"] = f"Some Other {role.title()}"
        self.assertEqual(self.run_main(COMPLETE, other, "--expect-distinct"), 0)


if __name__ == "__main__":
    unittest.main()
