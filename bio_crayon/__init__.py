"""
BioCrayon - A Python package for managing biological data colormaps.

This package provides tools for loading, validating, and using colormaps
specifically designed for biological data visualization.
"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("bio-crayon")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

__author__ = "Matthias Flotho"
__email__ = "matthias.flotho@ccb.uni-saarland.de"

from .core import BioCrayon
from .utils import hex_to_rgb, rgb_to_hex, interpolate_colors
from .validators import validate_colormap_data

__all__ = [
    "BioCrayon",
    "hex_to_rgb",
    "rgb_to_hex",
    "interpolate_colors",
    "validate_colormap_data",
]
