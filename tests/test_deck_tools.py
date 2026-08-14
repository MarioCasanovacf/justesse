"""Round-trip tests for the presentation-safe HTML converter and the object inspector.

The converter's claim is that nothing is rasterized and every element survives as a native,
editable object. These tests verify that claim the way the reference says to verify it: by reading
the inventory back out of the written file, not by trusting the converter's own report.
"""

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import html2deck  # noqa: E402
import inspect_pptx  # noqa: E402


DECK = """
<div class="slide" data-name="situation" style="background:#FAF8F2">
  <div class="wrapper">
    <div class="text" data-name="stage"
         style="left:72px;top:36px;width:260px;height:22px;font-size:14px;color:#333333">01 / Situation</div>
    <div class="line" data-name="top-rule"
         style="left:72px;top:69px;width:1136px;height:1px;background:#333333"></div>
    <div class="text" data-name="title"
         style="left:72px;top:120px;width:900px;height:120px;font-size:44px;font-weight:700;color:#111111">Billing clarity drives<br>the negative signal</div>
    <div class="rect" data-name="panel"
         style="left:72px;top:300px;width:400px;height:180px;background:#EEEEEE;border:1px solid #999999"></div>
    <div class="ellipse" data-name="dot"
         style="left:520px;top:340px;width:24px;height:24px;background:#B00020"></div>
  </div>
</div>
<div class="slide" data-name="evidence">
  <div class="text" data-name="title"
       style="left:72px;top:60px;width:900px;height:60px;font-size:32px;color:#111111">Negative volume fell</div>
  <div class="rect" data-name="bar"
       style="left:72px;top:400px;width:60px;height:200px;background:#B00020"></div>
</div>
"""


def convert(html):
    """Convert `html` and return the inspector's records for the written file."""
    slides = html2deck.parse_html(html)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "deck.pptx"
        html2deck.build_pptx(slides, path)
        return slides, inspect_pptx.inspect(path)


class ConverterTests(unittest.TestCase):
    def setUp(self):
        self.slides, self.records = convert(DECK)

    def by_kind(self, kind):
        return [record for record in self.records if record["kind"] == kind]

    def named(self, name, slide):
        return next(
            record
            for record in self.records
            if record.get("name") == name and record.get("slide") == slide
        )

    def test_every_slide_and_object_survives(self):
        self.assertEqual(self.by_kind("deck")[0]["slides"], 2)
        self.assertEqual([record["objects"] for record in self.by_kind("slide")], [5, 2])

    def test_nothing_is_rasterized(self):
        """The whole point of the subset: no picture, no chart frame, no flattened group."""
        self.assertEqual(self.by_kind("picture"), [])
        self.assertEqual(self.by_kind("graphicFrame"), [])
        self.assertEqual(self.by_kind("group"), [])
        self.assertFalse([record for record in self.records if record.get("rasterized")])

    def test_text_stays_live_text_with_the_authored_string(self):
        self.assertEqual(self.named("stage", 1)["kind"], "textbox")
        self.assertEqual(self.named("stage", 1)["text"], "01 / Situation")
        self.assertEqual(
            self.named("title", 1)["text"], "Billing clarity drives\nthe negative signal"
        )

    def test_geometry_round_trips_exactly(self):
        self.assertEqual(self.named("stage", 1)["bbox"], [72, 36, 260, 22])
        self.assertEqual(self.named("panel", 1)["bbox"], [72, 300, 400, 180])
        self.assertEqual(self.named("bar", 2)["bbox"], [72, 400, 60, 200])

    def test_kinds_map_to_their_native_geometry(self):
        self.assertEqual(self.named("panel", 1)["geometry"], "rect")
        self.assertEqual(self.named("dot", 1)["geometry"], "ellipse")
        self.assertEqual(self.named("top-rule", 1)["kind"], "line")
        self.assertEqual(self.named("top-rule", 1)["geometry"], "line")

    def test_declared_colors_reach_the_file(self):
        self.assertEqual(self.named("panel", 1)["color"], "#EEEEEE")
        self.assertEqual(self.named("dot", 1)["color"], "#B00020")

    def test_slide_background_is_declared_not_inherited(self):
        self.assertEqual(self.slides[0].background, "FAF8F2")
        self.assertIsNone(self.slides[1].background)

    def test_canvas_maps_to_the_sixteen_by_nine_frame(self):
        self.assertEqual(html2deck.CANVAS_WIDTH_PX, 1280)
        self.assertEqual(html2deck.CANVAS_HEIGHT_PX, 720)
        self.assertEqual(html2deck.SLIDE_WIDTH_EMU, 12192000)
        self.assertEqual(html2deck.SLIDE_HEIGHT_EMU, 6858000)
        self.assertEqual(html2deck.CANVAS_WIDTH_PX * 9, html2deck.CANVAS_HEIGHT_PX * 16)


PREVIEW_HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Deck</title>
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; }
  .slide { position: relative; width: 1280px; height: 720px; overflow: hidden; margin: 0 auto; }
  .text, .rect, .ellipse, .line { position: absolute; margin: 0; padding: 0; }
  .ellipse { border-radius: 50%; }
</style>
</head>
<body style="background:#123456">
"""


class PreviewStylesheetTests(unittest.TestCase):
    """The canvas preview block is geometry for the browser and invisible to the converter.

    Authoring HTML for a canvas the browser does not assume means the page renders as a stacked
    column unless a stylesheet declares the fixed frame and the absolute boxes. That stylesheet has
    to be inert on the way to the deck, in both directions: the author reviews a real slide, and no
    one can move a declared value out of the inline style, where the subset is enforced, into a
    stylesheet where it would render in the preview and quietly vanish from the presentation file.
    """

    def test_a_preview_stylesheet_does_not_change_the_converted_file(self):
        _, plain = convert(DECK)
        _, previewed = convert(PREVIEW_HEAD + DECK + "</body></html>")
        self.assertEqual(plain, previewed)

    def test_the_page_background_is_not_mistaken_for_a_slide(self):
        """The body carries the canvas fill so nothing reads as backdrop; it converts to nothing."""
        slides, records = convert(PREVIEW_HEAD + DECK + "</body></html>")
        self.assertEqual(len(slides), 2)
        self.assertEqual([slide.background for slide in slides], ["FAF8F2", None])
        self.assertNotIn("#123456", "".join(str(record) for record in records))

    def test_the_stylesheet_is_not_a_way_around_the_subset(self):
        """Its rules name properties the converter refuses inline; it still refuses them inline."""
        hidden = PREVIEW_HEAD.replace(
            ".ellipse { border-radius: 50%; }", ".ellipse { border-radius: 50%; background: #00FF00; }"
        )
        _, records = convert(hidden + DECK + "</body></html>")
        dot = next(record for record in records if record.get("name") == "dot")
        self.assertEqual(dot["color"], "#B00020")
        with self.assertRaises(html2deck.UnsupportedConstruct):
            html2deck.parse_html(
                '<div class="slide"><div class="rect" data-name="x" '
                'style="left:0px;top:0px;width:10px;height:10px;position:absolute"></div></div>'
            )


class RejectionTests(unittest.TestCase):
    """Constructs outside the subset must fail at authoring time, never flatten silently."""

    def assertRejected(self, style, *, fragment):
        html = f'<div class="slide"><div class="rect" data-name="x" style="{style}"></div></div>'
        with self.assertRaises(html2deck.UnsupportedConstruct) as caught:
            html2deck.parse_html(html)
        self.assertIn(fragment, str(caught.exception))

    def test_runtime_layout_is_rejected(self):
        base = "left:0px;top:0px;width:10px;height:10px;background:#000000;"
        self.assertRejected(base + "display:flex", fragment="display")
        self.assertRejected(base + "position:relative", fragment="position")
        self.assertRejected(base + "padding:8px", fragment="padding")

    def test_non_absolute_dimensions_are_rejected(self):
        base = "left:0px;top:0px;height:10px;background:#000000;"
        self.assertRejected(base + "width:50%", fragment="percentage")
        self.assertRejected(base + "width:auto", fragment="auto")
        self.assertRejected(base + "width:calc(100px - 2px)", fragment="calc")

    def test_effects_without_shape_equivalents_are_rejected(self):
        base = "left:0px;top:0px;width:10px;height:10px;background:#000000;"
        self.assertRejected(base + "box-shadow:0 1px 2px #000000", fragment="box-shadow")
        self.assertRejected(base + "filter:blur(2px)", fragment="filter")
        self.assertRejected(base + "transform:rotate(2deg)", fragment="transform")
        self.assertRejected(base + "opacity:0.5", fragment="opacity")

    def test_gradients_and_external_images_are_rejected(self):
        base = "left:0px;top:0px;width:10px;height:10px;"
        self.assertRejected(
            base + "background:linear-gradient(#000000,#ffffff)", fragment="gradient"
        )
        self.assertRejected(base + "background:url(logo.png)", fragment="images")

    def test_a_box_without_absolute_coordinates_is_rejected(self):
        self.assertRejected("left:0px;top:0px;width:10px;background:#000000", fragment="height")

    def test_a_non_hex_color_is_rejected(self):
        self.assertRejected(
            "left:0px;top:0px;width:10px;height:10px;background:rebeccapurple",
            fragment="hex value",
        )

    def test_an_element_outside_a_slide_is_rejected(self):
        with self.assertRaises(html2deck.UnsupportedConstruct) as caught:
            html2deck.parse_html('<div class="rect" style="left:0px;top:0px;width:1px;height:1px"></div>')
        self.assertIn("outside any `.slide`", str(caught.exception))

    def test_a_text_object_without_text_is_rejected(self):
        html = '<div class="slide"><div class="text" style="left:0px;top:0px;width:10px;height:10px;font-size:12px"></div></div>'
        with self.assertRaises(html2deck.UnsupportedConstruct) as caught:
            html2deck.parse_html(html)
        self.assertIn("carries no text", str(caught.exception))

    def test_a_shape_carrying_text_is_rejected(self):
        html = '<div class="slide"><div class="rect" style="left:0px;top:0px;width:10px;height:10px;background:#000000">hello</div></div>'
        with self.assertRaises(html2deck.UnsupportedConstruct) as caught:
            html2deck.parse_html(html)
        self.assertIn("use a separate `text` object", str(caught.exception))

    def test_html_without_a_slide_is_rejected(self):
        with self.assertRaises(html2deck.UnsupportedConstruct):
            html2deck.parse_html("<p>just a paragraph</p>")


if __name__ == "__main__":
    unittest.main()
