<!-- This file is auto-generated from upstream.toml. Do not edit manually. -->

# Material Official

Material Design Icons (Official) — 2500+ Google design system icons with 5 style variants

## Installation

```bash
pip install justmyresource-material-icons
```

## Usage

```python
from justmyresource import ResourceRegistry

registry = ResourceRegistry()
content = registry.get_resource("material-icons:icon-name")
print(content.text)  # SVG content
```

## Prefixes

This pack can be accessed using the following prefixes:

- `material-icons` (primary)

- `mi` (alias)



## Variants


This pack includes the following variants:

- `filled`

- `outlined` (default)

- `rounded`

- `sharp`

- `two-tone`


To access a specific variant, use the format `material-icons:variant/icon-name`:

```python
# Access default variant (outlined)
content = registry.get_resource("material-icons:icon-name")

# Access specific variant
content = registry.get_resource("material-icons:filled/icon-name")
```


## License

- **Upstream License**: Apache-2.0
- **Copyright**: Copyright (c) Google LLC
- **Upstream Source**: https://github.com/google/material-design-icons

For full license details, see the [LICENSE](../LICENSE) file.

## Upstream

This pack bundles icons from:
- **Source**: https://github.com/google/material-design-icons
- **Version**: 4.0.0

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

