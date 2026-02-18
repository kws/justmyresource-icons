"""Build script for Material Design Icons (Official) icon pack.

Extracts SVGs from the upstream tar.gz archive and repackages them
into a standardized icons.zip format with variant prefixes.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from justmyresource_pack_tools.archive import ArchiveReader
from justmyresource_pack_tools.config import UpstreamConfig
from justmyresource_pack_tools.normalize import to_kebab_case
from justmyresource_pack_tools.repack import ZipEntry

# Variant directory name mapping
VARIANT_MAP = {
    "materialicons": "filled",
    "materialiconsoutlined": "outlined",
    "materialiconsround": "rounded",
    "materialiconssharp": "sharp",
    "materialiconstwotone": "two-tone",
}


def extract(archive: ArchiveReader, config: UpstreamConfig) -> Iterator[ZipEntry]:
    """Extract icons from Material Design Icons (Official) upstream archive.

    Material Design Icons (Official) archive structure (tar.gz from GitHub):
        material-design-icons-{tag}/
          src/
            {category}/
              {icon_name}/
                materialicons/24px.svg
                materialiconsoutlined/24px.svg
                materialiconsround/24px.svg
                materialiconssharp/24px.svg
                materialiconstwotone/24px.svg

    Output structure (multi-variant):
        filled/account-balance.svg
        outlined/account-balance.svg
        rounded/account-balance.svg
        sharp/account-balance.svg
        two-tone/account-balance.svg
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

        # Filter for paths matching */src/{category}/{icon_name}/{variant_dir}/24px.svg
        if "/src/" not in member.name:
            continue

        if not member.name.endswith("24px.svg"):
            continue

        # Extract category, icon_name, and variant_dir from path
        # Example: "material-design-icons-4.0.0/src/action/account_balance/materialiconsoutlined/24px.svg"
        # -> category = "action", icon_name = "account_balance", variant_dir = "materialiconsoutlined"
        parts = member.name.split("/src/")
        if len(parts) != 2:
            continue

        path_after_src = parts[1]  # "action/account_balance/materialiconsoutlined/24px.svg"
        path_components = path_after_src.split("/")
        if len(path_components) != 4:
            continue

        category = path_components[0]  # "action"
        icon_name = path_components[1]  # "account_balance" (snake_case)
        variant_dir = path_components[2]  # "materialiconsoutlined"
        filename = path_components[3]  # "24px.svg"

        # Map variant directory to variant name
        variant = VARIANT_MAP.get(variant_dir)
        if variant is None:
            continue

        # Only include variants listed in config
        if variant not in allowed_variants:
            continue

        # Normalize icon name from snake_case to kebab-case
        # e.g., "account_balance" -> "account-balance", "3d_rotation" -> "3d-rotation"
        normalized_name = to_kebab_case(icon_name)

        # Multi-variant, so output preserves variant prefix
        zip_path = f"{variant}/{normalized_name}.svg"

        # Read file content
        with archive.extractfile(member) as f:
            content = f.read()

        yield ZipEntry(path=zip_path, content=content)

