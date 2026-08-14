# Finishing

The last pass, and only the last pass. Load this after the interface-quality checks hold: finishing
operates below the threshold where most viewers can name what changed, and at that depth it can
only refine a surface that already works. Finishing never buys forgiveness for a broken hierarchy,
a dishonest chart, or a missing state, and it is bounded by the same batched verification rounds as
everything else. On a profile run, the declaration's canvas, geometry, and type values are the
authority these refinements serve.

## Surface temperature is a decision

A warm paper white and a cool one are different design decisions, not shades of the same default.
Choose the surface's temperature deliberately, state it as a value, and hold it constant across
every surface of one system; a deck whose slides drift between warm and cool paper was assembled,
not composed. The same applies to ink: foreground text on a light surface reads better slightly
off full black, tinted toward the surface's own temperature, and secondary text on a colored
surface derives from that hue rather than defaulting to a neutral gray. Pure maximum-contrast
pairings vibrate; chosen near-extremes compose.

## Optical outranks mechanical

Mathematically centered is not visually centered. Where the platform allows it, trim text boxes to
the cap height and baseline so labels center on the letters rather than on the font's built-in
leading; the CSS `text-box-trim` mechanism does this natively in current Chromium and Safari
engines, and engines that do not know it simply ignore it, which makes it a safe progressive
enhancement. Where trimming is unavailable, compensate the padding by hand and record the
compensation. Hang punctuation and bullets into the margin so the text edge reads straight; native
support is narrow, so treat cross-engine hanging as an enhancement measured from font metrics, not
a requirement. Round positions to the device grid so hairlines stay crisp instead of straddling
pixels.

## Emptiness has to be assigned

A sparse composition fails in a specific way: not too little content, but content spread at roughly
equal distances so nothing groups. Three elements separated by three similar gaps give the eye no
structure, and undifferentiated space reads as absence rather than air. The gap between a heading
and the sentence that supports it is not the same measurement as the gap between that pair and the
next idea; when they are set to the same number, the reader is told those relationships are equal,
which is a claim the design did not mean to make.

Assign the emptiness instead. Bind related elements into one block at a distance that reads as
belonging. Anchor the element that carries the weight — a conclusion, a recommendation, a headline
figure — to a baseline held constant across the surfaces of one system, so a reader moving between
them finds it in the same place. What is left over becomes a single deliberate void between two
anchored masses, which composes, rather than several similar voids, which drift. On a fixed canvas
this is easy to check numerically: measure each surface's top gap and bottom gap, and treat a
sparse surface whose empty space collects at one end as unfinished.

## Letterforms at small sizes

- Letterspace runs of capitals and small capitals slightly; their forms were drawn to stand apart.
  Do not letterspace lowercase text, whose forms were drawn to touch their neighbors' rhythm.
- Use true small capitals only when the typeface actually carries them; synthesized small caps are
  scaled-down capitals with the wrong weight and are a visible downgrade, not a refinement.
- Keep numeral behavior deliberate: tabular lining figures where numbers align in columns, as the
  data-visualization reference already requires, and text figures only as a considered choice in
  running prose.
- Read the rag of unjustified text at real widths. A right edge that staircases, echoes a shape, or
  breaks a proper name awkwardly is fixed with soft breaks and hyphenation policy, not ignored.

## The watermark principle

A finished system may carry one signature move pitched below conscious notice: a surface texture
only visible at an angle, a numeral set chosen against expectation, a rule weight that shifts by
context, a corner treatment reserved for one element class. One such move rewards the reader who
looks closely. Two compete, and a system whose every element whispers a different signature is
shouting. Name the move in the design read so it is a decision on the record, not an accident a
reviewer has to reverse-engineer.

## Judging near-identical work

When two candidate surfaces look the same, the judgment lives in differences most viewers cannot
name, and asserting them by eye is not evidence. This repository ships a comparison instrument,
`tools/diff_specimens.py`, that reads the object inventories of two specimens and names their
deltas: color differences graded perceptually, geometry differences to the pixel, and type
differences by size and family. It also renders the verdict eyes cannot be trusted to give, in
either direction: that two specimens differ only sub-perceptually, or that two supposedly distinct
identities produced the same design with different words on it. Distinct briefs or distinct
declared profiles must produce measurably distinct surfaces; convergence to one look, however
refined, is a failure of the system, not proof of its taste.
