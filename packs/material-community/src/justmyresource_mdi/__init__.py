"""JustMyResource pack for Material Design Icons (Community / Pictogrammers)."""

from __future__ import annotations

from justmyresource.pack_utils import ZippedResourcePack


class MDIResourcePack(ZippedResourcePack):
    """Resource pack for Material Design Icons (Community).

    Provides access to 7000+ SVG icons from the Pictogrammers community.
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
        MDIResourcePack instance.
    """
    return MDIResourcePack(package_name="justmyresource_mdi")
