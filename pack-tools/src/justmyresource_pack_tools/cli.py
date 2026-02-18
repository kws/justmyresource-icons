"""CLI for pack-tools."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import click

from justmyresource_pack_tools.archive import open_archive
from justmyresource_pack_tools.config import UpstreamConfig
from justmyresource_pack_tools.download import compute_sha256, download_with_cache
from justmyresource_pack_tools.manifest import generate_manifest
from justmyresource_pack_tools.readme import generate_readme
from justmyresource_pack_tools.repack import create_icon_zip


@click.group()
def main() -> None:
    """Build tools for creating JustMyResource icon packs."""
    pass


@main.command()
@click.argument("pack_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def fetch(pack_dir: Path) -> None:
    """Fetch upstream archive for a pack (downloads to cache/).

    Args:
        pack_dir: Path to pack directory (e.g., packs/lucide/).
    """
    upstream_toml = pack_dir / "upstream.toml"
    if not upstream_toml.exists():
        click.echo(f"Error: upstream.toml not found in {pack_dir}", err=True)
        sys.exit(1)

    try:
        config = UpstreamConfig.load(upstream_toml)
        cache_dir = pack_dir / "cache"

        click.echo(f"Fetching {pack_dir.name}...")
        click.echo(f"  URL: {config.source.url}")
        click.echo(f"  Tag: {config.source.tag}")

        archive_path = download_with_cache(
            url=config.source.url,
            cache_dir=cache_dir,
            expected_sha256=config.source.sha256 if config.source.sha256 else None,
        )

        click.echo(f"✓ Archive cached at {archive_path}")

    except Exception as e:
        click.echo(f"Error fetching {pack_dir.name}: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("pack_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def build(pack_dir: Path) -> None:
    """Build pack (extracts from cache, generates icons.zip + manifest + README).

    Args:
        pack_dir: Path to pack directory (e.g., packs/lucide/).
    """
    upstream_toml = pack_dir / "upstream.toml"
    if not upstream_toml.exists():
        click.echo(f"Error: upstream.toml not found in {pack_dir}", err=True)
        sys.exit(1)

    try:
        config = UpstreamConfig.load(upstream_toml)
        cache_dir = pack_dir / "cache"

        # Check cache exists
        cached_files = list(cache_dir.glob("*"))
        if not cached_files:
            click.echo(
                f"Error: No cached archive found in {cache_dir}.\n"
                f"Run 'pack-tools fetch {pack_dir}' first.",
                err=True,
            )
            sys.exit(1)

        # Use the cached archive (should be only one file)
        archive_path = cached_files[0]
        click.echo(f"Processing {archive_path.name}...")

        # Determine output directory from pack structure
        # Look for src/justmyresource_* directory
        src_dir = pack_dir / "src"
        if not src_dir.exists():
            click.echo(f"Error: src/ directory not found in {pack_dir}", err=True)
            sys.exit(1)

        output_dirs = [d for d in src_dir.iterdir() if d.is_dir() and d.name.startswith("justmyresource_")]
        if not output_dirs:
            click.echo(
                f"Error: No justmyresource_* directory found in {src_dir}",
                err=True,
            )
            sys.exit(1)
        output_dir = output_dirs[0]

        # Dynamically import and call per-pack bundler
        build_module_name = config.build.module
        build_entry_name = config.build.entry

        # Load the build module
        build_py = pack_dir / f"{build_module_name}.py"
        if not build_py.exists():
            click.echo(f"Error: {build_py} not found", err=True)
            sys.exit(1)

        spec = importlib.util.spec_from_file_location(
            f"{pack_dir.name}.{build_module_name}", build_py
        )
        if spec is None or spec.loader is None:
            click.echo(f"Error: Could not load {build_py}", err=True)
            sys.exit(1)

        build_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build_module)

        # Get the extract function
        if not hasattr(build_module, build_entry_name):
            click.echo(
                f"Error: {build_entry_name} not found in {build_py}",
                err=True,
            )
            sys.exit(1)

        extract_func = getattr(build_module, build_entry_name)

        # Open archive and extract icons
        with open_archive(archive_path) as archive:
            entries = list(extract_func(archive, config))

        # Create icons.zip
        zip_path = output_dir / "icons.zip"
        icon_count = create_icon_zip(iter(entries), zip_path)
        click.echo(f"✓ Created {zip_path} with {icon_count} icons")

        # Generate manifest
        manifest_path = output_dir / "pack_manifest.json"
        computed_sha256 = compute_sha256(archive_path)
        generate_manifest(
            upstream_toml_path=upstream_toml,
            icon_count=icon_count,
            variants=None,  # Read from config
            output_path=manifest_path,
            computed_sha256=computed_sha256,
        )
        click.echo(f"✓ Generated {manifest_path}")

        # Generate README
        generate_readme(pack_dir)
        click.echo(f"✓ Generated {pack_dir / 'README.md'}")

    except Exception as e:
        click.echo(f"Error building {pack_dir.name}: {e}", err=True)
        import traceback

        traceback.print_exc()
        sys.exit(1)


@main.command()
@click.argument("pack_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def dist(pack_dir: Path) -> None:
    """Build distribution wheel for a pack.

    Args:
        pack_dir: Path to pack directory (e.g., packs/lucide/).
    """
    try:
        # Determine workspace root (assumes structure: workspace_root/packs/pack_name/)
        workspace_root = pack_dir.resolve().parent.parent
        dist_dir = workspace_root / "dist"
        dist_dir.mkdir(exist_ok=True)

        click.echo(f"Building wheel for {pack_dir.name}...")
        result = subprocess.run(
            [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist_dir)],
            cwd=pack_dir,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            click.echo(f"Error: Build failed for {pack_dir.name}", err=True)
            if result.stdout:
                click.echo(result.stdout, err=True)
            if result.stderr:
                click.echo(result.stderr, err=True)
            sys.exit(1)
        click.echo(f"✓ Built wheel for {pack_dir.name}")

    except Exception as e:
        click.echo(f"Error building wheel for {pack_dir.name}: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("pack_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def install(pack_dir: Path) -> None:
    """Install a pack into the current environment for testing (editable mode).

    Args:
        pack_dir: Path to pack directory (e.g., packs/lucide/).
    """
    pyproject = pack_dir / "pyproject.toml"
    if not pyproject.exists():
        click.echo(f"Error: pyproject.toml not found in {pack_dir}", err=True)
        sys.exit(1)

    try:
        click.echo(f"Installing {pack_dir.name} (editable)...")
        result = subprocess.run(
            ["uv", "pip", "install", "-e", "."],
            cwd=pack_dir,
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            click.echo(f"Error: Install failed for {pack_dir.name}", err=True)
            if result.stdout:
                click.echo(result.stdout, err=True)
            if result.stderr:
                click.echo(result.stderr, err=True)
            sys.exit(1)
        click.echo(f"✓ Installed {pack_dir.name}")

    except Exception as e:
        click.echo(f"Error installing {pack_dir.name}: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

