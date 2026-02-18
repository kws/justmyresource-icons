"""Build script for Font Awesome icon pack.

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
    """Extract icons from Font Awesome upstream archive.

    Font Awesome archive structure (zip from GitHub releases):
        fontawesome-free-{tag}-web/
          svgs/
            solid/
              arrow-right.svg
              house.svg
            regular/
              heart.svg
              ...
            brands/
              github.svg
              ...

    Output structure (multi-variant):
        solid/arrow-right.svg
        solid/house.svg
        regular/heart.svg
        brands/github.svg
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

        # Filter for paths matching */svgs/{variant}/*.svg
        if "/svgs/" not in member.name:
            continue

        if not member.name.endswith(".svg"):
            continue

        # Extract variant and filename from path
        # Example: "fontawesome-free-6.7.2-web/svgs/solid/arrow-right.svg"
        # -> variant = "solid", filename = "arrow-right.svg"
        parts = member.name.split("/svgs/")
        if len(parts) != 2:
            continue

        variant_path = parts[1]  # "solid/arrow-right.svg"
        path_parts = variant_path.split("/", 1)
        if len(path_parts) != 2:
            continue

        variant = path_parts[0]
        filename = path_parts[1]

        # Only include variants listed in config
        if variant not in allowed_variants:
            continue

        # Names are already kebab-case, no normalization needed
        # Multi-variant, so output preserves style prefix
        zip_path = f"{variant}/{filename}"

        # Read file content
        with archive.extractfile(member) as f:
            content = f.read()

        yield ZipEntry(path=zip_path, content=content)


