"""Unified archive reading interface for tar and zip files."""

from __future__ import annotations

import tarfile
import zipfile
from collections.abc import Iterator
from pathlib import Path
from typing import Protocol


class ArchiveMember(Protocol):
    """Protocol for archive member objects."""

    name: str
    """Path of the member within the archive."""

    def isfile(self) -> bool:
        """Check if member is a file (not a directory)."""
        ...


class ArchiveReader(Protocol):
    """Protocol for archive readers."""

    def getmembers(self) -> list[ArchiveMember]:
        """Get all members in the archive."""
        ...

    def extractfile(self, member: ArchiveMember) -> ArchiveMember:
        """Extract a file member for reading."""
        ...


class ZipArchiveMember:
    """Adapter to make ZipInfo conform to ArchiveMember protocol."""

    def __init__(self, info: zipfile.ZipInfo) -> None:
        """Initialize adapter from ZipInfo.

        Args:
            info: ZipInfo object from zipfile.
        """
        self._info = info
        self.name = info.filename

    def isfile(self) -> bool:
        """Check if member is a file (not a directory).

        Returns:
            True if file, False if directory.
        """
        return not self._info.is_dir()


class TarArchiveReader:
    """Archive reader for tar files."""

    def __init__(self, tar_path: Path) -> None:
        """Initialize tar archive reader.

        Args:
            tar_path: Path to tar archive.
        """
        self._tar_path = tar_path
        self._tar: tarfile.TarFile | None = None

    def __enter__(self) -> ArchiveReader:
        """Open tar file for reading."""
        # Auto-detect compression
        mode = "r"
        if self._tar_path.suffix == ".gz" or self._tar_path.name.endswith(".tar.gz"):
            mode = "r:gz"
        elif self._tar_path.suffix == ".bz2" or self._tar_path.name.endswith(".tar.bz2"):
            mode = "r:bz2"
        elif self._tar_path.suffix == ".xz" or self._tar_path.name.endswith(".tar.xz"):
            mode = "r:xz"

        self._tar = tarfile.open(self._tar_path, mode)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close tar file."""
        if self._tar:
            self._tar.close()
            self._tar = None

    def getmembers(self) -> list[ArchiveMember]:
        """Get all members in the tar archive."""
        if not self._tar:
            raise RuntimeError("Archive not open")
        return list(self._tar.getmembers())

    def extractfile(self, member: ArchiveMember) -> ArchiveMember:
        """Extract a file member for reading."""
        if not self._tar:
            raise RuntimeError("Archive not open")
        return self._tar.extractfile(member)  # type: ignore[return-value]


class ZipArchiveReader:
    """Archive reader for zip files."""

    def __init__(self, zip_path: Path) -> None:
        """Initialize zip archive reader.

        Args:
            zip_path: Path to zip archive.
        """
        self._zip_path = zip_path
        self._zip: zipfile.ZipFile | None = None

    def __enter__(self) -> ArchiveReader:
        """Open zip file for reading."""
        self._zip = zipfile.ZipFile(self._zip_path, "r")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close zip file."""
        if self._zip:
            self._zip.close()
            self._zip = None

    def getmembers(self) -> list[ArchiveMember]:
        """Get all members in the zip archive."""
        if not self._zip:
            raise RuntimeError("Archive not open")
        # Convert ZipInfo to a protocol-compatible object
        return [ZipArchiveMember(info) for info in self._zip.infolist()]

    def extractfile(self, member: ArchiveMember) -> ArchiveMember:
        """Extract a file member for reading."""
        if not self._zip:
            raise RuntimeError("Archive not open")
        return self._zip.open(member.name)  # type: ignore[return-value]


def open_archive(archive_path: Path) -> ArchiveReader:
    """Open an archive file (tar or zip) for reading.

    Args:
        archive_path: Path to archive file.

    Returns:
        Context manager that yields an ArchiveReader.

    Raises:
        ValueError: If archive type cannot be determined.
    """
    if archive_path.suffix == ".zip" or archive_path.name.endswith(".zip"):
        return ZipArchiveReader(archive_path)
    elif (
        archive_path.suffix == ".tar"
        or archive_path.suffix == ".gz"
        or archive_path.name.endswith(".tar.gz")
        or archive_path.name.endswith(".tgz")
        or archive_path.name.endswith(".tar.bz2")
        or archive_path.name.endswith(".tar.xz")
    ):
        return TarArchiveReader(archive_path)
    else:
        raise ValueError(f"Cannot determine archive type for {archive_path}")

