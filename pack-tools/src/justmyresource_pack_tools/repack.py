"""Repacking utilities for creating icon zip files."""

from __future__ import annotations

import zipfile
from collections.abc import Iterator
from pathlib import Path
from typing import NamedTuple


class ZipEntry(NamedTuple):
    """Entry to write into the icon zip."""

    path: str
    """Path within the zip (e.g., "outlined/settings.svg" or "arrow-down.svg")."""
    content: bytes
    """File content as bytes."""


def create_icon_zip(entries: Iterator[ZipEntry], output_path: Path) -> int:
    """Create an icon zip file from entries.

    Args:
        entries: Iterator of ZipEntry objects to write.
        output_path: Path where the zip file will be created.

    Returns:
        Number of entries written.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for entry in entries:
            zip_file.writestr(entry.path, entry.content)
            count += 1

    return count


