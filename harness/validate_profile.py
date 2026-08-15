#!/usr/bin/env python3
"""Gate for a `personal:<name>` profile declaration.

This skill ships no profile. Activating the flag opens the ten-field declaration defined in
`skill/justesse/references/profile-declaration.md`; this validator decides whether a declaration is
complete and concrete enough to design against. It is deliberately dependency-free.

Usage:

    python3 harness/validate_profile.py path/to/declaration.json

Exit status is 0 only when every required field holds a concrete value. What this enforces is
completeness and concreteness. It cannot detect a value borrowed from another profile or from a
published artifact; that remains a review gate, stated in the reference.
"""

import json
import re
import sys
from pathlib import Path


HEX = re.compile(r"\A#[0-9A-Fa-f]{6}\Z")
AVAILABILITY = {"installed", "licensed", "substitute-required"}
TYPE_ROLES = ("display", "prose", "ui", "data")
SEMANTIC_ROLES = ("positive", "warning", "negative", "neutral", "structure")
REQUIRED_FIELDS = (
    "identity",
    "canvas",
    "type_roles",
    "semantic_color",
    "action_treatment",
    "geometry",
    "voice",
    "exclusions",
    "posture",
    "evidence",
)

# Answers that look filled in but decide nothing. Matched against the whole normalized string.
NON_ANSWERS = {
    "",
    "-",
    "--",
    "?",
    "??",
    "n/a",
    "na",
    "none",
    "null",
    "nil",
    "tbd",
    "tba",
    "todo",
    "to be defined",
    "to be determined",
    "pending",
    "placeholder",
    "example",
    "default",
    "the default",
    "standard",
    "the usual",
    "usual",
    "same",
    "same as before",
    "same as last time",
    "unchanged",
    "you decide",
    "your call",
    "your choice",
    "up to you",
    "use your judgment",
    "use your judgement",
    "whatever",
    "whatever fits",
    "whatever you think",
    "anything",
    "any",
    "idk",
    "i don't know",
    "dunno",
    "unknown",
    "xxx",
    "xx",
    "lorem ipsum",
    # The same non-answers in Spanish, which is what this form is most often filled in.
    "pendiente",
    "por definir",
    "no aplica",
    "ninguno",
    "ninguna",
    "el de siempre",
    "la de siempre",
    "lo de siempre",
    "igual que antes",
    "lo mismo",
    "cualquiera",
    "lo que sea",
    "no sé",
    "no se",
    "ni idea",
}
# Deferrals that can hide inside a longer sentence.
NON_ANSWER_SUBSTRINGS = (
    "you decide",
    "up to you",
    "use your judgment",
    "use your judgement",
    "same as the",
    "same as our",
    "like the other",
    "to be defined",
    "to be determined",
    "tbd",
    "tú decides",
    "tu decides",
    "tú decide",
    "tu decide",
    "como veas",
    "a tu criterio",
    "lo que tú creas",
    "lo que tu creas",
    "como tú creas",
    "como tu creas",
    "lo que veas",
    "lo que prefieras",
    # A deferral that takes a qualifier and keeps deferring: "lo que sea mejor", "lo que sea
    # más claro". Matching the exact phrase alone let every qualified form through.
    "lo que sea",
    "el que quieras",
    "igual que el",
    "igual que la",
    "como el otro",
    "como la otra",
)

# A worked example per field, so a blocked run can re-ask concretely instead of saying "invalid".
# These fix the shape of an answer, never propose one: a declaration that echoes them has declared
# nothing, which is why `profile-declaration.md` refuses copies of them.
EXAMPLES = {
    "identity.name": "atlas",
    "identity.owner": "Atlas Research Cooperative",
    "identity.scope": '["quarterly research notes", "internal decision memos"]',
    "identity.purpose": "present bounded quantitative research without implying commercial claims",
    "canvas.surface": "#FFFDF7",
    "canvas.ink": "#121212",
    "canvas.dark_variant": '{"surface": "#101010", "ink": "#F2F2F2"} or null for none',
    "type_roles.display.family": "Source Serif 4",
    "type_roles.display.fallback": "Georgia, serif",
    "type_roles.display.availability": "installed",
    "semantic_color.positive.hex": "#1F5F3F",
    "semantic_color.positive.redundancy": '["direct label", "upward marker"]',
    "action_treatment": "an ink-outlined button with an underlined label, never a status fill",
    "geometry.corner_radius_px": "0",
    "geometry.hairline_px": "1 (not \"thin\")",
    "geometry.emphasis_rule_px": "3",
    "geometry.spacing_base_px": "8",
    "geometry.elevation": "no shadow at any level; separation comes from rules and spacing",
    "voice.person": "first person singular for authored statements",
    "voice.heading_case": "sentence case",
    "voice.register": '["precise", "restrained", "impersonal"]',
    "voice.refuses": '["exclamation marks", "superlatives", "brand-we"]',
    "exclusions": '["gradients", "glow and glass", "automatic dark mode", "bounce motion", "stock photography of people"]',
    "posture.density": "balanced, one evidence module per fold",
    "posture.motion": "none beyond focus states",
    "posture.closing": "three or four bounded paths with my lean stated and named as a lean, never a single next step",
    "evidence.unit": "stated on every axis and every displayed total",
    "evidence.period": "ISO week range, unbroken",
    "evidence.source": "named dataset and capture date in the caption",
    "evidence.uncertainty": "interval bands on every estimated series",
}


def example_for(field: str) -> str:
    """The closest worked example for a field path, including indexed and per-role paths."""
    stripped = re.sub(r"\[\d+\]", "", field)
    if stripped in EXAMPLES:
        return EXAMPLES[stripped]
    parts = stripped.split(".")
    # Per-role paths reuse the documented role's example: type_roles.ui.family -> display.family.
    if len(parts) == 3 and parts[0] == "type_roles":
        return EXAMPLES.get(f"type_roles.display.{parts[2]}", "")
    if len(parts) == 3 and parts[0] == "semantic_color":
        return EXAMPLES.get(f"semantic_color.positive.{parts[2]}", "")
    while parts:
        parts.pop()
        candidate = ".".join(parts)
        if candidate in EXAMPLES:
            return EXAMPLES[candidate]
    return ""


failures: list[str] = []


def fail(field: str, reason: str) -> None:
    failures.append(f"{field}: {reason}")


def normalized(value: str) -> str:
    return " ".join(value.split()).strip().casefold()


def concrete(field: str, value, *, min_words: int = 1) -> bool:
    """A string answer that can be applied without a second interpretation."""
    if not isinstance(value, str):
        fail(field, f"expected text, got {type(value).__name__}")
        return False
    text = normalized(value)
    if text in NON_ANSWERS:
        fail(field, f"non-answer {value!r}; re-ask this field")
        return False
    for marker in NON_ANSWER_SUBSTRINGS:
        if marker in text:
            fail(field, f"deferral {value!r}; re-ask this field")
            return False
    if len(text.split()) < min_words:
        fail(field, f"underdetermined {value!r}; needs at least {min_words} word(s)")
        return False
    return True


def hex_color(field: str, value) -> bool:
    if not isinstance(value, str) or not HEX.match(value.strip()):
        fail(field, f"expected a #RRGGBB hex value, got {value!r}")
        return False
    return True


def whole_number(field: str, value) -> bool:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        fail(field, f"expected a non-negative whole number of px, got {value!r}")
        return False
    return True


def mapping(field: str, value) -> bool:
    if not isinstance(value, dict):
        fail(field, f"expected an object, got {type(value).__name__}")
        return False
    return True


def string_list(field: str, value, minimum: int) -> bool:
    if not isinstance(value, list):
        fail(field, f"expected a list, got {type(value).__name__}")
        return False
    if len(value) < minimum:
        fail(field, f"needs at least {minimum} entries, got {len(value)}")
        return False
    ok = True
    for index, item in enumerate(value):
        if not concrete(f"{field}[{index}]", item):
            ok = False
    return ok


def check_identity(value) -> None:
    if not mapping("identity", value):
        return
    concrete("identity.name", value.get("name"))
    concrete("identity.owner", value.get("owner"))
    concrete("identity.purpose", value.get("purpose"), min_words=4)
    string_list("identity.scope", value.get("scope"), 1)


def check_canvas(value) -> None:
    if not mapping("canvas", value):
        return
    hex_color("canvas.surface", value.get("surface"))
    hex_color("canvas.ink", value.get("ink"))
    if "dark_variant" not in value:
        fail("canvas.dark_variant", "required; state the two hex values or null for none")
        return
    dark = value["dark_variant"]
    if dark is None:
        return
    if mapping("canvas.dark_variant", dark):
        hex_color("canvas.dark_variant.surface", dark.get("surface"))
        hex_color("canvas.dark_variant.ink", dark.get("ink"))


def check_type_roles(value) -> None:
    if not mapping("type_roles", value):
        return
    for role in TYPE_ROLES:
        if role not in value:
            fail(f"type_roles.{role}", "required role is undeclared")
            continue
        entry = value[role]
        if not mapping(f"type_roles.{role}", entry):
            continue
        concrete(f"type_roles.{role}.family", entry.get("family"))
        concrete(f"type_roles.{role}.fallback", entry.get("fallback"))
        availability = entry.get("availability")
        if availability not in AVAILABILITY:
            fail(
                f"type_roles.{role}.availability",
                f"expected one of {sorted(AVAILABILITY)}, got {availability!r}",
            )


def check_semantic_color(value) -> None:
    if not mapping("semantic_color", value):
        return
    for role in SEMANTIC_ROLES:
        if role not in value:
            fail(f"semantic_color.{role}", "required role is undeclared")
            continue
        entry = value[role]
        if not mapping(f"semantic_color.{role}", entry):
            continue
        hex_color(f"semantic_color.{role}.hex", entry.get("hex"))
        string_list(f"semantic_color.{role}.redundancy", entry.get("redundancy"), 1)


def check_geometry(value) -> None:
    if not mapping("geometry", value):
        return
    whole_number("geometry.corner_radius_px", value.get("corner_radius_px"))
    whole_number("geometry.hairline_px", value.get("hairline_px"))
    whole_number("geometry.emphasis_rule_px", value.get("emphasis_rule_px"))
    whole_number("geometry.spacing_base_px", value.get("spacing_base_px"))
    concrete("geometry.elevation", value.get("elevation"))


def check_voice(value) -> None:
    if not mapping("voice", value):
        return
    concrete("voice.person", value.get("person"))
    concrete("voice.heading_case", value.get("heading_case"))
    register = value.get("register")
    if string_list("voice.register", register, 3) and len(register) != 3:
        fail("voice.register", f"expected exactly 3 adjectives, got {len(register)}")
    string_list("voice.refuses", value.get("refuses"), 1)


def check_posture(value) -> None:
    if not mapping("posture", value):
        return
    concrete("posture.density", value.get("density"))
    concrete("posture.motion", value.get("motion"))
    # How the work closes is structural, not tone. A single recommendation and a set of paths with
    # a stated lean produce different final surfaces from the same evidence, so the identity has to
    # say which one it hands over.
    concrete("posture.closing", value.get("closing"))


def check_evidence(value) -> None:
    if not mapping("evidence", value):
        return
    for key in ("unit", "period", "source", "uncertainty"):
        concrete(f"evidence.{key}", value.get(key))


def validate(declaration) -> list[str]:
    """Return the list of failures for one declaration object."""
    failures.clear()
    if not isinstance(declaration, dict):
        return [f"declaration: expected a JSON object, got {type(declaration).__name__}"]
    for field in REQUIRED_FIELDS:
        if field not in declaration:
            fail(field, "required field is undeclared")
    check_identity(declaration.get("identity"))
    check_canvas(declaration.get("canvas"))
    check_type_roles(declaration.get("type_roles"))
    check_semantic_color(declaration.get("semantic_color"))
    concrete("action_treatment", declaration.get("action_treatment"), min_words=4)
    check_geometry(declaration.get("geometry"))
    check_voice(declaration.get("voice"))
    string_list("exclusions", declaration.get("exclusions"), 5)
    check_posture(declaration.get("posture"))
    check_evidence(declaration.get("evidence"))
    return list(failures)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"FAIL: no declaration at {path}")
        return 1
    try:
        declaration = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"FAIL: {path} is not valid JSON: {error}")
        return 1
    problems = validate(declaration)
    if problems:
        for problem in problems:
            field = problem.split(":", 1)[0]
            example = example_for(field)
            print(f"FAIL: {problem}" + (f"\n      re-ask, e.g. {example}" if example else ""))
        print(
            f"\nBLOCKED: {len(problems)} field(s) are undeclared or non-concrete. "
            "Re-ask only these, with the example attached, then re-run. Do not begin design work."
        )
        return 1
    name = declaration["identity"]["name"]
    print(f"PASS: declaration for personal:{name} is complete across all 10 fields")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
