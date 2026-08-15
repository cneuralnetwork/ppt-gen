# Confirmed brief schema

Use this structure for `prefill.json` and `brief.json`. Prefill files may omit unknown fields. Submitted briefs must contain all required fields.

```json
{
  "schema_version": 1,
  "project": {
    "title": "required",
    "topic": "required",
    "content": "required source material or content brief",
    "audience": "required",
    "purpose": "educate | persuade | recommend | sell | facilitate | celebrate",
    "audience_outcome": "required",
    "language": "English",
    "presenter": "",
    "context": ""
  },
  "delivery": {
    "slide_count": 10,
    "duration_minutes": 12,
    "aspect_ratio": "16:9",
    "speaker_notes": true,
    "citations": "speaker-notes | visible-footnotes | both | none",
    "output_name": "presentation.pptx"
  },
  "style": {
    "archetype": "academic | executive | editorial | workshop | playful-quiz | product-launch | data-analyst | custom",
    "energy": "restrained | balanced | high",
    "visual_medium": "scientific-illustration | editorial-photography | tactile-collage | paper-cut | painterly | dimensional | data-led | custom",
    "palette": "mineral-ink | forest-clay | oxblood-paper | monochrome | sunlit-primary | custom",
    "typography": "scholarly-humanist | editorial | executive | expressive | technical | custom",
    "density": "spacious | balanced | dense-reference",
    "imagery_frequency": "every-slide | frequent | selective",
    "custom_direction": "",
    "reference_notes": ""
  },
  "assets": {
    "reference_deck": "",
    "brand_assets": [],
    "source_files": []
  },
  "content_policy": {
    "research": "provided-only | authoritative-only | current-web-allowed",
    "factuality": "source-required",
    "visuals": "imagegen-raster-only",
    "allow_svg": false
  }
}
```

Normalize `output_name` to a filename ending in `.pptx`. Keep paths as strings; do not read or upload a path until it is needed for the deck.
