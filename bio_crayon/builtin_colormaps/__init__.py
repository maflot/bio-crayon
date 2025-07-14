"""
Built-in colormaps for BioCrayon.
"""

from pathlib import Path

# Get the path to this directory
BUILTIN_DIR = Path(__file__).parent


def get_builtin_colormap_path(name: str) -> Path:
    """
    Get the path to a built-in colormap file.

    Args:
        name: Name of the colormap file (without .json extension)

    Returns:
        Path to the colormap file

    Raises:
        FileNotFoundError: If the colormap file doesn't exist
    """
    filepath = BUILTIN_DIR / f"{name}.json"
    if not filepath.exists():
        available = [f.stem for f in BUILTIN_DIR.glob("*.json")]
        raise FileNotFoundError(
            f"Built-in colormap '{name}' not found. Available: {available}"
        )
    return filepath
