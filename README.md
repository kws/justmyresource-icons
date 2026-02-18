# JustMyResource Icons

A monorepo containing icon pack implementations for [JustMyResource](https://github.com/kws/justmyresource), a resource discovery and resolution library for Python.

## Project Overview

This repository provides **JustMyResource**-compatible icon packs for major open-source icon sets. Each pack follows a **"zip-in-wheel"** distribution pattern:

- Icons are fetched directly from upstream sources at build time (not from intermediate PyPI packages)
- SVGs are packaged as a single ZIP archive within each wheel
- Zero runtime dependencies beyond `justmyresource` core
- Direct version tracking from upstream releases

All packs implement the `ResourcePack` protocol from `justmyresource` core, enabling uniform discovery and access through the `ResourceRegistry`.

## Available Packs

| Pack | PyPI Package | Version | Icons | Variants | License |
|------|-------------|---------|-------|----------|---------|
| **Lucide** | `justmyresource-lucide` | 0.469.0 | 1,544 | — | ISC |
| **Material Official** | `justmyresource-material-icons` | 4.0.0 | 6,862 | filled, outlined, rounded, sharp, two-tone | Apache-2.0 |
| **Material Community** | `justmyresource-mdi` | 7.4.47 | 7,447 | — | Apache-2.0 |
| **Phosphor** | `justmyresource-phosphor` | 2.0.8 | 7,488 | thin, light, regular, bold, fill, duotone | MIT |
| **Font Awesome Free** | `justmyresource-font-awesome` | 6.7.2 | 2,060 | solid, regular, brands | CC-BY-4.0 |
| **Heroicons** | `justmyresource-heroicons` | 2.2.0 | 1,288 | 24/outline, 24/solid, 20/solid, 16/solid | MIT |

## Prerequisites

- **Python 3.10+**
- **uv** or **pip** for package management
- **just** task runner (install with `cargo install just` or `brew install just`)
- **pack-tools** installed in development mode:

```bash
cd pack-tools
uv pip install -e .
```

## Quick Start

The build process for each pack follows three steps:

1. **Fetch** upstream archive (downloads to `cache/`):
   ```bash
   just fetch lucide
   ```

2. **Build** pack (extracts from cache, generates `icons.zip` + `pack_manifest.json` + `README.md`):
   ```bash
   just build lucide
   ```

3. **Dist** build wheel:
   ```bash
   just dist lucide
   ```

### Batch Operations

Fetch or build all packs at once:

```bash
just fetch-all    # Fetch all upstream archives
just build-all   # Build all packs
```

## Managing Packs

### Updating an Existing Pack

To update a pack to a newer upstream version:

1. **Edit `upstream.toml`** in the pack directory:
   - Update `tag` to the new upstream version
   - Update `url` to point to the new release archive
   - Clear or update `sha256` (will be computed on first fetch)

2. **Update version in `pyproject.toml`** to match the upstream tag

3. **Run the build pipeline**:
   ```bash
   just fetch <pack-name>
   just build <pack-name>
   just dist <pack-name>
   ```

The `fetch` command will download the new archive, verify its SHA-256 checksum, and cache it. The `build` command will extract icons, generate the manifest, and create the README. The `dist` command will build the wheel.

### Adding a New Pack

To add a new icon pack to the monorepo:

1. **Create pack directory structure**:
   ```
   packs/<pack-name>/
   ├── src/
   │   └── justmyresource_<pack_name>/
   │       └── __init__.py
   ├── pack.py
   ├── pyproject.toml
   └── upstream.toml
   ```

2. **Write `upstream.toml`** (see [upstream.toml Reference](#upstreamtoml-reference) below):
   - Configure `[source]` section with download URL and tag
   - Configure `[license]` section with SPDX identifier and copyright
   - Configure `[pack]` section with prefixes, description, variants
   - Configure `[build]` section with module/entry point (defaults: `pack.py` / `extract`)

3. **Write `pack.py`** extraction logic:
   - Implement the `PackBundler` protocol (see [Extraction Protocol](#packpy-extraction-protocol) below)
   - Extract SVGs from upstream archive structure
   - Normalize names to kebab-case
   - Handle variants if applicable

4. **Create `pyproject.toml`**:
   - Set package name: `justmyresource-<pack-name>`
   - Set version to match upstream tag
   - Add dependency: `justmyresource>=1.0.0,<2.0.0`
   - Register entry point: `justmyresource.packs` → `<pack-name>`

5. **Create `__init__.py`**:
   - Subclass `ZippedResourcePack` from `justmyresource.pack_utils`
   - Implement `_normalize_name()` if needed (for variant handling)
   - Export `get_resource_provider()` factory function

6. **Run the build pipeline**:
   ```bash
   just fetch <pack-name>
   just build <pack-name>
   just dist <pack-name>
   ```

See existing packs for examples:
- **Simple pack** (single variant): [`packs/lucide/`](packs/lucide/)
- **Multi-variant pack**: [`packs/phosphor/`](packs/phosphor/)

## Project Structure

```
justmyresource-icons/
├── pack-tools/                    # Build tooling package
│   ├── src/
│   │   └── justmyresource_pack_tools/
│   │       ├── cli.py            # CLI commands (fetch, build, dist)
│   │       ├── config.py        # UpstreamConfig loader
│   │       ├── download.py       # Archive download + caching
│   │       ├── archive.py        # Unified tar/zip reader
│   │       ├── repack.py         # Create icons.zip
│   │       ├── manifest.py       # Generate pack_manifest.json
│   │       ├── normalize.py      # Name normalization utilities
│   │       ├── readme.py         # README generation
│   │       └── protocol.py      # PackBundler protocol
│   └── pyproject.toml
│
├── packs/                        # Icon pack packages
│   ├── <pack-name>/
│   │   ├── pack.py              # Per-pack extraction logic
│   │   ├── upstream.toml        # Pack configuration
│   │   ├── pyproject.toml       # Package metadata
│   │   ├── README.md            # Auto-generated pack docs
│   │   ├── LICENSE              # Upstream license
│   │   ├── LICENSES/            # Additional license files
│   │   ├── cache/               # Cached upstream archives (gitignored)
│   │   └── src/
│   │       └── justmyresource_<name>/
│   │           ├── __init__.py
│   │           ├── icons.zip    # Generated at build time (gitignored)
│   │           └── pack_manifest.json  # Generated at build time (gitignored)
│   └── ...
│
├── justfile                      # Build automation
├── pyproject.toml                # Root workspace config (Ruff/Mypy)
└── README.md                     # This file
```

## upstream.toml Reference

The `upstream.toml` file is the single source of truth for pack metadata. It does NOT contain extraction logic (that lives in `pack.py`).

### Schema

```toml
[source]
url = "https://github.com/owner/repo/archive/refs/tags/v1.0.0.tar.gz"
tag = "v1.0.0"
sha256 = ""  # Fill when first fetched

[license]
spdx = "MIT"
copyright = "Copyright (c) Contributors"
upstream_license_url = "https://github.com/owner/repo/blob/main/LICENSE"
modifications = "SVGs extracted and repackaged; names normalized to kebab-case"

[pack]
prefixes = ["pack-name", "short"]
description = "Pack description — icon count and style notes"
source_url = "https://pack-website.com"
variants = []  # Empty for single-variant packs
default_variant = ""  # Empty for single-variant packs

[build]
module = "pack"  # Python module to import (default: "pack")
entry = "extract"  # Function name to call (default: "extract")
```

### Field Descriptions

**`[source]`**
- `url` (required): Direct download URL for the upstream archive
- `tag` (required): Upstream version tag (used for pack versioning)
- `sha256` (optional): SHA-256 checksum for verification (empty until first fetch)

**`[license]`**
- `spdx` (required): SPDX license identifier (e.g., "MIT", "ISC", "Apache-2.0", "CC-BY-4.0")
- `copyright` (required): Copyright holder string
- `upstream_license_url` (required): URL to upstream license file
- `modifications` (optional): Description of modifications during repackaging

**`[pack]`**
- `prefixes` (required): List of prefix aliases (e.g., `["lucide", "luc"]`)
- `description` (required): Human-readable description
- `source_url` (required): Upstream project homepage or repository URL
- `variants` (required): List of variant names (empty list `[]` for single-variant packs)
- `default_variant` (required): Default variant for bare lookups (empty string `""` for single-variant packs)

**`[build]`**
- `module` (optional, default: `"pack"`): Python module name (looks for `{module}.py` in pack directory)
- `entry` (optional, default: `"extract"`): Function name that implements `PackBundler` protocol

## pack.py Extraction Protocol

Each pack implements the `PackBundler` protocol by providing an `extract` function in `pack.py`:

```python
from collections.abc import Iterator
from justmyresource_pack_tools.archive import ArchiveReader
from justmyresource_pack_tools.config import UpstreamConfig
from justmyresource_pack_tools.repack import ZipEntry

def extract(archive: ArchiveReader, config: UpstreamConfig) -> Iterator[ZipEntry]:
    """Extract icons from upstream archive into standardized ZipEntry items.
    
    Args:
        archive: Archive reader for the upstream archive (tar or zip)
        config: Upstream configuration loaded from upstream.toml
    
    Yields:
        ZipEntry objects with normalized paths and content
    """
    for member in archive.getmembers():
        if not member.isfile():
            continue
        
        # Filter for SVG files in expected location
        if not member.name.endswith(".svg"):
            continue
        if "/icons/" not in member.name:
            continue
        
        # Extract and normalize filename
        filename = Path(member.name).name
        zip_path = filename  # Or variant/filename for multi-variant packs
        
        # Read file content
        with archive.extractfile(member) as f:
            content = f.read()
        
        yield ZipEntry(path=zip_path, content=content)
```

The function receives an `ArchiveReader` (unified interface for tar/zip) and `UpstreamConfig` (parsed from `upstream.toml`), and yields `ZipEntry` objects with:
- `path`: Normalized path within the zip (e.g., `"arrow-down.svg"` or `"regular/arrow-down.svg"`)
- `content`: File content as bytes

The build system will:
1. Call your `extract()` function
2. Collect all `ZipEntry` objects
3. Create `icons.zip` from the entries
4. Generate `pack_manifest.json` from `upstream.toml` + icon count
5. Generate `README.md` from Jinja2 template

## Build Pipeline Detail

### `fetch` Command

```bash
pack-tools fetch packs/<pack-name>
```

- Reads `upstream.toml` to get source URL and SHA-256
- Downloads archive to `packs/<pack-name>/cache/`
- Validates SHA-256 checksum if provided
- Reuses cache if valid checksum matches

### `build` Command

```bash
pack-tools build packs/<pack-name>
```

- Loads `upstream.toml` configuration
- Opens cached archive from `cache/` directory
- Dynamically imports `pack.py` and calls `extract()` function
- Creates `icons.zip` from `ZipEntry` iterator
- Generates `pack_manifest.json` with pack metadata
- Generates `README.md` from Jinja2 template
- Writes all artifacts to `src/justmyresource_<name>/`

### `dist` Command

```bash
pack-tools dist packs/<pack-name>
```

- Runs `python -m build --wheel` in the pack directory
- Outputs wheel to `dist/` directory
- Wheel contains `icons.zip` and `pack_manifest.json` bundled inside

## Development

### Installing a Pack for Testing

Install a pack in editable mode:

```bash
just install <pack-name>
```

Or manually:

```bash
cd packs/<pack-name>
uv pip install -e .
```

### Code Quality

Lint, format, and type-check all code:

```bash
just lint        # Check code style
just format      # Auto-fix and format
just typecheck   # Run mypy type checking
```

### Generating READMEs

Regenerate all pack READMEs from `upstream.toml`:

```bash
just generate-readmes
```

## License

Each pack carries its own upstream license in the `LICENSES/` directory. The pack implementation code itself is licensed under MIT (see individual pack `LICENSE` files for details).

- **Lucide**: ISC
- **Material Official**: Apache-2.0
- **Material Community**: Apache-2.0
- **Phosphor**: MIT
- **Font Awesome Free**: CC-BY-4.0 (attribution required)
- **Heroicons**: MIT

## Related Projects

- **[justmyresource](https://github.com/kws/justmyresource)**: Core resource discovery library
- **[pack-tools](pack-tools/)**: Build tooling for creating icon packs

