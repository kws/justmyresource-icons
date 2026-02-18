"""Configuration loading for upstream.toml files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _load_toml(file_path: Path) -> dict[str, Any]:
    """Load TOML file with fallback to tomli.

    Args:
        file_path: Path to TOML file.

    Returns:
        Parsed TOML dictionary.

    Raises:
        ImportError: If neither tomllib nor tomli is available.
        ValueError: If file cannot be parsed.
    """
    try:
        import tomllib
    except ImportError:
        try:
            import tomli as tomllib
        except ImportError:
            raise ImportError(
                "TOML parsing requires Python 3.11+ (tomllib) or tomli package. "
                "Install with: pip install tomli"
            ) from None

    with open(file_path, "rb") as f:
        return tomllib.load(f)


@dataclass(frozen=True, slots=True)
class SourceConfig:
    """Source configuration from upstream.toml [source] section."""

    url: str
    tag: str
    sha256: str = ""


@dataclass(frozen=True, slots=True)
class LicenseConfig:
    """License configuration from upstream.toml [license] section."""

    spdx: str
    copyright: str
    upstream_license_url: str
    modifications: str = ""
    attribution_required: bool = False
    attribution_text: str = ""
    brands_note: str = ""


@dataclass(frozen=True, slots=True)
class PackConfig:
    """Pack configuration from upstream.toml [pack] section."""

    prefixes: list[str]
    description: str
    source_url: str
    variants: list[str]
    default_variant: str


@dataclass(frozen=True, slots=True)
class BuildConfig:
    """Build configuration from upstream.toml [build] section."""

    module: str = "pack"
    entry: str = "extract"


@dataclass(frozen=True, slots=True)
class UpstreamConfig:
    """Complete upstream.toml configuration."""

    source: SourceConfig
    license: LicenseConfig
    pack: PackConfig
    build: BuildConfig

    @classmethod
    def load(cls, upstream_toml_path: Path) -> UpstreamConfig:
        """Load and parse upstream.toml file.

        Args:
            upstream_toml_path: Path to upstream.toml file.

        Returns:
            UpstreamConfig instance.

        Raises:
            ValueError: If required fields are missing.
        """
        config = _load_toml(upstream_toml_path)

        source_dict = config.get("source", {})
        source = SourceConfig(
            url=source_dict.get("url", ""),
            tag=source_dict.get("tag", ""),
            sha256=source_dict.get("sha256", "").strip(),
        )

        if not source.url or not source.tag:
            raise ValueError("Missing required fields in [source]: url, tag")

        license_dict = config.get("license", {})
        license_config = LicenseConfig(
            spdx=license_dict.get("spdx", ""),
            copyright=license_dict.get("copyright", ""),
            upstream_license_url=license_dict.get("upstream_license_url", ""),
            modifications=license_dict.get("modifications", ""),
            attribution_required=license_dict.get("attribution_required", False),
            attribution_text=license_dict.get("attribution_text", ""),
            brands_note=license_dict.get("brands_note", ""),
        )

        if not license_config.spdx or not license_config.copyright:
            raise ValueError("Missing required fields in [license]: spdx, copyright")

        pack_dict = config.get("pack", {})
        pack = PackConfig(
            prefixes=pack_dict.get("prefixes", []),
            description=pack_dict.get("description", ""),
            source_url=pack_dict.get("source_url", ""),
            variants=pack_dict.get("variants", []),
            default_variant=pack_dict.get("default_variant", ""),
        )

        if not pack.prefixes or not pack.description or not pack.source_url:
            raise ValueError(
                "Missing required fields in [pack]: prefixes, description, source_url"
            )

        build_dict = config.get("build", {})
        build = BuildConfig(
            module=build_dict.get("module", "pack"),
            entry=build_dict.get("entry", "extract"),
        )

        return cls(source=source, license=license_config, pack=pack, build=build)

