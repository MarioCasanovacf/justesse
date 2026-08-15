#!/usr/bin/env python3
"""Compare two profile declarations before either one is built.

    python3 tools/diff_declarations.py a.json b.json
    python3 tools/diff_declarations.py a.json b.json --expect-distinct

`diff_specimens.py` answers whether two identities produced the same design, but it can only
answer after both have been built. Convergence is cheaper to catch one step earlier: two
declarations that agree on canvas, type stack, and geometry will produce surfaces that agree,
and finding that out costs four surfaces if the first check happens at the end.

What is compared is what the declaration actually fixes: canvas and semantic colors graded
perceptually in OKLab, the four type roles by family, and the four geometry values to the pixel.
Voice, exclusions, and posture are reported as text differences and never sway the verdict, for
the same reason `diff_specimens.py` excludes copy — two identities can share a register and still
look nothing alike, and two identities can differ in every adjective and still converge on one
design.

The verdict is deliberately blunt. A declaration pair whose colors are all sub-perceptual and
whose type stacks and geometry match is one identity wearing two names, whatever its prose says.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from diff_specimens import DE_SUBPERCEPTUAL, delta_e  # noqa: E402

TYPE_ROLES = ("display", "prose", "ui", "data")
SEMANTIC_ROLES = ("positive", "warning", "negative", "neutral", "structure")
GEOMETRY_KEYS = ("corner_radius_px", "hairline_px", "emphasis_rule_px", "spacing_base_px")


def colors_of(declaration):
    colors = {
        "canvas.surface": declaration["canvas"]["surface"],
        "canvas.ink": declaration["canvas"]["ink"],
    }
    for role in SEMANTIC_ROLES:
        colors[f"semantic.{role}"] = declaration["semantic_color"][role]["hex"]
    return colors


def families_of(declaration):
    return {role: declaration["type_roles"][role]["family"] for role in TYPE_ROLES}


def compare(a, b):
    """Return (findings, distinct_signals, total_signals)."""
    findings = []
    distinct = 0
    total = 0

    for key, left in colors_of(a).items():
        right = colors_of(b)[key]
        total += 1
        de = delta_e(left, right)
        if de < DE_SUBPERCEPTUAL:
            findings.append(f"[sub-perceptual] {key}: {left} vs {right} (dE {de:.1f})")
        else:
            distinct += 1
            findings.append(f"[distinct] {key}: {left} vs {right} (dE {de:.1f})")

    families_b = families_of(b)
    for role, left in families_of(a).items():
        right = families_b[role]
        total += 1
        if left == right:
            findings.append(f"[same] type.{role}: both {left}")
        else:
            distinct += 1
            findings.append(f"[distinct] type.{role}: {left} vs {right}")

    for key in GEOMETRY_KEYS:
        left, right = a["geometry"][key], b["geometry"][key]
        total += 1
        if left == right:
            findings.append(f"[same] geometry.{key}: both {left}")
        else:
            distinct += 1
            findings.append(f"[distinct] geometry.{key}: {left} vs {right}")

    for key, getter in (
        ("action_treatment", lambda d: d["action_treatment"]),
        ("posture.closing", lambda d: d["posture"]["closing"]),
        ("voice.register", lambda d: ", ".join(d["voice"]["register"])),
    ):
        if getter(a) != getter(b):
            findings.append(f"[text] {key} differs; excluded from the verdict")

    return findings, distinct, total


def main(argv):
    flags = {arg for arg in argv[1:] if arg.startswith("--")}
    paths = [arg for arg in argv[1:] if not arg.startswith("--")]
    if len(paths) != 2 or flags - {"--expect-distinct", "--expect-same"}:
        print(__doc__.strip())
        return 2
    try:
        a, b = (json.loads(Path(path).read_text(encoding="utf-8")) for path in paths)
    except (OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}")
        return 1

    findings, distinct, total = compare(a, b)
    for finding in findings:
        print(finding)

    name_a = a["identity"]["name"]
    name_b = b["identity"]["name"]
    share = distinct / total
    verdict = "DISTINCT IDENTITIES" if share >= 0.5 else "CONVERGENT IDENTITIES"
    print(
        f"\nVerdict: {verdict} · {distinct} of {total} fixed signals differ "
        f"({share:.0%}) between personal:{name_a} and personal:{name_b}"
    )
    if "--expect-distinct" in flags and verdict != "DISTINCT IDENTITIES":
        print("FAIL: expected distinct identities; these two would build the same design.")
        return 1
    if "--expect-same" in flags and verdict != "CONVERGENT IDENTITIES":
        print("FAIL: expected the same identity.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
