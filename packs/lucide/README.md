<!-- This file is auto-generated from upstream.toml. Do not edit manually. -->

# Lucide

Lucide icon library — 1500+ minimalist SVG icons

## Installation

```bash
pip install justmyresource-lucide
```

## Usage

```python
from justmyresource import ResourceRegistry

registry = ResourceRegistry()
content = registry.get_resource("lucide:icon-name")
print(content.text)  # SVG content
```

## Prefixes

This pack can be accessed using the following prefixes:

- `lucide` (primary)

- `luc` (alias)



## Variants


This pack has a single variant. Icons can be accessed directly:

```python
content = registry.get_resource("lucide:icon-name")
```


## License

- **Upstream License**: ISC
- **Copyright**: Copyright (c) Lucide Contributors
- **Upstream Source**: https://lucide.dev

For full license details, see the [LICENSE](../LICENSE) file.

## Upstream

This pack bundles icons from:
- **Source**: https://lucide.dev
- **Version**: 0.575.0

## Development

To build this pack from source:

```bash
# 1. Fetch upstream archive (downloads to cache/)
pack-tools fetch <pack-name>

# 2. Build icons.zip and manifest (processes from cache)
pack-tools build <pack-name>

# 3. Create distribution wheel
pack-tools dist <pack-name>
```

The cache persists across builds. To force a fresh download, delete the `cache/` directory.

