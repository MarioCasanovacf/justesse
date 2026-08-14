#!/usr/bin/env python3
"""Deterministic structural validator for the benchmark contract and fixture.

Checks internal arithmetic and structural consistency of contract.json and fixture.json in this
directory: weekly rows sum to the recorded totals, negative-feedback driver counts sum to the
negative total, the fixture freezes exactly eight weeks bounded by the declared period, exactly
four bounded derived claims and four frozen surface copy payloads exist, the synthetic-data
disclosure is present, and the activation, semantic-map, surface-brief, hard-gate, and
rubric-weight structures declared in contract.json are internally coherent.

Contributed 2026-08-12 from the operator's harness epic (T-318..T-329, killed as duplicate; PR-014).
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
fixture = json.loads((ROOT / "fixture.json").read_text(encoding="utf-8"))
checks: list[tuple[str, bool]] = []


def check(name: str, condition: bool) -> None:
    checks.append((name, bool(condition)))


check("synthetic disclosure", fixture["status"] == "synthetic_benchmark_data" and "Synthetic" in fixture["disclosure"])
check("eight frozen weeks", len(fixture["weekly_feedback"]) == 8)
check("period matches first week", fixture["weekly_feedback"][0]["week"] == fixture["period"]["start"])
check("period matches last week", fixture["weekly_feedback"][-1]["week"] == fixture["period"]["end"])
positive = sum(row["positive"] for row in fixture["weekly_feedback"])
neutral = sum(row["neutral"] for row in fixture["weekly_feedback"])
negative = sum(row["negative"] for row in fixture["weekly_feedback"])
check("positive total", positive == fixture["totals"]["positive"])
check("neutral total", neutral == fixture["totals"]["neutral"])
check("negative total", negative == fixture["totals"]["negative"])
check("grand total", positive + neutral + negative == fixture["totals"]["all"])
check("driver total", sum(row["count"] for row in fixture["negative_feedback_drivers"]) == negative)
check("four bounded claims", len(fixture["derived_claims_allowed"]) == 4)
check("four frozen copy payloads", set(fixture["copy_payloads"]) == {"dashboard", "decision_memo", "personal_landing", "case_study_report"})
check("five frozen slide payloads", len(fixture["copy_payloads"]["decision_memo"]["slides"]) == 5)
check("surface copy is nonempty", all(all(isinstance(value, (str, list)) and bool(value) for value in payload.values()) for payload in fixture["copy_payloads"].values()))
check("activation flag", contract["activation"]["flag"] == "personal:<name>")
check("no bundled profile", contract["activation"]["ships_bundled_profile"] is False)
check("declaration required", contract["activation"]["declaration_required"] is True)
check("ten declaration fields", len(contract["activation"]["declaration_fields"]) == 10)
check("declaration fields are unique", len(set(contract["activation"]["declaration_fields"])) == 10)
check("flagged variant requires declaration", "declaration" in contract["variants"]["B"])
check("declaration recorded in provenance", any("declaration" in field for field in contract["control"]["required_provenance"]))
check("negative control", contract["activation"]["negative_control_required"] and "B_no_flag" in contract["variants"])
check("three variants", set(contract["variants"]) == {"A", "B", "B_no_flag"})
check("four surfaces", set(contract["surface_briefs"]) == {"dashboard", "decision_memo", "personal_landing", "case_study_report"})
check("five-slide memo", len(contract["surface_briefs"]["decision_memo"]["slides"]) == 5)
check("slide aspect ratio", contract["surface_briefs"]["decision_memo"]["slide_size"]["aspect_ratio"] == "16:9")
check("slide inches", contract["surface_briefs"]["decision_memo"]["slide_size"]["width_inches"] == 13.333 and contract["surface_briefs"]["decision_memo"]["slide_size"]["height_inches"] == 7.5)
check("render dimensions", contract["surface_briefs"]["decision_memo"]["render_size_pixels"] == {"width": 1600, "height": 900})
check("semantic roles", set(contract["semantic_map"]) == {"positive_success", "warning", "negative_critical", "neutral", "structure_reference_total"})
check("every semantic role sources from the declaration", all(
    item["source"].startswith("declaration.semantic_color.") for item in contract["semantic_map"].values()
))
check("semantic sources are distinct", len({item["source"] for item in contract["semantic_map"].values()}) == 5)
check("semantic map carries no literal values", not any(
    "#" in json.dumps(item) for item in contract["semantic_map"].values()
))
check("every semantic role has redundancy", all(len(item["redundancy"]) >= 2 for item in contract["semantic_map"].values()))
memo_brief = contract["surface_briefs"]["decision_memo"]
canvas = memo_brief["canvas_pixels"]
check("canvas is 16:9", canvas["width"] * 9 == canvas["height"] * 16)
check("canvas maps to the slide frame at 96 px per inch", (
    round(memo_brief["slide_size"]["width_inches"] * 96) == canvas["width"]
    and round(memo_brief["slide_size"]["height_inches"] * 96) == canvas["height"]
))
check("memo requires native editable objects", "every element a native editable object" in memo_brief["requirements"])
check("memo forbids rasterized regions", "no rasterized region" in memo_brief["requirements"])
check("seven profile invariants", len(contract["profile_invariants_when_flagged"]) == 7)
check("invariants trace to the declaration", any(
    "declaration" in invariant for invariant in contract["profile_invariants_when_flagged"]
))
check("seven hard gates", len(contract["hard_gates"]) == 7)
check("promotion delta", contract["automated_promotion"]["minimum_total_improvement_points"] == 15)
check("no surface regression", contract["automated_promotion"]["surface_regressions_allowed"] == 0)
check("human gate retained", "profile owner" in contract["human_gate"] and "publish" in contract["human_gate"])
check("seven rubric dimensions", len(contract["rubric_weights"]) == 7)
check("rubric scores profile fidelity", "structural_profile_fidelity" in contract["rubric_weights"])
check("rubric totals 100", sum(contract["rubric_weights"].values()) == 100)
check("contract ships no literal design values", "#" not in json.dumps(contract))

failed = [name for name, ok in checks if not ok]
if failed:
    for name in failed:
        print(f"FAIL: {name}")
    raise SystemExit(f"FAILED {len(checks) - len(failed)}/{len(checks)}")

print(f"PASS {len(checks)}/{len(checks)} named assertions")
