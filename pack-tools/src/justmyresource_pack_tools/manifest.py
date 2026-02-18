"""Manifest generation for icon packs.

This module generates pack_manifest.json files from upstream.toml
and extracted content metadata.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from justmyresource_pack_tools.config import UpstreamConfig


def generate_manifest(
    upstream_toml_path: Path,
    icon_count: int,
    variants: list[str] | None = None,
    output_path: Path | None = None,
    computed_sha256: str | None = None,
) -> dict[str, Any]:
    """Generate pack_manifest.json from upstream.toml and pack metadata.

    Args:
        upstream_toml_path: Path to upstream.toml configuration file.
        icon_count: Number of icons in the pack.
        variants: Optional list of variant names. If None, reads from upstream.toml [pack].variants.
        output_path: Optional path to write manifest JSON file.
        computed_sha256: Computed SHA-256 of the downloaded archive.

    Returns:
        Dictionary containing the manifest data.

    Raises:
        ValueError: If upstream.toml is invalid.
    """
    config = UpstreamConfig.load(upstream_toml_path)

    # Use provided variants or read from config
    variant_list = variants if variants is not None else config.pack.variants
    sha256 = computed_sha256 or config.source.sha256

    # Extract pack name from directory structure
    pack_name = upstream_toml_path.parent.name

    # Extract GitHub repo from URL if it's a GitHub URL
    upstream_repo = ""
    if "github.com" in config.source.url:
        # Try to extract owner/repo from URL
        parts = config.source.url.split("github.com/")
        if len(parts) > 1:
            repo_part = parts[1].split("/")[0:2]
            if len(repo_part) == 2:
                upstream_repo = f"https://github.com/{'/'.join(repo_part)}"

    manifest = {
        "pack": {
            "name": pack_name,
            "version": config.source.tag,
            "upstream_repo": upstream_repo,
            "upstream_tag": config.source.tag,
            "upstream_license": config.license.spdx,
            "build_timestamp": get_build_timestamp(),
            "sha256_archive": sha256,
            # Include pack metadata for runtime access
            "prefixes": config.pack.prefixes,
            "description": config.pack.description,
            "source_url": config.pack.source_url,
            "variants": variant_list,
            "default_variant": config.pack.default_variant,
        },
        "contents": {
            "icon_count": icon_count,
            "variants": variant_list,
            "format": "image/svg+xml",
            "naming_convention": "kebab-case",
        },
        "style": {
            "description": config.pack.description,
        },
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

    return manifest


def get_build_timestamp() -> str:
    """Get current timestamp in ISO 8601 format.

    Returns:
        ISO 8601 timestamp string (e.g., "2026-02-16T12:00:00Z").
    """
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


