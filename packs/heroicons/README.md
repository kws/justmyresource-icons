<!-- This file is auto-generated from upstream.toml. Do not edit manually. -->

# Heroicons

Heroicons — 300+ Tailwind-aligned SVG icons

## Installation

```bash
pip install justmyresource-heroicons
```

## Usage

```python
from justmyresource import ResourceRegistry

registry = ResourceRegistry()
content = registry.get_resource("heroicons:icon-name")
print(content.text)  # SVG content
```

## Prefixes

This pack can be accessed using the following prefixes:

- `heroicons` (primary)

- `hero` (alias)



## Variants


This pack includes the following variants:

- `24/outline` (default)

- `24/solid`

- `20/solid`

- `16/solid`


To access a specific variant, use the format `heroicons:variant/icon-name`:

```python
# Access default variant (24/outline)
content = registry.get_resource("heroicons:icon-name")

# Access specific variant
content = registry.get_resource("heroicons:24/outline/icon-name")
```


## License

- **Upstream License**: MIT
- **Copyright**: Copyright (c) Tailwind Labs
- **Upstream Source**: https://heroicons.com

For full license details, see the [LICENSE](../LICENSE) file.

## Upstream

This pack bundles icons from:
- **Source**: https://heroicons.com
- **Version**: v2.2.0

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

