# Implementation Plan: JustMyResource Icons Monorepo

This plan outlines the steps to establish a monorepo for `justmyresource`, containing the core library and icon packs for the most widely-used open-source icon sets.

## Strategy

- **Architecture**: Monorepo with `core/` and `packs/` directories.
- **Distribution**: "Zip-in-Wheel" pattern. Icons are fetched **directly from upstream** at build time (not from intermediate PyPI packages), stored as a single ZIP within the wheel, and accessed via `zipfile` at runtime.
- **Build System**: `hatch` with shared build hooks for automated fetching.
- **Versioning**: Each pack's version tracks its upstream release (e.g., `justmyresource-lucide==0.564.0` ↔ Lucide `0.564.0`).

### Why "Download from Upstream" (not wrapping PyPI packages)

The existing `justmyresource-lucide` depends on the third-party `lucide` PyPI package (a Django/Jinja template library) and accesses its internal `lucide.zip` — an undocumented implementation detail. This approach has significant drawbacks:

1. **Fragile coupling** to third-party internals that can break without warning.
2. **Unnecessary transitive dependencies** (Django template code for a CLI tool user).
3. **Inconsistent formats** per upstream package (zip, loose files, Python dicts).
4. **Limited coverage** — most icon sets don't have suitable PyPI wrappers.
5. **Version indirection** — pinning a wrapper's version, not the icon set's version.

The Zip-in-Wheel approach gives us **uniform architecture**, **zero runtime dependencies** (beyond `justmyresource` core), **direct source-of-truth versioning**, and **resilience** against third-party package changes.

---

## Target Icon Sets

### Tier 1: The Essential Three (High Priority)

| Pack | Upstream Repo | ~Icons | Style | Variants | License |
|------|--------------|--------|-------|----------|---------|
| **Lucide** | `lucide-icons/lucide` | 1,500+ | 2px stroke, minimalist | Single (consistent stroke) | ISC |
| **Material Design Icons (Official)** | `google/material-design-icons` | 2,500+ | Google design system | Filled, Outlined, Rounded, Sharp, Two-Tone | Apache 2.0 |
| **Material Design Icons (Community)** | `Templarian/MaterialDesign` / `@mdi/svg` (npm) | 7,000+ | Massive variety | Single (filled) | Apache 2.0 (Pictogrammers) |

### Tier 2: Functional Expansion (Medium Priority)

| Pack | Upstream Repo | ~Icons | Style | Variants | License |
|------|--------------|--------|-------|----------|---------|
| **Phosphor Icons** | `phosphor-icons/core` | 1,200+ | Flexible weight system | Thin, Light, Regular, Bold, Fill, Duotone | MIT |
| **Font Awesome (Free)** | `FortAwesome/Font-Awesome` | 2,000+ (free) | Industry standard | Solid, Regular, Brands | CC BY 4.0 / MIT |
| **Heroicons** | `tailwindlabs/heroicons` | 300+ | Tailwind-aligned | 16/solid, 20/solid, 24/outline, 24/solid | MIT |

---

## Upstream Source Details

### Lucide
- **Source**: GitHub releases at `lucide-icons/lucide`
- **SVG location**: `icons/` directory in source tree; also available via `lucide-static` npm package
- **Download strategy**: Clone/download tag archive, extract `icons/*.svg`
- **Naming**: kebab-case (`arrow-down.svg`, `alarm-clock.svg`)
- **Prefixes**: `lucide`, `luc`

### Material Design Icons (Official)
- **Source**: GitHub repo `google/material-design-icons`
- **SVG location**: Complex structure — organized by category, then variant. The `material-symbols` variant is the modern replacement.
- **Download strategy**: Download tag archive; extract and repack only the SVG files. The repo is very large (~4GB with fonts), so the build hook must selectively extract.
- **Naming**: snake_case (`arrow_back.svg`, `settings.svg`) — normalize to kebab-case at build time
- **Variants**: `filled`, `outlined`, `rounded`, `sharp`, `two-tone` — each icon exists in up to 5 variants
- **Variant handling**: Stored in zip as `{variant}/{name}.svg`. Default resolution returns `outlined` variant; explicit access via `mi:outlined/settings` or metadata query.
- **Prefixes**: `material-icons`, `mi`

### Material Design Icons (Community / Pictogrammers)
- **Source**: `@mdi/svg` npm package or GitHub releases at `Templarian/MaterialDesign`
- **SVG location**: `svg/` directory in npm package (flat, clean)
- **Download strategy**: Download npm tarball or GitHub release; extract `svg/*.svg`
- **Naming**: kebab-case (`dishwasher.svg`, `raspberry-pi.svg`)
- **Prefixes**: `mdi`

### Phosphor Icons
- **Source**: GitHub releases at `phosphor-icons/core`
- **SVG location**: Organized by weight: `assets/{weight}/{name}.svg`
- **Download strategy**: Download tag archive; extract all weight directories
- **Naming**: kebab-case with weight suffix for non-regular (`arrow-right.svg`, `arrow-right-bold.svg`)
- **Variant handling**: Weights stored as `{weight}/{name}.svg`. Default resolution returns `regular` weight; explicit access via `phosphor:bold/arrow-right` or metadata query.
- **Prefixes**: `phosphor`, `ph`

### Font Awesome (Free)
- **Source**: GitHub releases at `FortAwesome/Font-Awesome`
- **SVG location**: `svgs/{style}/` in release archive (solid, regular, brands)
- **Download strategy**: Download release zip; extract `svgs/**/*.svg` (free tier only)
- **Naming**: kebab-case (`arrow-right.svg`, `house.svg`)
- **Variant handling**: Styles stored as `{style}/{name}.svg`. Default resolution returns `solid`; explicit access via `fa:regular/heart` or `fa:brands/github`.
- **Prefixes**: `font-awesome`, `fa`
- **License note**: SVGs are CC BY 4.0 (attribution required); code is MIT. The `brands` subset has its own terms.

### Heroicons
- **Source**: GitHub releases at `tailwindlabs/heroicons`
- **SVG location**: `src/{size}/{style}/` (e.g., `src/24/outline/`, `src/20/solid/`)
- **Download strategy**: Download tag archive; extract `src/**/*.svg`
- **Naming**: kebab-case (`arrow-right.svg`, `home.svg`)
- **Variant handling**: Size+style combinations: `24/outline`, `24/solid`, `20/solid`, `16/solid`. Default resolution returns `24/outline`; explicit access via `hero:24/solid/home`.
- **Prefixes**: `heroicons`, `hero`

---

## Pack Metadata & Indexing

Each pack should ship with a **metadata index** that enables version management, variant resolution, and downstream tooling.

### Pack Manifest (`pack_manifest.json`)

Generated at **build time** by the hatch build hook and bundled alongside `icons.zip` in the wheel:

```json
{
  "pack": {
    "name": "lucide",
    "version": "0.564.0",
    "upstream_repo": "https://github.com/lucide-icons/lucide",
    "upstream_tag": "0.564.0",
    "upstream_license": "ISC",
    "build_timestamp": "2026-02-15T12:00:00Z",
    "sha256_archive": "abc123..."
  },
  "contents": {
    "icon_count": 1563,
    "variants": [],
    "format": "image/svg+xml",
    "naming_convention": "kebab-case"
  },
  "style": {
    "stroke_width": "2px",
    "default_size": "24x24",
    "design_system": "Lucide",
    "description": "Minimalist, 2px stroke icons"
  }
}
```

For packs with **variants** (Material Official, Phosphor, Font Awesome, Heroicons):

```json
{
  "pack": {
    "name": "material-icons",
    "version": "4.0.0",
    "upstream_repo": "https://github.com/google/material-design-icons",
    "upstream_tag": "4.0.0",
    "upstream_license": "Apache-2.0",
    "build_timestamp": "2026-02-15T12:00:00Z",
    "sha256_archive": "def456..."
  },
  "contents": {
    "icon_count": 2589,
    "variants": ["filled", "outlined", "rounded", "sharp", "two-tone"],
    "default_variant": "outlined",
    "format": "image/svg+xml",
    "naming_convention": "kebab-case"
  },
  "style": {
    "default_size": "24x24",
    "design_system": "Material Design",
    "description": "Google Material Design icon set with 5 style variants"
  }
}
```

### Runtime Access

The `ZippedResourcePack` base class exposes manifest data:

```python
pack = registry.get_pack("lucide")
manifest = pack.get_manifest()   # Returns parsed pack_manifest.json
manifest["pack"]["version"]      # "0.564.0"
manifest["contents"]["variants"] # []
```

The manifest is also available through `ResourceContent.metadata` on individual resources:

```python
content = registry.get_resource("mi:settings")
content.metadata["variant"]  # "outlined" (the default)
content.metadata["pack_version"]  # "4.0.0"
```

---

## Upstream Version Tracking

### The Problem

Each pack tracks an upstream GitHub release. We need to:
1. Know what version each pack currently bundles.
2. Detect when upstream releases a new version.
3. Make it easy to bump and rebuild.

### Solution: `upstream.toml` (per pack)

Each pack directory contains an `upstream.toml` that is the **single source of truth** for pack metadata (source URL, license, pack identity, variants). It does NOT contain extraction logic (that lives in per-pack `build.py` scripts).

```toml
# packs/lucide/upstream.toml
[source]
url = "https://github.com/lucide-icons/lucide/archive/refs/tags/0.469.0.tar.gz"
tag = "0.469.0"
sha256 = ""  # Fill when first fetched

[license]
spdx = "ISC"
copyright = "Copyright (c) Lucide Contributors"
upstream_license_url = "https://github.com/lucide-icons/lucide/blob/main/LICENSE"
modifications = "SVGs extracted and repackaged; names normalized to kebab-case"

[pack]
prefixes = ["lucide", "luc"]
description = "Lucide icon library — 1500+ minimalist SVG icons"
source_url = "https://lucide.dev"
variants = []
default_variant = ""
```

For a multi-variant pack:

```toml
# packs/material-official/upstream.toml
[source]
url = "https://github.com/google/material-design-icons/archive/refs/tags/4.0.0.tar.gz"
tag = "4.0.0"
sha256 = ""  # Fill when first fetched

[license]
spdx = "Apache-2.0"
copyright = "Copyright (c) Google LLC"
upstream_license_url = "https://github.com/google/material-design-icons/blob/master/LICENSE"
modifications = "SVGs extracted and repackaged; names normalized to kebab-case; organized by variant"

[pack]
prefixes = ["material-icons", "mi"]
description = "Material Design Icons (Official) — 2500+ Google design system icons with 5 style variants"
source_url = "https://github.com/google/material-design-icons"
variants = ["filled", "outlined", "rounded", "sharp", "two-tone"]
default_variant = "outlined"
```

**Key changes from original design:**
- No `[extract]` section — extraction logic lives in per-pack `build.py` scripts
- No `repo` field — `url` contains the complete download URL directly
- No `url_template` — use concrete `url` values
- `variants` and `default_variant` are in `[pack]` section (documentation + runtime metadata)

### Download Cache

Each pack maintains a local `cache/` directory to avoid re-downloading upstream archives on every build:

- **Location**: `packs/<pack>/cache/`
- **Filename**: Derived from URL (e.g., `lucide-0.469.0.tar.gz`)
- **Validation**: Cache is validated using SHA-256 checksums from `upstream.toml`
- **Behavior**:
  - If cached file exists and SHA-256 matches, reuse cache (instant)
  - If cache miss or SHA-256 mismatch, download fresh copy to cache
  - Cache is `.gitignore`d (build artifacts only)
  - To force re-download, manually delete `cache/` directory

The `pack-tools` CLI provides generic build operations that work for all packs:
- Reads `upstream.toml` to get source URL and SHA-256
- Calls `download_with_cache()` to download to `packs/<pack>/cache/`
- Used by `just fetch <pack>` command

Per-pack `build.py` scripts read from cache (assume fetch already done) and do not download.

### Automated Version Checking

A GitHub Actions workflow (`check-upstream.yml`) runs weekly:

1. For each `packs/*/upstream.toml`, query the GitHub API for the latest release tag.
2. Compare against the pinned `tag` in `upstream.toml`.
3. If newer, open a PR that:
   - Updates `tag` and `sha256` in `upstream.toml`.
   - Bumps the pack version in `pyproject.toml`.
   - Triggers a test build to verify the new archive works.

This ensures we stay current without manual tracking.

---

## Directory Structure

```text
justmyresource-icons/
├── core/                           # justmyresource core library
│   ├── pyproject.toml
│   └── src/justmyresource/
│       ├── __init__.py
│       ├── core.py                 # ResourceRegistry
│       ├── types.py                # ResourcePack protocol, ResourceContent, etc.
│       └── pack_utils.py           # ZippedResourcePack base class
│
├── packs/                          # Icon pack packages
│   ├── lucide/                     # justmyresource-lucide
│   │   ├── pyproject.toml
│   │   ├── upstream.toml           # Upstream source config
│   │   ├── hatch_build.py          # Build hook (uses shared fetcher)
│   │   └── src/justmyresource_lucide/
│   │       ├── __init__.py         # Entry point factory
│   │       └── (icons.zip)         # Generated at build time, .gitignored
│   │
│   ├── material-official/          # justmyresource-material-icons
│   │   ├── pyproject.toml
│   │   ├── upstream.toml
│   │   ├── hatch_build.py
│   │   └── src/justmyresource_material_icons/
│   │       ├── __init__.py
│   │       └── (icons.zip)
│   │
│   ├── material-community/         # justmyresource-mdi
│   │   ├── pyproject.toml
│   │   ├── upstream.toml
│   │   ├── hatch_build.py
│   │   └── src/justmyresource_mdi/
│   │       ├── __init__.py
│   │       └── (icons.zip)
│   │
│   ├── phosphor/                   # justmyresource-phosphor
│   │   ├── pyproject.toml
│   │   ├── upstream.toml
│   │   ├── hatch_build.py
│   │   └── src/justmyresource_phosphor/
│   │       ├── __init__.py
│   │       └── (icons.zip)
│   │
│   ├── font-awesome/               # justmyresource-font-awesome
│   │   ├── pyproject.toml
│   │   ├── upstream.toml
│   │   ├── hatch_build.py
│   │   └── src/justmyresource_font_awesome/
│   │       ├── __init__.py
│   │       └── (icons.zip)
│   │
│   └── heroicons/                  # justmyresource-heroicons
│       ├── pyproject.toml
│       ├── upstream.toml
│       ├── hatch_build.py
│       └── src/justmyresource_heroicons/
│           ├── __init__.py
│           └── (icons.zip)
│
├── pack-tools/                     # Build tools package (justmyresource-pack-tools)
│   ├── pyproject.toml
│   ├── README.md
│   └── src/justmyresource_pack_tools/
│       ├── cli.py                  # CLI entry point (fetch/build/dist commands)
│       ├── config.py               # Load and parse upstream.toml
│       ├── download.py             # Download archives, SHA-256 verification, caching
│       ├── archive.py              # Unified archive reader (tar/zip)
│       ├── repack.py               # Create icon zip from entries
│       ├── manifest.py             # Generate pack_manifest.json
│       ├── normalize.py            # Name normalization (snake→kebab, etc.)
│       ├── readme.py                # README generation using Jinja2
│       ├── protocol.py             # PackBundler Protocol definition
│       └── templates/
│           └── readme.md.j2        # Jinja2 template for READMEs
│
├── scripts/                        # Dev scripts
│   ├── fetch_all.sh                # Pre-populate all packs for offline build
│   ├── check_upstream.py           # Version checking script
│   └── build_all.sh                # Build all wheels
│
├── .github/
│   └── workflows/
│       ├── test.yml                # CI: test core + all packs
│       ├── release.yml             # CD: build wheels, publish to PyPI
│       └── check-upstream.yml      # Weekly upstream version check
│
├── pyproject.toml                  # Root workspace config (Ruff/Mypy/Hatch)
└── .gitignore                      # Includes src/*/icons.zip, *.whl, etc.
```

---

## Phase 1: Repository Scaffolding & Shared Infrastructure

1. **Initialize Git Repository**
   - Create root directory.
   - Create `.gitignore` (standard Python + ignore `**/icons.zip`, `**/pack_manifest.json` build artifacts).

2. **Root Configuration**
   - Create root `pyproject.toml` defining the workspace members.
   - Configure shared linters (`ruff`) and type checking (`mypy`).

3. **Build Tools Package** (`pack-tools/`)
   - Installable as `justmyresource-pack-tools` package.
   - CLI commands: `fetch`, `build`, `dist`.
   - `config.py`: Load and parse `upstream.toml` with typed configuration classes.
   - `download.py`: Download archives from URLs, compute/verify SHA-256 checksums, caching support.
   - `archive.py`: Unified interface for reading tar and zip archives.
   - `repack.py`: Create `icons.zip` from entry iterators.
   - `manifest.py`: Generate `pack_manifest.json` from `upstream.toml` + extracted content (includes pack metadata: prefixes, variants, default_variant).
   - `normalize.py`: Name normalization (snake_case → kebab-case, etc.).
   - `readme.py`: Auto-generate per-pack READMEs using Jinja2 templates.
   - `protocol.py`: `PackBundler` Protocol definition for per-pack extraction logic.

## Phase 2: Core Library (`core/`)

1. **Migrate Core Code**
   - Initialize `core/pyproject.toml` (package name: `justmyresource`).
   - Copy existing `ResourceRegistry`, `ResourcePack` protocol, and types from the current `justmyresource` repo.

2. **Implement `ZippedResourcePack` Base Class** (`pack_utils.py`)
   - Accept `package_name` and `archive_name`.
   - Use `importlib.resources.files` to locate the zip and manifest.
   - Use `zipfile.ZipFile` to read SVGs directly from the archive (no extraction).
   - Implement `get_resource()`, `list_resources()`, `get_prefixes()`.
   - Support **variant resolution**: if zip contains `{variant}/{name}.svg`, resolve default variant transparently while allowing explicit `variant/name` access.
   - Expose `get_manifest()` → parsed `pack_manifest.json`.
   - **Auto-populate metadata**: If `prefixes` or `pack_info` not provided to `__init__`, read from `pack_manifest.json` (which includes `pack.prefixes`, `pack.description`, `pack.source_url`, `pack.upstream_license`).
   - Populate `ResourceContent.metadata` with variant, pack version, etc.

3. **Verify EntryPoints Logic**
   - Ensure `ResourceRegistry` correctly loads packs via `importlib.metadata`.

## Phase 3: Lucide Pack (Tier 1 — Proof of Concept)

1. **Project Setup**
   - Create `packs/lucide/pyproject.toml` (package name: `justmyresource-lucide`).
   - Create `packs/lucide/upstream.toml`.
   - Dependency: `justmyresource` (workspace path or version range).

2. **Build Script**
   - Create `packs/lucide/build.py` (pack-specific extraction logic).
   - Uses `pack-tools` CLI and library: `open_archive()`, `create_icon_zip()`, `generate_manifest()`.
   - **Assumes cache exists** (run `just fetch lucide` first).
   - Reads cached archive from `cache/` directory.
   - Reads `upstream.toml` via `UpstreamConfig.load()` for pack metadata.
   - Extracts SVGs according to pack's upstream layout, repacks into standard `icons.zip` structure.
   - Generates `icons.zip` + `pack_manifest.json` into `src/justmyresource_lucide/`.

3. **Package Implementation**
   - `src/justmyresource_lucide/__init__.py`: Minimal entry point factory returning `ZippedResourcePack(package_name="justmyresource_lucide")`.
   - `ZippedResourcePack` auto-populates `prefixes` and `PackInfo` from `pack_manifest.json` at runtime.
   - Register entry point: `justmyresource.packs` → `lucide`.

4. **Validation**
   - Test workflow: `just fetch lucide` → `just build lucide` → `just dist lucide`
   - Test: `registry.get_resource("lucide:home")` returns valid SVG.
   - Test: `pack.get_manifest()["pack"]["version"]` matches upstream tag.
   - Test: `list_resources()` returns expected count.

## Phase 4: Remaining Tier 1 Packs

### Material Icons (Official)
- **Challenge**: The upstream repo is ~4GB with fonts, PNGs, etc. The build hook must selectively extract only 24px SVGs for each variant.
- **Zip structure**: `{variant}/{name}.svg` (e.g., `outlined/settings.svg`).
- **Name normalization**: Google uses `snake_case` → normalize to `kebab-case`.
- **Test**: Verify 5 variants × core icon returns different SVGs.

### Material Design Icons (Community)
- **Source**: `@mdi/svg` npm tarball (clean flat SVG directory) or GitHub release.
- **Zip structure**: Flat `{name}.svg` (single variant).
- **Test**: Verify high icon count (7,000+), spot-check unusual names (`dishwasher`, `raspberry-pi`).

## Phase 5: Tier 2 Packs

### Phosphor Icons
- **Zip structure**: `{weight}/{name}.svg` (thin, light, regular, bold, fill, duotone).
- **Default**: `regular` weight.
- **Test**: Same icon name across all 6 weights returns different SVGs.

### Font Awesome (Free)
- **Zip structure**: `{style}/{name}.svg` (solid, regular, brands).
- **Default**: `solid` style.
- **License handling**: Include attribution notice in `pack_manifest.json` metadata.
- **Test**: `fa:brands/github` returns the GitHub logo SVG.

### Heroicons
- **Zip structure**: `{size}/{style}/{name}.svg` (24/outline, 24/solid, 20/solid, 16/solid).
- **Default**: `24/outline`.
- **Test**: `hero:24/solid/home` vs `hero:24/outline/home` return different SVGs.

## Phase 6: CI/CD & Verification

1. **Local Testing Script**
   - `scripts/build_all.sh`: Installs core editable, builds all packs, installs them, runs smoke tests.
   - `scripts/fetch_all.sh`: Downloads all upstream archives for offline development.

2. **GitHub Actions: Test** (`test.yml`)
   - Matrix strategy: test core + each pack independently.
   - For each pack: trigger build hook (needs network), run pack tests.
   - Shared test suite: every pack must pass `test_pack_contract.py` (get a known icon, list resources, check manifest).

3. **GitHub Actions: Release** (`release.yml`)
   - Build wheels for all packs.
   - Verify each wheel contains `icons.zip` + `pack_manifest.json`.
   - Publish to PyPI (each pack is an independent PyPI package).

4. **GitHub Actions: Upstream Check** (`check-upstream.yml`)
   - Weekly cron job.
   - For each `upstream.toml`, check GitHub API for latest release.
   - Open PR if update available, with changelog link and diff of icon count.

---

## Variant Resolution Design

Packs with variants (Material Official, Phosphor, Font Awesome, Heroicons) need a consistent resolution strategy.

### Zip Internal Structure

```
icons.zip
├── outlined/
│   ├── settings.svg
│   ├── home.svg
│   └── ...
├── filled/
│   ├── settings.svg
│   └── ...
└── ...
```

### Resolution Rules

1. **Bare name** (`mi:settings`): Resolves to `{default_variant}/settings.svg`.
2. **Explicit variant** (`mi:filled/settings`): Resolves to `filled/settings.svg`.
3. **List resources**: By default lists unique icon names (deduplicated across variants). With `include_variants=True`, lists `variant/name` forms.

### Metadata on ResourceContent

```python
content = registry.get_resource("mi:settings")
content.metadata == {
    "variant": "outlined",       # which variant was resolved
    "available_variants": ["filled", "outlined", "rounded", "sharp", "two-tone"],
    "pack_version": "4.0.0",
}
```

---

## PyPI Package Naming

| Directory | PyPI Package | Import Name | Entry Point Key |
|-----------|-------------|-------------|-----------------|
| `core/` | `justmyresource` | `justmyresource` | — |
| `packs/lucide/` | `justmyresource-lucide` | `justmyresource_lucide` | `lucide` |
| `packs/material-official/` | `justmyresource-material-icons` | `justmyresource_material_icons` | `material-icons` |
| `packs/material-community/` | `justmyresource-mdi` | `justmyresource_mdi` | `mdi` |
| `packs/phosphor/` | `justmyresource-phosphor` | `justmyresource_phosphor` | `phosphor` |
| `packs/font-awesome/` | `justmyresource-font-awesome` | `justmyresource_font_awesome` | `font-awesome` |
| `packs/heroicons/` | `justmyresource-heroicons` | `justmyresource_heroicons` | `heroicons` |

---

## Technical Constraints Checklist

- [ ] **No loose SVGs in Git**: `.gitignore` blocks `**/icons.zip` and `**/pack_manifest.json`.
- [ ] **Lazy Loading**: `zipfile` is not opened until `get_resource()` or `list_resources()` is called.
- [ ] **Deterministic builds**: SHA-256 of upstream archive is pinned in `upstream.toml` and verified at build time.
- [ ] **Name normalization**: All icon names are kebab-case regardless of upstream convention.
- [ ] **Variant defaults**: Each multi-variant pack has a documented default variant.
- [ ] **License compliance**: Each pack includes proper attribution (LICENSE/NOTICE files, manifest metadata).
- [ ] **Shared test contract**: All packs pass a common test suite verifying the `ResourcePack` protocol.
- [ ] **Prefix registration**:
  - Lucide: `lucide`, `luc`
  - Material Official: `material-icons`, `mi`
  - Material Community: `mdi`
  - Phosphor: `phosphor`, `ph`
  - Font Awesome: `font-awesome`, `fa`
  - Heroicons: `heroicons`, `hero`
