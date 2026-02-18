"""Build script for Phosphor Icons icon pack.

Extracts SVGs from the upstream zip archive and repackages them
into a standardized icons.zip format with variant prefixes.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from justmyresource_pack_tools.archive import ArchiveReader
from justmyresource_pack_tools.config import UpstreamConfig
from justmyresource_pack_tools.repack import ZipEntry


def extract(archive: ArchiveReader, config: UpstreamConfig) -> Iterator[ZipEntry]:
    """Extract icons from Phosphor Icons upstream archive.

    Phosphor archive structure (zip from GitHub):
        phosphor-icons-core-{tag}/
          assets/
            thin/
              arrow-right.svg
              house.svg
            light/
              arrow-right.svg
              ...
            regular/
              arrow-right.svg
              ...
            bold/
              arrow-right.svg
              ...
            fill/
              arrow-right.svg
              ...
            duotone/
              arrow-right.svg
              ...

    Output structure (multi-variant):
        thin/arrow-right.svg
        thin/house.svg
        light/arrow-right.svg
        regular/arrow-right.svg
        bold/arrow-right.svg
        fill/arrow-right.svg
        duotone/arrow-right.svg
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

        # Filter for paths matching */assets/{weight}/*.svg
        if "/assets/" not in member.name:
            continue

        if not member.name.endswith(".svg"):
            continue

        # Extract weight and filename from path
        # Example: "phosphor-icons-core-2.0.8/assets/regular/arrow-right.svg"
        # -> weight = "regular", filename = "arrow-right.svg"
        parts = member.name.split("/assets/")
        if len(parts) != 2:
            continue

        variant_path = parts[1]  # "regular/arrow-right.svg"
        path_parts = variant_path.split("/", 1)
        if len(path_parts) != 2:
            continue

        weight = path_parts[0]  # This is the variant name
        filename = path_parts[1]

        # Only include variants listed in config
        if weight not in allowed_variants:
            continue

        # Names are already kebab-case, no normalization needed
        # Multi-variant, so output preserves weight prefix
        zip_path = f"{weight}/{filename}"

        # Read file content
        with archive.extractfile(member) as f:
            content = f.read()

        yield ZipEntry(path=zip_path, content=content)

