# Image direction

## Build one style lock

Condense the confirmed style into 60 to 120 words. State the medium, palette, texture, lighting, composition, depth, seriousness, and exclusions. Keep it concrete enough that two independently generated images belong to the same deck.

Attach the exact same style-lock text to every prompt. Do not weaken it to keywords.

## Direct each slide asset

Each prompt must include:

1. the slide's communication job;
2. the specific subject or relationship to depict;
3. the target aspect ratio and likely crop;
4. where negative space is needed for native slide text;
5. the locked style paragraph;
6. exclusions such as no embedded words, no logos, no watermark, no UI chrome, and no generic gradients.

Create diagrams without embedded labels. Ask for clear visual anchors, distinct regions, and uncluttered space where PowerPoint labels will sit.

## Style translations

- **Academic:** precise scientific editorial illustration, disciplined hierarchy, restrained color, quiet paper or laboratory material, generous label zones, no decorative pseudo-data.
- **Executive:** composed editorial imagery, real-world stakes, restrained materials, directional light, credible scale, no generic business handshakes or dashboard props.
- **Playful quiz:** tactile paper construction, surprising objects, legible silhouettes, deliberate humor, energetic framing, no corporate card layout.
- **Product launch:** show the real product artifact when available; otherwise use an authored conceptual scene tied to the product's actual function, not a fake app window.
- **Data analyst:** use image generation for the atmospheric or explanatory layer; keep exact data in editable native charts, labels, and tables.

## Visual manifest

Write `visual-manifest.json` in the work directory:

```json
{
  "style_lock": "exact repeated style paragraph",
  "assets": [
    {
      "slide": 2,
      "purpose": "what this visual helps the audience understand",
      "prompt": "full image-generation prompt including the style lock",
      "path": "/absolute/path/to/generated.png",
      "generator": "image_gen",
      "approved": true
    }
  ]
}
```

Reject an asset when its prompt omits the style lock, its file is not raster, it contains unreadable generated text, it contradicts the slide's claim, or it drifts from the palette and material.

Do not reuse one generated image for different claims. A repeated full-deck background is the only normal exception.
