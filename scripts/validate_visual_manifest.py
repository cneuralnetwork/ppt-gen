#!/usr/bin/env python3
"""Verify style-lock reuse and raster provenance for generated deck visuals."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


RASTER_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def is_raster(path: Path) -> bool:
    try:
        head = path.read_bytes()[:16]
    except OSError:
        return False
    return (
        head.startswith(b"\x89PNG\r\n\x1a\n")
        or head.startswith(b"\xff\xd8\xff")
        or (head.startswith(b"RIFF") and head[8:12] == b"WEBP")
    )


def validate(data: Any, *, require_files: bool) -> list[str]:
    if not isinstance(data, dict):
        return ["manifest must be a JSON object"]
    errors: list[str] = []
    style_lock = str(data.get("style_lock", "")).strip()
    assets = data.get("assets")
    if len(style_lock) < 40:
        errors.append("style_lock must be a concrete paragraph of at least 40 characters")
    if not isinstance(assets, list) or not assets:
        errors.append("assets must be a non-empty array")
        return errors

    slides: set[int] = set()
    paths: set[Path] = set()
    for index, asset in enumerate(assets, start=1):
        prefix = f"assets[{index - 1}]"
        if not isinstance(asset, dict):
            errors.append(f"{prefix} must be an object")
            continue
        slide = asset.get("slide")
        if not isinstance(slide, int) or slide < 1:
            errors.append(f"{prefix}.slide must be a positive integer")
        elif slide in slides:
            errors.append(f"{prefix}.slide duplicates slide {slide}; use a unique storytelling visual per slide")
        else:
            slides.add(slide)

        purpose = str(asset.get("purpose", "")).strip()
        prompt = str(asset.get("prompt", ""))
        generator = asset.get("generator")
        approved = asset.get("approved")
        raw_path = str(asset.get("path", "")).strip()
        path = Path(raw_path) if raw_path else Path()

        if not purpose:
            errors.append(f"{prefix}.purpose is required")
        if style_lock and style_lock not in prompt:
            errors.append(f"{prefix}.prompt does not contain the exact style_lock")
        if generator != "image_gen":
            errors.append(f"{prefix}.generator must be image_gen")
        if approved is not True:
            errors.append(f"{prefix}.approved must be true")
        if not raw_path or not path.is_absolute():
            errors.append(f"{prefix}.path must be absolute")
            continue
        if path.suffix.lower() not in RASTER_EXTENSIONS:
            errors.append(f"{prefix}.path must end in PNG, JPEG, or WebP")
        if path in paths:
            errors.append(f"{prefix}.path reuses a visual already assigned to another slide")
        paths.add(path)
        if require_files:
            if not path.is_file():
                errors.append(f"{prefix}.path does not exist: {path}")
            elif not is_raster(path):
                errors.append(f"{prefix}.path is not valid PNG, JPEG, or WebP data")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--allow-missing", action="store_true", help="Validate a planning manifest before generation")
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"VISUAL_MANIFEST_INVALID: {exc}", file=sys.stderr)
        return 1
    errors = validate(data, require_files=not args.allow_missing)
    if errors:
        for error in errors:
            print(f"VISUAL_MANIFEST_INVALID: {error}", file=sys.stderr)
        return 1
    print(f"VISUAL_MANIFEST_VALID assets={len(data['assets'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
