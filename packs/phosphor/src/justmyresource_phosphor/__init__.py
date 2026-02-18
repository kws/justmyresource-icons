"""JustMyResource pack for Phosphor Icons."""

from __future__ import annotations

from justmyresource.pack_utils import ZippedResourcePack


class PhosphorResourcePack(ZippedResourcePack):
    """Resource pack for Phosphor Icons.

    Provides access to 1200+ SVG icons with flexible weight system:
    thin, light, regular, bold, fill, and duotone.
    """

    def _normalize_name(self, name: str) -> str:
        """Normalize resource name for lookup in zip.

        Supports weight prefixes like "bold/arrow-right" or bare names
        which default to the regular weight.

        Args:
            name: Resource name from user.

        Returns:
            Normalized name with weight prefix and .svg extension.
        """
        if not name.endswith(".svg"):
            name = f"{name}.svg"
        # If no weight prefix, add default weight
        if "/" not in name:
            name = f"regular/{name}"
        return name


def get_resource_provider():
    """Entry point factory for JustMyResource.

    Returns:
        PhosphorResourcePack instance.
    """
    return PhosphorResourcePack(package_name="justmyresource_phosphor")
