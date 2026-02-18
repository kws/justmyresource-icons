"""Build script for Material Design Icons (Community) icon pack.

Extracts SVGs from the upstream zip archive and repackages them
into a standardized icons.zip format.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from justmyresource_pack_tools.archive import ArchiveReader
from justmyresource_pack_tools.config import UpstreamConfig
from justmyresource_pack_tools.repack import ZipEntry


def extract(archive: ArchiveReader, config: UpstreamConfig) -> Iterator[ZipEntry]:
    """Extract icons from Material Design Icons (Community) upstream archive.

    Material Design Icons (Community) archive structure (zip from GitHub):
        MaterialDesign-{hash}/
          svg/
            ab-testing.svg
            abacus.svg
            account-alert.svg
            ...
          templates/
            ...

    Output structure (flat, single variant):
        ab-testing.svg
        abacus.svg
        account-alert.svg
        ...

    Args:
        archive: Archive reader for the upstream archive.
        config: Upstream configuration loaded from upstream.toml.

    Yields:
        ZipEntry objects with normalized paths and content.
    """
    for member in archive.getmembers():
        # Only process SVG files
        if not member.isfile():
            continue

        # Filter for paths matching */svg/*.svg
        # Exclude templates/ directory
        if "/svg/" not in member.name:
            continue

        if not member.name.endswith(".svg"):
            continue

        # Extract just the filename (e.g., "ab-testing.svg")
        # from paths like "MaterialDesign-2424e74.../svg/ab-testing.svg"
        filename = Path(member.name).name

        # Names are already kebab-case, no normalization needed
        # Single variant, so output is flat
        zip_path = filename

        # Read file content
        with archive.extractfile(member) as f:
            content = f.read()

        yield ZipEntry(path=zip_path, content=content)

