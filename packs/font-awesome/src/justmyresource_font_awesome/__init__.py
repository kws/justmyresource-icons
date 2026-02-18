"""JustMyResource pack for Font Awesome Free icons."""

from __future__ import annotations

from justmyresource.pack_utils import ZippedResourcePack


class FontAwesomeResourcePack(ZippedResourcePack):
    """Resource pack for Font Awesome Free icons.

    Provides access to 2000+ SVG icons from Font Awesome Free:
    solid, regular, and brands styles.

    Note: Font Awesome Free icons are licensed under CC BY 4.0.
    Attribution is required - see LICENSES/FONT-AWESOME-ATTRIBUTION.
    """

    def _normalize_name(self, name: str) -> str:
        """Normalize resource name for lookup in zip.

        Supports style prefixes like "solid/heart" or "brands/github" or bare names
        which default to the solid style.

        Args:
            name: Resource name from user.

        Returns:
            Normalized name with style prefix and .svg extension.
        """
        if not name.endswith(".svg"):
            name = f"{name}.svg"
        # If no style prefix, add default style
        if "/" not in name:
            name = f"solid/{name}"
        return name


def get_resource_provider():
    """Entry point factory for JustMyResource.

    Returns:
        FontAwesomeResourcePack instance.
    """
    return FontAwesomeResourcePack(package_name="justmyresource_font_awesome")
