# Deck production

## Plan

1. Express the communication job in one sentence.
2. Choose a narrative arc appropriate to the job.
3. Draft a slide table with slide number, audience-facing takeaway title, essential evidence, and visual purpose.
4. Remove repeated beats. Prefer fewer stronger slides over a crowded deck.
5. Plan the closing slide as the resolution of the opening.

## Source

Use user-provided material as the primary source. Research only within the submitted research policy. Record each non-trivial claim and asset source in `source-notes.txt`, then add a `[Sources]` block to the relevant slide's speaker notes.

Never generate plausible-looking data. When evidence is missing, use a clearly marked placeholder or adjust the claim.

## Author

Follow the installed presentation toolchain and its required runtime setup. Build from a JavaScript ES module with `@oai/artifact-tool` and export one editable PPTX.

Use generated raster imagery as the visual layer. Keep titles, body copy, labels, equations, sources, and exact values native and editable. Use native shapes only for simple backgrounds, masks, highlights, and accurate diagram annotations.

Match the selected seriousness:

- academic decks favor disciplined hierarchy, evidence, and readable annotation;
- executive decks favor decisions, consequences, and sparse high-value evidence;
- workshops favor prompts, shared artifacts, and usable instructions;
- playful decks favor timing, surprise, and visual rhythm without sacrificing legibility.

## Verify

Render every slide. Inspect the deck once for narrative flow and every slide again at full size for craft.

Check:

- title and body fit;
- equal margins where intentional;
- text clearance from crops and custom silhouettes;
- label and connector accuracy;
- contrast and font consistency;
- unique, on-style generated imagery;
- source notes and final-slide resolution;
- no SVG media or SVG relationships in the PPTX package.

Fix the source and rerender after every discovered issue. A contact sheet alone is not sufficient proof.
