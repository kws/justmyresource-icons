"""JustMyResource pack for Heroicons."""

from __future__ import annotations

from justmyresource.pack_utils import ZippedResourcePack


class HeroiconsResourcePack(ZippedResourcePack):
    """Resource pack for Heroicons.

    Provides access to 300+ SVG icons from Tailwind Labs, organized by
    size (16, 20, 24) and style (outline, solid).
    """

    def _normalize_name(self, name: str) -> str:
        """Normalize resource name for lookup in zip.

        Supports size/style prefixes like "24/outline/home" or "24/solid/home"
        or bare names which default to "24/outline".

        Args:
            name: Resource name from user.

        Returns:
            Normalized name with size/style prefix and .svg extension.
        """
        if not name.endswith(".svg"):
            name = f"{name}.svg"
        # If no size/style prefix, add default
        if "/" not in name:
            name = f"24/outline/{name}"
        return name


def get_resource_provider():
    """Entry point factory for JustMyResource.

    Returns:
        HeroiconsResourcePack instance.
    """
    return HeroiconsResourcePack(package_name="justmyresource_heroicons")
