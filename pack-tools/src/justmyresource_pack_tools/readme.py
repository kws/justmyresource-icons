"""README generation for icon packs using Jinja2 templates."""

from __future__ import annotations

import importlib.resources
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from justmyresource_pack_tools.config import UpstreamConfig


def generate_readme(pack_dir: Path) -> None:
    """Generate README.md for a single pack.

    Args:
        pack_dir: Path to pack directory (e.g., packs/lucide/).
    """
    upstream_toml = pack_dir / "upstream.toml"
    if not upstream_toml.exists():
        print(f"⚠️  Skipping {pack_dir.name}: no upstream.toml found")
        return

    config = UpstreamConfig.load(upstream_toml)

    # Read pyproject.toml to get package name
    pyproject_toml = pack_dir / "pyproject.toml"
    package_name = pack_dir.name.replace("-", "_")
    if pyproject_toml.exists():
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib

        with open(pyproject_toml, "rb") as f:
            pyproject = tomllib.load(f)
            package_name = pyproject.get("project", {}).get("name", package_name)

    # Determine pack name from directory
    pack_name = pack_dir.name.replace("-", " ").title()

    # Load Jinja2 template
    env = Environment(
        loader=PackageLoader("justmyresource_pack_tools", "templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("readme.md.j2")

    # Build context
    default_prefix = config.pack.prefixes[0] if config.pack.prefixes else "pack"
    aliases = config.pack.prefixes[1:] if len(config.pack.prefixes) > 1 else []
    context: dict[str, Any] = {
        "pack_name": pack_name,
        "package_name": package_name,
        "description": config.pack.description,
        "prefixes": config.pack.prefixes,
        "default_prefix": default_prefix,
        "aliases": aliases,
        "has_aliases": len(aliases) > 0,
        "variants": config.pack.variants,
        "default_variant": config.pack.default_variant,
        "has_variants": len(config.pack.variants) > 0,
        "license_spdx": config.license.spdx,
        "copyright": config.license.copyright,
        "source_url": config.pack.source_url,
        "tag": config.source.tag,
    }

    # Render template
    readme_content = template.render(**context)

    # Write README
    readme_path = pack_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"✓ Generated {readme_path}")


def generate_all_readmes(packs_dir: Path) -> int:
    """Generate READMEs for all packs in a directory.

    Args:
        packs_dir: Path to packs directory (e.g., packs/).

    Returns:
        Exit code (0 for success, 1 for error).
    """
    if not packs_dir.exists():
        print(f"Error: packs directory not found at {packs_dir}")
        return 1

    for pack_dir in sorted(packs_dir.iterdir()):
        if pack_dir.is_dir() and (pack_dir / "upstream.toml").exists():
            try:
                generate_readme(pack_dir)
            except Exception as e:
                print(f"Error generating README for {pack_dir.name}: {e}")
                return 1

    return 0


