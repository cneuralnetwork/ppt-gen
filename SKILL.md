---
name: ppt-gen
description: Art-direct, create, and revise polished PowerPoint decks through a mandatory localhost intake dashboard, prompt-aware prefill, style-locked raster image generation, editable slide authoring, and visual/package QA. Use for any explicit PPT Gen request involving PPT, PPTX, PowerPoint, pitch deck, lecture deck, academic presentation, quiz deck, keynote, workshop, presentation generation, or presentation revision.
---

# PPT Gen

Turn a presentation request into a confirmed brief, a coherent narrative, a style-locked set of generated visuals, and a verified editable PPTX.

## Set paths

Set these absolute paths before starting:

```text
PPT_GEN_SKILL_DIR=<directory containing this SKILL.md>
PPT_GEN_WORK_DIR=<writable per-deck working directory>
PPT_GEN_BRIEF=<PPT_GEN_WORK_DIR>/brief.json
PPT_GEN_PREFILL=<PPT_GEN_WORK_DIR>/prefill.json
```

Keep generated plans, prompts, renders, and QA evidence inside `PPT_GEN_WORK_DIR`. Put only the final PPTX at the user-requested destination.

## 1. Build the prefill

Read the complete request, conversation, attached text, source files, and reference-deck instructions before asking anything.

Create `PPT_GEN_PREFILL` as a partial object following [references/brief-schema.md](references/brief-schema.md). Infer only values supported by the request. Copy provided source content faithfully into `project.content`. Leave unknown values absent so the dashboard can distinguish an unanswered question from an inferred answer.

Never silently replace explicit user direction with a dashboard default.

## 2. Open the intake dashboard

Always open the dashboard whenever this skill is invoked, including for an edit or revision, even when every field can be prefilled. The dashboard is the confirmation gate, not a fallback questionnaire. For an edit, prefill the current deck's known content and style plus the requested change.

Run:

```text
python "$PPT_GEN_SKILL_DIR/scripts/intake_server.py" \
  --prefill "$PPT_GEN_PREFILL" \
  --result "$PPT_GEN_BRIEF" \
  --open
```

Keep the process running while the user reviews the form. If browser opening is unavailable, surface the printed localhost URL. Do not replace this dashboard with chat questions unless the server cannot run.

Wait for the user to press **Lock brief and continue**. Do not author slides before `PPT_GEN_BRIEF` exists.

Validate the result:

```text
python "$PPT_GEN_SKILL_DIR/scripts/validate_brief.py" "$PPT_GEN_BRIEF"
```

If the user changes the prompt while the dashboard is open, update the prefill and restart the intake rather than producing from stale choices.

## 3. Lock the communication and art direction

Read [references/deck-production.md](references/deck-production.md) and [references/image-direction.md](references/image-direction.md).

Write one communication job:

```text
By the end, [audience] should [outcome] because [central takeaway].
```

Create a cumulative narrative outline. Give each slide one job, one audience-facing claim, and one visual purpose. Do not expose planning language on slides.

Translate the confirmed style answers into a compact `style_lock` containing:

- visual medium and rendering technique;
- palette and contrast behavior;
- lighting, texture, and atmosphere;
- composition, camera, and negative-space rules;
- seriousness, energy, and era;
- exclusions that prevent generic or off-style imagery.

Repeat the same `style_lock` verbatim in every image-generation prompt. Change only the subject, framing, and slide-specific purpose.

## 4. Generate the visual system

Use the image-generation tool for every storytelling visual. Do not use image search, stock imagery, downloaded illustrations, icon packs, generated SVG, or programmatic drawings.

Generate raster files only: PNG, JPEG, or WebP. Use a unique visual for each slide unless a repeated background is an intentional part of the visual system.

For academic, scientific, technical, and data-heavy decks:

- generate precise, label-free diagram bases or scientific illustrations;
- request clear zones for editable labels and citations;
- add factual labels, values, equations, and arrows as editable PowerPoint content;
- never trust text or numbers rendered inside a generated image.

For playful, quiz, event, or youth-oriented decks, carry the chosen material, color, humor, and energy through every asset. Do not merely recolor a corporate deck.

User-supplied raster brand marks or essential photographs may be used only when the user explicitly selects them. Never fabricate a logo. Rasterize any required user-supplied SVG before placement, and do not embed the source SVG.

Create and validate a visual manifest as described in [references/image-direction.md](references/image-direction.md).

```text
python "$PPT_GEN_SKILL_DIR/scripts/validate_visual_manifest.py" \
  "$PPT_GEN_WORK_DIR/visual-manifest.json"
```

## 5. Author the PPTX

Use the installed presentation authoring workflow and `@oai/artifact-tool` from a JavaScript ES module. Load the workspace dependencies first. Do not use `python-pptx`.

Use native PowerPoint text for all audience-facing copy. Use simple native background fields, masks, and layout geometry only when they support the generated imagery. Do not substitute generic vector illustrations for missing generated assets.

Choose fonts from the confirmed typography direction and the fonts actually available in the environment. Prefer a characterful display face plus a quiet reading face when the style calls for it. Shorten copy or change layout before shrinking type.

Add a `[Sources]` block to speaker notes for every externally sourced claim and every non-user asset or reference. Keep generated-asset prompt provenance in the work directory.

## 6. Prove the result

Render every slide and inspect every slide at full size. Also inspect a montage for narrative rhythm and style consistency.

Fix all unintended overlap, clipping, wrapping, low contrast, broken crops, inconsistent margins, repeated visuals, unresolved placeholders, diagram-label mismatches, and off-style imagery.

Run the no-SVG package audit:

```text
python "$PPT_GEN_SKILL_DIR/scripts/audit_pptx.py" <final.pptx>
```

The audit must pass. Also run the presentation overflow test supplied by the installed presentation tooling.

Confirm that:

- every non-brand storytelling visual is an approved generated raster asset;
- the same style lock is evident across the complete deck;
- the selected font voice matches the seriousness and audience;
- factual diagrams remain accurate because labels and numbers are editable;
- every interactive or linked element requested by the user works;
- the final slide resolves the opening rather than ending on a generic thank-you.

Deliver only after the deck, renders, and package audit all agree.
