"""Build script for Lucide icon pack.

Extracts SVGs from the upstream tar.gz archive and repackages them
into a standardized icons.zip format.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from justmyresource_pack_tools.archive import ArchiveReader
from justmyresource_pack_tools.config import UpstreamConfig
from justmyresource_pack_tools.repack import ZipEntry


def extract(archive: ArchiveReader, config: UpstreamConfig) -> Iterator[ZipEntry]:
    """Extract icons from Lucide upstream archive.

    Lucide archive structure (tar.gz from GitHub):
        lucide-{tag}/
          icons/
            arrow-down.svg
            alarm-clock.svg
            ...

    Output structure (flat, single variant):
        arrow-down.svg
        alarm-clock.svg
        ...

    Args:
        archive: Archive reader for the upstream archive.
        config: Upstream configuration loaded from upstream.toml.

    Yields:
        ZipEntry objects with normalized paths and content.
    """
    for member in archive.getmembers():
        # Only process SVG files in the icons/ directory
        if not member.isfile():
            continue

        # Filter for paths matching */icons/*.svg
        # Skip nested directories like icons/categories/
        if "/icons/" not in member.name:
            continue

        if not member.name.endswith(".svg"):
            continue

        # Extract just the filename (e.g., "arrow-down.svg")
        # from paths like "lucide-0.469.0/icons/arrow-down.svg"
        filename = Path(member.name).name

        # Names are already kebab-case, no normalization needed
        # Single variant, so output is flat
        zip_path = filename

        # Read file content
        with archive.extractfile(member) as f:
            content = f.read()

        yield ZipEntry(path=zip_path, content=content)

