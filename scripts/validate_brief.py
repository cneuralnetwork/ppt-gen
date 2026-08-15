#!/usr/bin/env python3
"""Normalize and validate PPT Gen intake briefs without third-party packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_BRIEF: dict[str, Any] = {
    "schema_version": 1,
    "project": {
        "title": "",
        "topic": "",
        "content": "",
        "audience": "",
        "purpose": "educate",
        "audience_outcome": "",
        "language": "English",
        "presenter": "",
        "context": "",
    },
    "delivery": {
        "slide_count": 10,
        "duration_minutes": 12,
        "aspect_ratio": "16:9",
        "speaker_notes": True,
        "citations": "speaker-notes",
        "output_name": "presentation.pptx",
    },
    "style": {
        "archetype": "editorial",
        "energy": "balanced",
        "visual_medium": "editorial-photography",
        "palette": "forest-clay",
        "typography": "editorial",
        "density": "balanced",
        "imagery_frequency": "frequent",
        "custom_direction": "",
        "reference_notes": "",
    },
    "assets": {"reference_deck": "", "brand_assets": [], "source_files": []},
    "content_policy": {
        "research": "authoritative-only",
        "factuality": "source-required",
        "visuals": "imagegen-raster-only",
        "allow_svg": False,
    },
}


CHOICES = {
    "project.purpose": {"educate", "persuade", "recommend", "sell", "facilitate", "celebrate"},
    "delivery.aspect_ratio": {"16:9", "4:3"},
    "delivery.citations": {"speaker-notes", "visible-footnotes", "both", "none"},
    "style.archetype": {"academic", "executive", "editorial", "workshop", "playful-quiz", "product-launch", "data-analyst", "custom"},
    "style.energy": {"restrained", "balanced", "high"},
    "style.visual_medium": {"scientific-illustration", "editorial-photography", "tactile-collage", "paper-cut", "painterly", "dimensional", "data-led", "custom"},
    "style.palette": {"mineral-ink", "forest-clay", "oxblood-paper", "monochrome", "sunlit-primary", "custom"},
    "style.typography": {"scholarly-humanist", "editorial", "executive", "expressive", "technical", "custom"},
    "style.density": {"spacious", "balanced", "dense-reference"},
    "style.imagery_frequency": {"every-slide", "frequent", "selective"},
    "content_policy.research": {"provided-only", "authoritative-only", "current-web-allowed"},
}


def merge_brief(base: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    """Deep-merge known nested dictionaries while retaining user fields."""
    result = deepcopy(base)
    for key, value in incoming.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge_brief(result[key], value)
        else:
            result[key] = value
    return result


def get_path(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def normalize_brief(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("The brief must be a JSON object.")
    brief = merge_brief(DEFAULT_BRIEF, data)

    for section in ("project", "delivery", "style", "assets", "content_policy"):
        if not isinstance(brief.get(section), dict):
            raise ValueError(f"{section} must be an object.")

    project = brief["project"]
    delivery = brief["delivery"]
    assets = brief["assets"]

    for field in ("title", "topic", "content", "audience", "audience_outcome", "language", "presenter", "context"):
        project[field] = str(project.get(field, "")).strip()

    for field in ("custom_direction", "reference_notes"):
        brief["style"][field] = str(brief["style"].get(field, "")).strip()

    delivery["slide_count"] = int(delivery["slide_count"])
    delivery["duration_minutes"] = int(delivery["duration_minutes"])
    delivery["speaker_notes"] = bool(delivery["speaker_notes"])

    output_name = Path(str(delivery.get("output_name") or "presentation.pptx")).name
    output_name = re.sub(r"[^A-Za-z0-9._-]+", "-", output_name).strip("-.") or "presentation.pptx"
    if not output_name.lower().endswith(".pptx"):
        output_name += ".pptx"
    delivery["output_name"] = output_name

    for field in ("brand_assets", "source_files"):
        value = assets.get(field, [])
        if not isinstance(value, list):
            raise ValueError(f"assets.{field} must be an array.")
        assets[field] = [str(item).strip() for item in value if str(item).strip()]
    assets["reference_deck"] = str(assets.get("reference_deck", "")).strip()

    brief["schema_version"] = 1
    brief["content_policy"]["factuality"] = "source-required"
    brief["content_policy"]["visuals"] = "imagegen-raster-only"
    brief["content_policy"]["allow_svg"] = False
    return brief


def validate_brief(brief: dict[str, Any], *, final: bool = True) -> list[str]:
    errors: list[str] = []
    if final:
        for path in (
            "project.title",
            "project.topic",
            "project.content",
            "project.audience",
            "project.audience_outcome",
        ):
            if not str(get_path(brief, path) or "").strip():
                errors.append(f"{path} is required")

    for path, options in CHOICES.items():
        value = get_path(brief, path)
        if value not in options:
            errors.append(f"{path} must be one of: {', '.join(sorted(options))}")

    slide_count = get_path(brief, "delivery.slide_count")
    duration = get_path(brief, "delivery.duration_minutes")
    if not isinstance(slide_count, int) or not 3 <= slide_count <= 60:
        errors.append("delivery.slide_count must be between 3 and 60")
    if not isinstance(duration, int) or not 1 <= duration <= 240:
        errors.append("delivery.duration_minutes must be between 1 and 240")
    if get_path(brief, "content_policy.allow_svg") is not False:
        errors.append("content_policy.allow_svg must be false")
    if get_path(brief, "content_policy.visuals") != "imagegen-raster-only":
        errors.append("content_policy.visuals must be imagegen-raster-only")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path)
    parser.add_argument("--normalize", type=Path, help="Write normalized JSON to this path")
    parser.add_argument("--partial", action="store_true", help="Allow required final fields to be empty")
    args = parser.parse_args()

    try:
        data = json.loads(args.brief.read_text(encoding="utf-8"))
        brief = normalize_brief(data)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"BRIEF_INVALID: {exc}", file=sys.stderr)
        return 1

    errors = validate_brief(brief, final=not args.partial)
    if errors:
        for error in errors:
            print(f"BRIEF_INVALID: {error}", file=sys.stderr)
        return 1

    if args.normalize:
        args.normalize.parent.mkdir(parents=True, exist_ok=True)
        args.normalize.write_text(json.dumps(brief, indent=2) + "\n", encoding="utf-8")
    print("BRIEF_VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
