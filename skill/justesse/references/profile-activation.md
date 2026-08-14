# Profile activation

A profile is an explicit, named identity layered onto the selected operating mode. It is never a
default, never inherited, and never bundled with this skill. This skill ships the mechanism; it
ships no profile.

Activate a profile only when the request or project instructions contain the exact flag
`personal:<name>`, where `<name>` identifies a declared profile the requester owns or is authorized
to apply. Without that exact flag, keep the visual language, voice, palette, materiality, geometry,
and surface color brand-neutral.

## Do not infer activation

Do not activate from a person's name, an artifact being personal, an author byline, a stylistic
reference, a prior conversation, an example in this skill, or the presence of this skill. A profile
flag naming someone who has not declared a profile is not an instruction to reconstruct one from
their public work, their repository, or your impression of their taste.

## Declaration precedes application

Activating the flag does not grant a visual system. It opens a required declaration. Read
[profile-declaration.md](profile-declaration.md) and obtain concrete answers to every required
field before making a single design decision under the profile. An activated flag with an
incomplete declaration is a blocked task, not a license to improvise, and not a reason to fall back
on brand-neutral defaults while claiming the profile is active.

Never populate an unanswered field by inference, by carrying a value from another profile, by
reusing a value that appears in this skill's own examples or harness fixtures, or by proposing a
value and treating silence as approval. An unanswered field is unanswered.

## Conflicts and disclosure

If the profile conflicts with a supplied brand, design system, or product contract, preserve the
contract and ask one focused question rather than blending identities.

State both the primary mode and `profile: personal:<name>` in the design read, and name the
declaration record the profile resolved from. Before delivery, verify that profile-specific choices
appear only in flagged outputs, and that an equivalent no-flag request contains no identity, token
set, signature type stack, or materiality assumption belonging to the profile.
