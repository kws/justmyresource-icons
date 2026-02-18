"""Name normalization utilities for icon packs.

This module provides functions for normalizing icon names across different
upstream conventions (snake_case, kebab-case, etc.).
"""

from __future__ import annotations


def to_kebab_case(name: str) -> str:
    """Convert name to kebab-case.

    Handles snake_case, PascalCase, camelCase, and other conventions.

    Args:
        name: Original name (may be snake_case, PascalCase, etc.).

    Returns:
        Name in kebab-case (e.g., "arrow-down", "alarm-clock-check").
    """
    import re

    # Remove file extension if present
    base_name = name
    if "." in name:
        parts = name.rsplit(".", 1)
        base_name = parts[0]
        extension = "." + parts[1]
    else:
        extension = ""

    # Convert underscores to hyphens
    result = base_name.replace("_", "-")

    # Insert hyphens before uppercase letters (PascalCase/camelCase)
    result = re.sub(r"([a-z])([A-Z])", r"\1-\2", result)

    # Collapse multiple consecutive hyphens
    result = re.sub(r"-+", "-", result)

    # Remove leading/trailing hyphens
    result = result.strip("-")

    # Lowercase everything
    result = result.lower()

    return result + extension


def strip_extension(name: str) -> str:
    """Remove file extension from name.

    Args:
        name: Name with or without extension.

    Returns:
        Name without extension.
    """
    if "." in name:
        return name.rsplit(".", 1)[0]
    return name


def add_extension(name: str, extension: str = ".svg") -> str:
    """Add file extension to name if not present.

    Args:
        name: Name with or without extension.
        extension: Extension to add (default: ".svg").

    Returns:
        Name with extension.
    """
    if not name.endswith(extension):
        return f"{name}{extension}"
    return name


