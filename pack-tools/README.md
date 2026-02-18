# justmyresource-pack-tools

Build tools for creating JustMyResource icon packs.

## Installation

```bash
pip install justmyresource-pack-tools
```

Or install from source:

```bash
cd pack-tools
pip install -e .
```

## Usage

The tool provides a CLI for building icon packs:

```bash
# Fetch upstream archive to cache/
pack-tools fetch packs/lucide

# Build: run per-pack bundler, generate icons.zip + manifest + README
pack-tools build packs/lucide

# Dist: build wheel
pack-tools dist packs/lucide
```

## Pack Structure

Each pack directory should contain:

- `upstream.toml` - Pack configuration (source URL, license, metadata)
- `pack.py` - Per-pack extraction logic implementing the `PackBundler` protocol
- `cache/` - Directory for cached upstream archives (created by `fetch`)

## Protocol

Packs implement the `PackBundler` protocol by providing an `extract` function:

```python
from justmyresource_pack_tools.archive import ArchiveReader
from justmyresource_pack_tools.config import UpstreamConfig
from justmyresource_pack_tools.repack import ZipEntry
from collections.abc import Iterator

def extract(archive: ArchiveReader, config: UpstreamConfig) -> Iterator[ZipEntry]:
    """Extract icons from upstream archive into standardized ZipEntry items."""
    # Pack-specific extraction logic here
    ...
```

