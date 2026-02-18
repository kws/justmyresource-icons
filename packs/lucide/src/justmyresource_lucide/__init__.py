"""JustMyResource pack for Lucide icons."""

from __future__ import annotations

from justmyresource.pack_utils import ZippedResourcePack


class LucideResourcePack(ZippedResourcePack):
    """Resource pack for Lucide icons.

    Provides access to 1500+ SVG icons from the Lucide icon library.
    """

    def _normalize_name(self, name: str) -> str:
        """Normalize resource name for lookup in zip.

        Args:
            name: Resource name from user.

        Returns:
            Normalized name with .svg extension.
        """
        if not name.endswith(".svg"):
            return f"{name}.svg"
        return name


def get_resource_provider():
    """Entry point factory for JustMyResource.

    Returns:
        LucideResourcePack instance.
    """
    return LucideResourcePack(package_name="justmyresource_lucide")
