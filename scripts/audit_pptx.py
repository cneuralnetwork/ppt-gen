#!/usr/bin/env python3
"""Fail when a PPTX package contains SVG media or SVG references."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path


SVG_TOKEN = re.compile(rb"(?:image/svg\+xml|\.svg(?:[\"'?#<]|$))", re.IGNORECASE)
RASTER_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".tif", ".tiff", ".bmp"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    args = parser.parse_args()

    if not args.pptx.is_file():
        print(f"PPTX_AUDIT_FAILED: file not found: {args.pptx}", file=sys.stderr)
        return 1

    failures: list[str] = []
    media: list[str] = []
    try:
        with zipfile.ZipFile(args.pptx) as archive:
            for info in archive.infolist():
                lower = info.filename.lower()
                if lower.endswith(".svg"):
                    failures.append(f"embedded SVG file: {info.filename}")
                if lower.startswith("ppt/media/") and not info.is_dir():
                    media.append(info.filename)
                    suffix = Path(lower).suffix
                    if suffix and suffix not in RASTER_EXTENSIONS:
                        failures.append(f"non-raster media extension: {info.filename}")
                if lower.endswith((".xml", ".rels")):
                    payload = archive.read(info)
                    if SVG_TOKEN.search(payload):
                        failures.append(f"SVG reference: {info.filename}")
    except zipfile.BadZipFile:
        print("PPTX_AUDIT_FAILED: file is not a valid ZIP/PPTX package", file=sys.stderr)
        return 1

    if failures:
        for failure in sorted(set(failures)):
            print(f"PPTX_AUDIT_FAILED: {failure}", file=sys.stderr)
        return 1

    print(f"PPTX_AUDIT_PASSED media_files={len(media)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
