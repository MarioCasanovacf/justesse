"""Tests for the specimen comparison instrument.

The instrument's claim is the business-card claim: it names differences most viewers cannot,
grades them perceptually, and renders a design verdict that content differences cannot sway.
Two specimens carrying different words on one design are the same design, and two identities
producing the same design is convergence, which the harness treats as a hard-gate failure.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import diff_specimens  # noqa: E402
import html2deck  # noqa: E402
import inspect_pptx  # noqa: E402


BASE = """
<div class="slide" data-name="s1" style="background:#FAF8F2">
  <div class="text" data-name="stage"
       style="left:72px;top:36px;width:260px;height:22px;font-size:14px;color:#333333;font-family:TestSans">01 / Situation</div>
  <div class="rect" data-name="panel"
       style="left:72px;top:300px;width:400px;height:180px;background:#EEEEEE"></div>
  <div class="line" data-name="rule"
       style="left:72px;top:69px;width:1136px;height:1px;background:#333333"></div>
</div>
"""


def inventory(html):
    slides = html2deck.parse_html(html)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "specimen.pptx"
        html2deck.build_pptx(slides, path)
        return inspect_pptx.inspect(path)


def variant(**replacements):
    html = BASE
    for old, new in replacements.items():
        html = html.replace(old.replace("_", ":"), new)
    return html


class InventoryTypeTests(unittest.TestCase):
    def test_inspector_captures_type_and_background(self):
        records = inventory(BASE)
        slide = next(record for record in records if record["kind"] == "slide")
        self.assertEqual(slide["background"], "#FAF8F2")
        stage = next(record for record in records if record.get("name") == "stage")
        self.assertEqual(stage["fontSizePx"], 14.0)
        self.assertEqual(stage["fontFamily"], "TestSans")


class VerdictTests(unittest.TestCase):
    def test_a_specimen_against_itself_is_delta_free(self):
        report = diff_specimens.compare(inventory(BASE), inventory(BASE))
        self.assertEqual(report.design, [])
        self.assertEqual(report.content, [])
        self.assertEqual(report.worst, 0)

    def test_different_words_on_one_design_stay_the_same_design(self):
        """The business-card case: another name, the same card."""
        other = inventory(variant(**{"01 / Situation": "02 / Evidence"}))
        report = diff_specimens.compare(inventory(BASE), other)
        self.assertEqual(report.design, [])
        self.assertEqual(len(report.content), 1)
        self.assertEqual(report.worst, 0)

    def test_a_one_pixel_shift_is_named_and_graded_sub_perceptual(self):
        other = inventory(variant(left_72px=("left:73px")))
        report = diff_specimens.compare(inventory(BASE), other)
        grades = {grade for grade, _ in report.design}
        self.assertEqual(grades, {"sub-perceptual"})
        self.assertTrue(any("1px" in message for _, message in report.design))

    def test_a_whisper_of_paper_temperature_is_still_named(self):
        """FAF8F2 to FAF7F0 sits far below what a viewer can call out; name it anyway."""
        other = inventory(variant(**{"#FAF8F2": "#FAF7F0"}))
        report = diff_specimens.compare(inventory(BASE), other)
        self.assertEqual(len(report.design), 1)
        grade, message = report.design[0]
        self.assertEqual(grade, "sub-perceptual")
        self.assertIn("surface", message)
        self.assertIn("dE", message)

    def test_a_frank_color_change_is_visible(self):
        other = inventory(variant(**{"#EEEEEE": "#B0C4DE"}))
        report = diff_specimens.compare(inventory(BASE), other)
        self.assertEqual(report.worst, 2)

    def test_a_type_family_change_is_visible(self):
        other = inventory(variant(TestSans="OtherSerif"))
        report = diff_specimens.compare(inventory(BASE), other)
        self.assertTrue(
            any("typeface" in message for grade, message in report.design if grade == "visible")
        )

    def test_structure_changes_are_visible(self):
        other = inventory(BASE.replace(
            '<div class="line" data-name="rule"\n       style="left:72px;top:69px;width:1136px;height:1px;background:#333333"></div>',
            "",
        ))
        report = diff_specimens.compare(inventory(BASE), other)
        self.assertEqual(report.worst, 2)
        self.assertTrue(any("object count" in message for _, message in report.design))


class GateTests(unittest.TestCase):
    """The two exit-code directions: regression check and convergence check."""

    def run_main(self, records_a, records_b, flag):
        with tempfile.TemporaryDirectory() as directory:
            path_a = Path(directory) / "a.ndjson"
            path_b = Path(directory) / "b.ndjson"
            import json

            path_a.write_text("\n".join(json.dumps(r) for r in records_a), encoding="utf-8")
            path_b.write_text("\n".join(json.dumps(r) for r in records_b), encoding="utf-8")
            return diff_specimens.main(["diff", str(path_a), str(path_b), flag])

    def test_expect_distinct_fails_on_convergence(self):
        same = inventory(variant(**{"01 / Situation": "another name"}))
        self.assertEqual(self.run_main(inventory(BASE), same, "--expect-distinct"), 1)

    def test_expect_distinct_passes_on_real_difference(self):
        other = inventory(variant(**{"#EEEEEE": "#B0C4DE"}))
        self.assertEqual(self.run_main(inventory(BASE), other, "--expect-distinct"), 0)

    def test_expect_same_fails_on_visible_difference(self):
        other = inventory(variant(**{"#EEEEEE": "#B0C4DE"}))
        self.assertEqual(self.run_main(inventory(BASE), other, "--expect-same"), 1)

    def test_expect_same_tolerates_sub_perceptual_drift(self):
        other = inventory(variant(left_72px="left:73px"))
        self.assertEqual(self.run_main(inventory(BASE), other, "--expect-same"), 0)


if __name__ == "__main__":
    unittest.main()
