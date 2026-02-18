"""Protocol definition for pack bundlers.

This module defines the PackBundler protocol that per-pack extraction
logic must implement.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Protocol

from justmyresource_pack_tools.archive import ArchiveReader
from justmyresource_pack_tools.config import UpstreamConfig
from justmyresource_pack_tools.repack import ZipEntry


class PackBundler(Protocol):
    """Protocol for pack bundlers that extract icons from upstream archives.

    Per-pack build scripts implement this protocol by providing an `extract`
    function that transforms upstream archive contents into standardized
    ZipEntry objects.
    """

    def extract(
        self, archive: ArchiveReader, config: UpstreamConfig
    ) -> Iterator[ZipEntry]:
        """Extract icons from upstream archive into standardized ZipEntry items.

        Args:
            archive: Archive reader for the upstream archive (tar or zip).
            config: Upstream configuration loaded from upstream.toml.

        Yields:
            ZipEntry objects with normalized paths and content.
        """
        ...


