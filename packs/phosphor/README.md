<!-- This file is auto-generated from upstream.toml. Do not edit manually. -->

# Phosphor

Phosphor Icons — 1200+ flexible weight system icons

## Installation

```bash
pip install justmyresource-phosphor
```

## Usage

```python
from justmyresource import ResourceRegistry

registry = ResourceRegistry()
content = registry.get_resource("phosphor:icon-name")
print(content.text)  # SVG content
```

## Prefixes

This pack can be accessed using the following prefixes:

- `phosphor` (primary)

- `ph` (alias)



## Variants


This pack includes the following variants:

- `thin`

- `light`

- `regular` (default)

- `bold`

- `fill`

- `duotone`


To access a specific variant, use the format `phosphor:variant/icon-name`:

```python
# Access default variant (regular)
content = registry.get_resource("phosphor:icon-name")

# Access specific variant
content = registry.get_resource("phosphor:thin/icon-name")
```


## License

- **Upstream License**: MIT
- **Copyright**: Copyright (c) Phosphor Icons
- **Upstream Source**: https://github.com/phosphor-icons/core

For full license details, see the [LICENSE](../LICENSE) file.

## Upstream

This pack bundles icons from:
- **Source**: https://github.com/phosphor-icons/core
- **Version**: v2.0.8

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

