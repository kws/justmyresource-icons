<!-- This file is auto-generated from upstream.toml. Do not edit manually. -->

# Material Community

Material Design Icons (Community) — 7000+ icons from the Pictogrammers community

## Installation

```bash
pip install justmyresource-mdi
```

## Usage

```python
from justmyresource import ResourceRegistry

registry = ResourceRegistry()
content = registry.get_resource("mdi:icon-name")
print(content.text)  # SVG content
```

## Prefixes

This pack can be accessed using the following prefixes:

- `mdi`


## Variants


This pack has a single variant. Icons can be accessed directly:

```python
content = registry.get_resource("mdi:icon-name")
```


## License

- **Upstream License**: Apache-2.0
- **Copyright**: Copyright (c) Pictogrammers
- **Upstream Source**: https://github.com/Templarian/MaterialDesign

For full license details, see the [LICENSE](../LICENSE) file.

## Upstream

This pack bundles icons from:
- **Source**: https://github.com/Templarian/MaterialDesign
- **Version**: 7.4.47

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

