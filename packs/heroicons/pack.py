"""Build script for Heroicons icon pack.

Extracts SVGs from the upstream tar.gz archive and repackages them
into a standardized icons.zip format with variant prefixes.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from justmyresource_pack_tools.archive import ArchiveReader
from justmyresource_pack_tools.config import UpstreamConfig
from justmyresource_pack_tools.repack import ZipEntry


def extract(archive: ArchiveReader, config: UpstreamConfig) -> Iterator[ZipEntry]:
    """Extract icons from Heroicons upstream archive.

    Heroicons archive structure (tar.gz from GitHub):
        heroicons-{tag}/
          optimized/
            24/
              outline/
                arrow-right.svg
                house.svg
              solid/
                arrow-right.svg
                house.svg
            20/
              solid/
                arrow-right.svg
                ...
            16/
              solid/
                arrow-right.svg
                ...

    Output structure (multi-variant):
        24/outline/arrow-right.svg
        24/outline/house.svg
        24/solid/arrow-right.svg
        24/solid/house.svg
        20/solid/arrow-right.svg
        16/solid/arrow-right.svg
        ...

    Args:
        archive: Archive reader for the upstream archive.
        config: Upstream configuration loaded from upstream.toml.

    Yields:
        ZipEntry objects with normalized paths and content.
    """
    # Get allowed variants from config
    allowed_variants = set(config.pack.variants)

    for member in archive.getmembers():
        # Only process SVG files
        if not member.isfile():
            continue

        # Filter for paths matching */optimized/{size}/{style}/*.svg
        if "/optimized/" not in member.name:
            continue

        if not member.name.endswith(".svg"):
            continue

        # Extract size, style, and filename from path
        # Example: "heroicons-2.2.0/optimized/24/outline/arrow-right.svg"
        # -> size = "24", style = "outline", filename = "arrow-right.svg"
        parts = member.name.split("/optimized/")
        if len(parts) != 2:
            continue

        variant_path = parts[1]  # "24/outline/arrow-right.svg"
        path_parts = variant_path.split("/")
        if len(path_parts) != 3:
            continue

        size = path_parts[0]
        style = path_parts[1]
        filename = path_parts[2]

        # Construct variant as "{size}/{style}"
        variant = f"{size}/{style}"

        # Only include variants listed in config
        if variant not in allowed_variants:
            continue

        # Names are already kebab-case, no normalization needed
        # Multi-variant, so output preserves variant prefix
        zip_path = f"{variant}/{filename}"

        # Read file content
        with archive.extractfile(member) as f:
            content = f.read()

        yield ZipEntry(path=zip_path, content=content)

