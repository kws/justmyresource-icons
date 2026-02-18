<!-- This file is auto-generated from upstream.toml. Do not edit manually. -->

# Font Awesome

Font Awesome Free — 2000+ industry standard icons (solid, regular, brands)

## Installation

```bash
pip install justmyresource-font-awesome
```

## Usage

```python
from justmyresource import ResourceRegistry

registry = ResourceRegistry()
content = registry.get_resource("font-awesome:icon-name")
print(content.text)  # SVG content
```

## Prefixes

This pack can be accessed using the following prefixes:

- `font-awesome` (primary)

- `fa` (alias)



## Variants


This pack includes the following variants:

- `solid` (default)

- `regular`

- `brands`


To access a specific variant, use the format `font-awesome:variant/icon-name`:

```python
# Access default variant (solid)
content = registry.get_resource("font-awesome:icon-name")

# Access specific variant
content = registry.get_resource("font-awesome:solid/icon-name")
```


## License

- **Upstream License**: CC-BY-4.0
- **Copyright**: Copyright (c) Fonticons, Inc.
- **Upstream Source**: https://fontawesome.com

For full license details, see the [LICENSE](../LICENSE) file.

## Upstream

This pack bundles icons from:
- **Source**: https://fontawesome.com
- **Version**: 6.7.2

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

