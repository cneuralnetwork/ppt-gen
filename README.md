# PPT Gen

`ppt-gen` is a Codex skill for producing art-directed, editable PowerPoint decks. It turns a prompt into a confirmed creative brief, opens a small localhost intake dashboard, locks one visual direction, generates style-specific raster imagery, authors the deck, and audits the finished PPTX.

## Install

### With npx

Install the skill globally for Codex:

```sh
npx --yes skills@latest add cneuralnetwork/ppt-gen \
  --global \
  --agent codex \
  --skill ppt-gen \
  --yes
```

The Skills CLI downloads the public GitHub repository and registers `ppt-gen` with Codex.

### With Git

Alternatively, clone the repository directly into the Codex skills directory:

```sh
git clone https://github.com/cneuralnetwork/ppt-gen.git ~/.codex/skills/ppt-gen
```

After installation, start a new Codex task so the available-skills list refreshes.

## Use

Mention the skill at the start of a Codex prompt:

```text
$ppt-gen Create a 10-slide academic presentation about real-time reinforcement learning for graduate students. Use a rigorous, restrained visual style and make the final slide resolve the opening research question.
```

You can provide a complete brief in the prompt:

```text
$ppt-gen

Create an 8-slide investor presentation for a seed-stage climate startup.

Audience: technical climate investors
Goal: secure follow-up diligence meetings
Content: use the attached market notes and traction spreadsheet
Style: editorial, optimistic, precise, natural-light photography
Format: 16:9
```

When the prompt already contains the audience, purpose, content, slide count, or visual direction, the dashboard prefills those answers. It only leaves genuinely unknown choices for review.

## What happens next

1. Codex extracts a partial brief from the prompt and supplied files.
2. A localhost dashboard opens with the known answers already filled in.
3. You review the choices and select **Lock brief and continue**.
4. The submitted brief becomes the binding narrative and visual direction.
5. Codex generates a unique raster visual system and builds the editable PPTX.
6. Every slide is rendered, inspected, corrected, and package-audited before delivery.

The dashboard is a mandatory confirmation gate, including for revisions. Normal users do not need to launch it manually.

## Production rules

- Storytelling visuals are generated specifically for the confirmed style.
- PPTX media must be PNG, JPEG, or WebP. SVG media and SVG relationships are rejected.
- Stock imagery, image-search assets, icon packs, and generic programmatic illustrations are not used.
- Factual labels, equations, numbers, and diagram annotations remain editable PowerPoint elements.
- Fonts are selected for the audience and seriousness, then checked against the installed fonts.
- Decks are authored with the supported JavaScript presentation toolchain, not `python-pptx`.
- Source notes, image prompts, assets, slide renders, and QA evidence are retained in the per-deck work directory.
- The last slide resolves the opening communication job instead of defaulting to a generic thank-you slide.

## Requirements

- Codex Desktop, Codex CLI, or the Codex IDE extension with skill support
- Python 3 for the local intake dashboard and validation scripts
- A Codex environment with image generation and PowerPoint authoring tools available
- A browser that can open a localhost URL

## Repository layout

```text
ppt-gen/
├── SKILL.md                       Core Codex workflow
├── AGENTS.md                      Presentation specialist contract
├── agents/openai.yaml             Skill display metadata
├── assets/dashboard/              Local intake dashboard
├── references/brief-schema.md     Submitted brief contract
├── references/deck-production.md  Narrative and production guidance
├── references/image-direction.md  Visual prompt and manifest guidance
└── scripts/
    ├── intake_server.py           Dashboard server and result writer
    ├── validate_brief.py          Brief validator
    ├── validate_visual_manifest.py
    └── audit_pptx.py              No-SVG package audit
```

## Development checks

Validate a submitted brief:

```sh
python scripts/validate_brief.py path/to/brief.json
```

Validate a generated-image manifest:

```sh
python scripts/validate_visual_manifest.py path/to/visual-manifest.json
```

Audit a finished deck for forbidden SVG content:

```sh
python scripts/audit_pptx.py path/to/final.pptx
```

The public source is available at [github.com/cneuralnetwork/ppt-gen](https://github.com/cneuralnetwork/ppt-gen).
