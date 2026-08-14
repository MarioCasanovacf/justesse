"""Tests for the declaration-to-tokens emitter.

The emitter's contract: it emits only from a declaration the gate would pass, its output is a
faithful mechanical projection of the declared values, and its tokens are namespaced so they can
be consumed by reference without colliding with a project's own properties.
"""

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "harness"))
sys.path.insert(0, str(ROOT / "tests"))

import declaration2tokens  # noqa: E402

from test_profile_gate import COMPLETE  # noqa: E402


class TokenEmissionTests(unittest.TestCase):
    def test_tokens_project_the_declared_values_exactly(self):
        tokens = declaration2tokens.tokens_from(COMPLETE)
        self.assertEqual(tokens["j-surface"], "#FFFDF7")
        self.assertEqual(tokens["j-ink"], "#121212")
        self.assertEqual(tokens["j-positive"], "#1F5F3F")
        self.assertEqual(tokens["j-structure"], "#121212")
        self.assertEqual(tokens["j-radius"], "0px")
        self.assertEqual(tokens["j-hairline"], "1px")
        self.assertEqual(tokens["j-space"], "8px")
        self.assertEqual(tokens["j-font-display"], '"Source Serif 4", Georgia, serif')

    def test_every_token_is_namespaced(self):
        for key in declaration2tokens.tokens_from(COMPLETE):
            with self.subTest(key=key):
                self.assertTrue(key.startswith("j-"))

    def test_no_dark_variant_emits_no_dark_tokens(self):
        tokens = declaration2tokens.tokens_from(COMPLETE)
        self.assertNotIn("j-dark-surface", tokens)
        css = declaration2tokens.as_css(tokens, "atlas", "0" * 64)
        self.assertNotIn("prefers-color-scheme", css)

    def test_a_declared_dark_variant_emits_the_media_block(self):
        declaration = copy.deepcopy(COMPLETE)
        declaration["canvas"]["dark_variant"] = {"surface": "#101010", "ink": "#F2F2F2"}
        tokens = declaration2tokens.tokens_from(declaration)
        css = declaration2tokens.as_css(tokens, "atlas", "0" * 64)
        self.assertIn("@media (prefers-color-scheme: dark)", css)
        self.assertIn("--j-surface: #101010;", css)

    def test_css_carries_provenance_and_the_no_hand_edit_notice(self):
        css = declaration2tokens.as_css(
            declaration2tokens.tokens_from(COMPLETE), "atlas", "abc123" + "0" * 58
        )
        self.assertIn("personal:atlas", css)
        self.assertIn("abc1230000000000", css)
        self.assertIn("Do not hand-edit; re-declare and re-emit", css)


class GateCompositionTests(unittest.TestCase):
    """Nothing is emitted from a declaration the gate would refuse."""

    def run_main(self, declaration, tmp, *flags):
        import json

        path = Path(tmp) / "declaration.json"
        path.write_text(json.dumps(declaration), encoding="utf-8")
        return declaration2tokens.main(["emit", str(path), *flags])

    def test_a_complete_declaration_emits(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_main(COMPLETE, tmp), 0)

    def test_an_incomplete_declaration_is_blocked(self):
        import tempfile

        declaration = copy.deepcopy(COMPLETE)
        declaration["canvas"]["surface"] = "off-white"
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_main(declaration, tmp), 1)

    def test_a_deferral_is_blocked(self):
        import tempfile

        declaration = copy.deepcopy(COMPLETE)
        declaration["action_treatment"] = "como veas"
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_main(declaration, tmp), 1)


if __name__ == "__main__":
    unittest.main()
