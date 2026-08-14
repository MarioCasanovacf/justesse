#!/usr/bin/env python3
"""Emit design tokens from a validated profile declaration, so declaring is building.

    python3 tools/declaration2tokens.py declaration.json              # CSS custom properties
    python3 tools/declaration2tokens.py declaration.json --json       # flat JSON
    python3 tools/declaration2tokens.py declaration.json -o tokens.css

The gap this closes: a declaration passes the gate and then someone transcribes its values into
CSS by hand, and the transcription is where drift creeps in — the drift `diff_specimens.py` would
catch later. Emitting the tokens mechanically removes the transcription step.

The gate composes: an incomplete or non-concrete declaration is refused here exactly as
`harness/validate_profile.py` refuses it, field by field. Nothing is emitted from a declaration
that could not be designed against.

Tokens are namespaced `--j-*` so they never collide with a project's own custom properties. A
surface consumes them by reference (`--surface: var(--j-surface)`), keeping its derived values —
panel tints, hairline colors mixed from the canvas — outside the declaration's authority, where
they belong.
"""

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness"))
import validate_profile  # noqa: E402


def font_stack(role):
    family = role["family"]
    quoted = f'"{family}"' if " " in family else family
    return f"{quoted}, {role['fallback']}"


def tokens_from(declaration):
    """Flat token dict from a declaration already known to be complete."""
    canvas = declaration["canvas"]
    semantic = declaration["semantic_color"]
    geometry = declaration["geometry"]
    tokens = {
        "j-surface": canvas["surface"],
        "j-ink": canvas["ink"],
        "j-positive": semantic["positive"]["hex"],
        "j-warning": semantic["warning"]["hex"],
        "j-negative": semantic["negative"]["hex"],
        "j-neutral": semantic["neutral"]["hex"],
        "j-structure": semantic["structure"]["hex"],
        "j-font-display": font_stack(declaration["type_roles"]["display"]),
        "j-font-prose": font_stack(declaration["type_roles"]["prose"]),
        "j-font-ui": font_stack(declaration["type_roles"]["ui"]),
        "j-font-data": font_stack(declaration["type_roles"]["data"]),
        "j-radius": f"{geometry['corner_radius_px']}px",
        "j-hairline": f"{geometry['hairline_px']}px",
        "j-emphasis-rule": f"{geometry['emphasis_rule_px']}px",
        "j-space": f"{geometry['spacing_base_px']}px",
    }
    dark = canvas.get("dark_variant")
    if dark:
        tokens["j-dark-surface"] = dark["surface"]
        tokens["j-dark-ink"] = dark["ink"]
    return tokens


def as_css(tokens, name, digest):
    lines = [
        ":root {",
        f"  /* personal:{name} — emitted from the validated declaration (sha256 {digest[:16]}). */",
        "  /* Do not hand-edit; re-declare and re-emit. Derived values stay outside this block. */",
    ]
    lines += [f"  --{key}: {value};" for key, value in tokens.items() if not key.startswith("j-dark-")]
    lines.append("}")
    if "j-dark-surface" in tokens:
        lines += [
            "@media (prefers-color-scheme: dark) {",
            "  :root {",
            f"    --j-surface: {tokens['j-dark-surface']};",
            f"    --j-ink: {tokens['j-dark-ink']};",
            "  }",
            "}",
        ]
    return "\n".join(lines) + "\n"


def main(argv):
    flags = {arg for arg in argv[1:] if arg.startswith("--")}
    positional = [arg for arg in argv[1:] if not arg.startswith("--")]
    out_path = None
    if "-o" in positional:
        index = positional.index("-o")
        try:
            out_path = Path(positional[index + 1])
        except IndexError:
            print(__doc__.strip())
            return 2
        positional = positional[:index] + positional[index + 2 :]
    if len(positional) != 1 or flags - {"--json"}:
        print(__doc__.strip())
        return 2
    path = Path(positional[0])
    if not path.is_file():
        print(f"FAIL: no declaration at {path}")
        return 1
    raw = path.read_bytes()
    try:
        declaration = json.loads(raw)
    except json.JSONDecodeError as error:
        print(f"FAIL: {path} is not valid JSON: {error}")
        return 1
    problems = validate_profile.validate(declaration)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        print("\nBLOCKED: tokens are only emitted from a complete declaration. Fix the fields above.")
        return 1
    tokens = tokens_from(declaration)
    digest = hashlib.sha256(raw).hexdigest()
    name = declaration["identity"]["name"]
    if "--json" in flags:
        payload = {"profile": name, "declaration_sha256": digest, "tokens": tokens}
        output = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    else:
        output = as_css(tokens, name, digest)
    if out_path:
        out_path.write_text(output, encoding="utf-8")
        print(f"PASS: {len(tokens)} tokens for personal:{name} -> {out_path}")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
