"""JustMyResource pack for Material Design Icons (Official)."""

from __future__ import annotations

from justmyresource.pack_utils import ZippedResourcePack


class MaterialIconsResourcePack(ZippedResourcePack):
    """Resource pack for Material Design Icons (Official).

    Provides access to 2500+ SVG icons from Google's Material Design icon set
    with 5 style variants: filled, outlined, rounded, sharp, and two-tone.
    """

    def _normalize_name(self, name: str) -> str:
        """Normalize resource name for lookup in zip.

        Supports variant prefixes like "outlined/settings" or bare names
        which default to the outlined variant.

        Args:
            name: Resource name from user.

        Returns:
            Normalized name with variant prefix and .svg extension.
        """
        if not name.endswith(".svg"):
            name = f"{name}.svg"
        # If no variant prefix, add default variant
        if "/" not in name:
            name = f"outlined/{name}"
        return name


def get_resource_provider():
    """Entry point factory for JustMyResource.

    Returns:
        MaterialIconsResourcePack instance.
    """
    return MaterialIconsResourcePack(package_name="justmyresource_material_icons")
