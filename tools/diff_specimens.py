#!/usr/bin/env python3
"""Name the differences between two specimens, including the ones eyes cannot be trusted to judge.

    python3 tools/diff_specimens.py a.pptx b.pptx
    python3 tools/diff_specimens.py a.inspect.ndjson b.inspect.ndjson --expect-distinct

Reads two object inventories (a .pptx directly, or NDJSON already produced by inspect_pptx.py),
pairs their objects, and grades every delta: color perceptually in OKLab, geometry to the pixel,
type by size and family. Content differences (the words) are reported separately from design
differences, because two specimens can be the same design carrying different words — and that is
precisely the verdict this tool exists to render in both directions:

- `--expect-same` exits nonzero when the designs differ visibly: a regression check.
- `--expect-distinct` exits nonzero when two supposedly distinct identities produced the same
  design: a convergence check. Distinct briefs or distinct declared profiles must produce
  measurably distinct surfaces.

Grades: `identical` (no delta), `sub-perceptual` (a delta most viewers cannot name: color below
the just-noticeable threshold, geometry within 1 px), `visible` (everything above). The design
verdict ignores text content and object names; structure, geometry, color, and type decide it.
"""

import json
import sys
from pathlib import Path

# Color deltas in OKLab, scaled by 100 to match common ΔE intuition.
DE_SUBPERCEPTUAL = 2.0
PX_SUBPERCEPTUAL = 1
FONT_PX_SUBPERCEPTUAL = 0.5


def srgb_to_oklab(hex_color):
    channels = []
    raw = hex_color.lstrip("#")
    for index in (0, 2, 4):
        value = int(raw[index : index + 2], 16) / 255
        channels.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    long_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    medium = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    short = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (
        0.2104542553 * long_ + 0.7936177850 * medium - 0.0040720468 * short,
        1.9779984951 * long_ - 2.4285922050 * medium + 0.4505937099 * short,
        0.0259040371 * long_ + 0.7827717662 * medium - 0.8086757660 * short,
    )


def delta_e(color_a, color_b):
    lab_a, lab_b = srgb_to_oklab(color_a), srgb_to_oklab(color_b)
    return 100 * sum((x - y) ** 2 for x, y in zip(lab_a, lab_b)) ** 0.5


def load_inventory(path):
    path = Path(path)
    if path.suffix.casefold() == ".pptx":
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import inspect_pptx

        return inspect_pptx.inspect(path)
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def objects_by_slide(records):
    slides = {}
    for record in records:
        if record["kind"] in ("textbox", "shape", "line", "picture", "graphicFrame", "group"):
            slides.setdefault(record["slide"], []).append(record)
    return slides


def backgrounds_by_slide(records):
    return {
        record["slide"]: record.get("background")
        for record in records
        if record["kind"] == "slide"
    }


class Report:
    def __init__(self):
        self.design = []   # (grade, message)
        self.content = []  # text differences, never part of the design verdict

    def add(self, grade, message):
        self.design.append((grade, message))

    @property
    def worst(self):
        order = {"identical": 0, "sub-perceptual": 1, "visible": 2}
        return max((order[grade] for grade, _ in self.design), default=0)


def grade_geometry(delta_px):
    if delta_px == 0:
        return "identical"
    return "sub-perceptual" if delta_px <= PX_SUBPERCEPTUAL else "visible"


def grade_color(de):
    # Any two differing values are at least a nameable difference; the threshold only
    # decides whether most viewers could see it, not whether it exists.
    return "sub-perceptual" if de < DE_SUBPERCEPTUAL else "visible"


def compare_objects(where, left, right, report):
    if left["kind"] != right["kind"] or left.get("geometry") != right.get("geometry"):
        report.add(
            "visible",
            f"{where}: kind changed {left['kind']}/{left.get('geometry')} -> "
            f"{right['kind']}/{right.get('geometry')}",
        )
        return
    box_a, box_b = left.get("bbox"), right.get("bbox")
    if box_a and box_b:
        deltas = [abs(a - b) for a, b in zip(box_a, box_b)]
        worst = max(deltas)
        if worst:
            axis = ("left", "top", "width", "height")[deltas.index(worst)]
            report.add(grade_geometry(worst), f"{where}: {axis} differs by {worst}px ({box_a} -> {box_b})")
    color_a, color_b = left.get("color"), right.get("color")
    if color_a and color_b and color_a != color_b:
        de = delta_e(color_a, color_b)
        report.add(grade_color(de), f"{where}: color {color_a} -> {color_b} (dE {de:.1f})")
    elif bool(color_a) != bool(color_b):
        report.add("visible", f"{where}: fill present on one side only")
    size_a, size_b = left.get("fontSizePx"), right.get("fontSizePx")
    if size_a is not None and size_b is not None and size_a != size_b:
        delta = abs(size_a - size_b)
        grade = "sub-perceptual" if delta <= FONT_PX_SUBPERCEPTUAL else "visible"
        report.add(grade, f"{where}: type size {size_a}px -> {size_b}px")
    family_a, family_b = left.get("fontFamily"), right.get("fontFamily")
    if family_a and family_b and family_a != family_b:
        report.add("visible", f"{where}: typeface {family_a} -> {family_b}")
    text_a, text_b = left.get("text"), right.get("text")
    if text_a is not None and text_b is not None and text_a != text_b:
        report.content.append(f"{where}: {text_a!r} -> {text_b!r}")


def compare(records_a, records_b):
    report = Report()
    slides_a, slides_b = objects_by_slide(records_a), objects_by_slide(records_b)
    if set(slides_a) != set(slides_b):
        report.add("visible", f"slide sets differ: {sorted(slides_a)} vs {sorted(slides_b)}")
        return report
    grounds_a, grounds_b = backgrounds_by_slide(records_a), backgrounds_by_slide(records_b)
    for number in sorted(slides_a):
        ground_a, ground_b = grounds_a.get(number), grounds_b.get(number)
        if ground_a and ground_b and ground_a != ground_b:
            de = delta_e(ground_a, ground_b)
            report.add(
                grade_color(de),
                f"slide {number}: surface {ground_a} -> {ground_b} (dE {de:.1f})",
            )
        elif bool(ground_a) != bool(ground_b):
            report.add("visible", f"slide {number}: background declared on one side only")
        left_objects, right_objects = slides_a[number], slides_b[number]
        if len(left_objects) != len(right_objects):
            report.add(
                "visible",
                f"slide {number}: object count {len(left_objects)} vs {len(right_objects)}",
            )
            continue
        # Pair by position in z-order; names are authored labels, not identity.
        for index, (left, right) in enumerate(zip(left_objects, right_objects), 1):
            where = f"slide {number} obj {index} ({left.get('name') or left['kind']})"
            compare_objects(where, left, right, report)
    return report


def main(argv):
    flags = {arg for arg in argv[1:] if arg.startswith("--")}
    paths = [arg for arg in argv[1:] if not arg.startswith("--")]
    if len(paths) != 2 or flags - {"--expect-same", "--expect-distinct"}:
        print(__doc__.strip())
        return 2
    report = compare(load_inventory(paths[0]), load_inventory(paths[1]))
    for grade, message in sorted(report.design, key=lambda item: item[0]):
        print(f"[{grade}] {message}")
    for message in report.content:
        print(f"[content] {message}")
    if report.worst == 2:
        verdict = "DISTINCT DESIGNS"
    elif report.worst == 1:
        verdict = "SAME DESIGN within sub-perceptual deltas"
    else:
        verdict = "SAME DESIGN, delta-free" + (" (different content)" if report.content else "")
    print(f"\nVerdict: {verdict}"
          + (f" · {len(report.content)} content difference(s), excluded from the design verdict"
             if report.content else ""))
    if "--expect-same" in flags and report.worst == 2:
        print("FAIL: expected the same design; visible design deltas found")
        return 1
    if "--expect-distinct" in flags and report.worst < 2:
        print("FAIL: expected measurably distinct designs; these converge to one design")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
