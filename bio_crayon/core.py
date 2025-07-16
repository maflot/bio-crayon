"""
Core BioCrayon class for managing biological data colormaps.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Union, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import requests

from .utils import (
    load_from_file,
    load_from_url,
    load_from_dict,
    detect_source_type,
    hex_to_rgb,
    rgb_to_hex,
    interpolate_colors,
    normalize_color,
    interpolate_color_lab,
    is_colorblind_safe,
    get_colorblind_safe_colors,
)
from .validators import (
    validate_colormap_data,
    validate_colormap_name,
    validate_hex_color,
    validate_categorical_colormap,
    validate_continuous_colormap,
    validate_expression_range,
    validate_colorblind_safety,
    validate_bio_specific_requirements,
)


class ColormapAccessor:
    """
    Helper class to provide intuitive bracket access to colormaps.

    Allows syntax like: bc["sex"]["M"] or bc["sex"].keys()
    """

    def __init__(self, biocrayon: "BioCrayon", colormap_name: str):
        self.biocrayon = biocrayon
        self.colormap_name = colormap_name
        self._colormap = biocrayon.get_colormap(colormap_name)
        self._fill_missing = False
        self._default_color = "#CCCCCC"

    def __getitem__(self, key: Union[str, float]) -> str:
        """Get color for key (category or value)."""
        return self.biocrayon.get_color(
            self.colormap_name,
            key,
            fill_missing=self._fill_missing,
            default_color=self._default_color,
        )

    def __contains__(self, key: Union[str, float]) -> bool:
        """Check if key exists in colormap."""
        if self._colormap["type"] == "categorical":
            return key in self._colormap["colors"]
        else:
            # For continuous, check if value is in range
            positions = self._colormap["positions"]
            return positions[0] <= key <= positions[-1]

    def keys(self):
        """Get all categories (for categorical colormaps)."""
        if self._colormap["type"] == "categorical":
            return self._colormap["colors"].keys()
        else:
            raise AttributeError("keys() only available for categorical colormaps")

    def values(self):
        """Get all colors (for categorical colormaps)."""
        if self._colormap["type"] == "categorical":
            return self._colormap["colors"].values()
        else:
            raise AttributeError("values() only available for categorical colormaps")

    def items(self):
        """Get all category-color pairs (for categorical colormaps)."""
        if self._colormap["type"] == "categorical":
            return self._colormap["colors"].items()
        else:
            raise AttributeError("items() only available for categorical colormaps")

    def get(self, key: Union[str, float], default=None):
        """Get color with default value if key doesn't exist."""
        try:
            return self.__getitem__(key)
        except (KeyError, ValueError):
            return default

    def set_fill_missing(
        self, fill_missing: bool = True, default_color: str = "#CCCCCC"
    ):
        """
        Configure whether to automatically assign colors for missing categories.

        Args:
            fill_missing: If True, automatically assign colors for missing categories
            default_color: Default color to use for missing values
        """
        self._fill_missing = fill_missing
        self._default_color = default_color
        return self

    def __repr__(self):
        colormap_type = self._colormap["type"]
        if colormap_type == "categorical":
            categories = list(self._colormap["colors"].keys())
            fill_status = " (fill_missing=True)" if self._fill_missing else ""
            return f"ColormapAccessor('{self.colormap_name}', categories={categories}){fill_status}"
        else:
            positions = self._colormap["positions"]
            return f"ColormapAccessor('{self.colormap_name}', range=[{positions[0]}, {positions[-1]}])"

    def to_list(self) -> List[str]:
        """Convert to list of colors (for pandas compatibility)."""
        if self._colormap["type"] == "categorical":
            return list(self._colormap["colors"].values())
        else:
            raise AttributeError("to_list() only available for categorical colormaps")

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary mapping categories to colors."""
        if self._colormap["type"] == "categorical":
            return dict(self._colormap["colors"])
        else:
            raise AttributeError("to_dict() only available for categorical colormaps")

    def __len__(self) -> int:
        """Return number of colors."""
        if self._colormap["type"] == "categorical":
            return len(self._colormap["colors"])
        else:
            return len(self._colormap["colors"])

    def __iter__(self):
        """Iterate over colors (for pandas compatibility)."""
        if self._colormap["type"] == "categorical":
            return iter(self._colormap["colors"].values())
        else:
            return iter(self._colormap["colors"])


class BioCrayon:
    """
    Main class for managing biological data colormaps.

    Supports loading colormaps from files, URLs, or dictionaries,
    and provides methods for accessing and converting colormaps.
    """

    def __init__(
        self,
        source: Optional[Union[str, Path, Dict[str, Any]]] = None,
        require_metadata: bool = False,
    ):
        """
        Initialize BioCrayon with optional source.

        Args:
            source: File path, URL, or dictionary containing colormap data
            require_metadata: Whether metadata is required (True for community colormaps)
        """
        self._data = {"metadata": {}, "colormaps": {}}
        self._metadata = {}
        self._colormaps = {}

        if source is not None:
            self.load(source, require_metadata=require_metadata)

    def load(
        self, source: Union[str, Path, Dict[str, Any]], require_metadata: bool = False
    ) -> None:
        """
        Load colormap data from source.

        Args:
            source: File path, URL, or dictionary containing colormap data
            require_metadata: Whether metadata is required (True for community colormaps)

        Raises:
            ValueError: If source is invalid or validation fails
            FileNotFoundError: If file doesn't exist
            requests.RequestException: If URL request fails
        """
        source_type = detect_source_type(source)

        if source_type == "file":
            data = load_from_file(source)
        elif source_type == "url":
            data = load_from_url(source)
        else:  # dict
            data = load_from_dict(source)

        # Validate the data
        errors = validate_colormap_data(data, require_metadata=require_metadata)
        if errors:
            raise ValueError(f"Invalid colormap data:\n" + "\n".join(errors))

        # Store the data
        self._data = data
        self._metadata = data.get("metadata", {})
        self._colormaps = data.get("colormaps", {})

    def get_colormap(self, name: str) -> Dict[str, Any]:
        """
        Get a specific colormap by name.

        Args:
            name: Name of the colormap

        Returns:
            Dictionary containing colormap data

        Raises:
            KeyError: If colormap doesn't exist
        """
        if name not in self._colormaps:
            available = list(self._colormaps.keys())
            raise KeyError(f"Colormap '{name}' not found. Available: {available}")

        return self._colormaps[name]

    def get_color(
        self,
        colormap_name: str,
        key_or_value: Union[str, float],
        fill_missing: bool = False,
        default_color: str = "#CCCCCC",
    ) -> str:
        """
        Get color for categorical key or continuous value.

        Args:
            colormap_name: Name of the colormap
            key_or_value: Category name (for categorical) or value (for continuous)
            fill_missing: If True, automatically assign colors for missing categories
            default_color: Default color to use for missing values (default: "#CCCCCC")

        Returns:
            Hex color string

        Raises:
            KeyError: If colormap doesn't exist and fill_missing is False
            ValueError: If value is out of range for continuous colormap
        """
        colormap = self.get_colormap(colormap_name)
        colormap_type = colormap["type"]

        if colormap_type == "categorical":
            colors = colormap["colors"]

            # Handle NaN/nan values
            if key_or_value in [None, "NaN", "nan", "NAN", "Nan"]:
                return default_color

            # Handle missing categories
            if key_or_value not in colors:
                if fill_missing:
                    # Auto-assign a color for missing category
                    return self._assign_color_for_missing_category(
                        colormap_name, key_or_value, colors
                    )
                else:
                    available = list(colors.keys())
                    raise KeyError(
                        f"Category '{key_or_value}' not found in colormap '{colormap_name}'. Available: {available}"
                    )
            return colors[key_or_value]

        elif colormap_type == "continuous":
            colors = colormap["colors"]
            positions = colormap["positions"]

            # Handle NaN/nan values for continuous colormaps
            if key_or_value in [None, "NaN", "nan", "NAN", "Nan"]:
                return default_color

            if not isinstance(key_or_value, (int, float)):
                raise ValueError(
                    f"Value must be numeric for continuous colormap: {key_or_value}"
                )

            value = float(key_or_value)

            # Handle edge cases
            if value <= positions[0]:
                return colors[0]
            if value >= positions[-1]:
                return colors[-1]

            # Find the appropriate segment
            for i in range(len(positions) - 1):
                if positions[i] <= value <= positions[i + 1]:
                    # Interpolate between colors
                    t = (value - positions[i]) / (positions[i + 1] - positions[i])
                    color1 = colors[i]
                    color2 = colors[i + 1]

                    # Simple linear interpolation
                    rgb1 = hex_to_rgb(color1)
                    rgb2 = hex_to_rgb(color2)

                    r = int(round(rgb1[0] * (1 - t) + rgb2[0] * t))
                    g = int(round(rgb1[1] * (1 - t) + rgb2[1] * t))
                    b = int(round(rgb1[2] * (1 - t) + rgb2[2] * t))

                    return rgb_to_hex(r, g, b)

            # Should not reach here
            raise ValueError(f"Could not interpolate value {value}")

        else:
            raise ValueError(f"Unknown colormap type: {colormap_type}")

    def _assign_color_for_missing_category(
        self, colormap_name: str, category: str, existing_colors: Dict[str, str]
    ) -> str:
        """
        Assign a color for a missing category.

        Args:
            colormap_name: Name of the colormap
            category: The missing category
            existing_colors: Dictionary of existing category-color mappings

        Returns:
            Hex color string for the missing category
        """
        # Get colorblind-safe colors
        from .utils import get_colorblind_safe_colors

        # Count how many colors we need (existing + 1 for the new category)
        n_needed = len(existing_colors) + 1

        # Get colorblind-safe colors
        safe_colors = get_colorblind_safe_colors(n_needed)

        # Find the first color that's not already used
        for color in safe_colors:
            if color not in existing_colors.values():
                # Add the new category-color mapping to the colormap
                self._colormaps[colormap_name]["colors"][category] = color
                return color

        # If all safe colors are used, generate a new one
        # Use a simple algorithm to generate a distinct color
        used_colors = set(existing_colors.values())

        # Try different hues to find a distinct color
        for hue in range(0, 360, 30):  # Every 30 degrees
            # Convert HSV to RGB
            from .utils import hsv_to_rgb, rgb_to_hex

            rgb = hsv_to_rgb(hue, 0.7, 0.8)  # Saturation 0.7, Value 0.8
            new_color = rgb_to_hex(*rgb)

            if new_color not in used_colors:
                # Add the new category-color mapping to the colormap
                self._colormaps[colormap_name]["colors"][category] = new_color
                return new_color

        # Fallback: use a gray color
        fallback_color = "#CCCCCC"
        self._colormaps[colormap_name]["colors"][category] = fallback_color
        return fallback_color

    def list_colormaps(self) -> List[str]:
        """
        List available colormaps.

        Returns:
            List of colormap names
        """
        return list(self._colormaps.keys())

    def to_matplotlib(
        self, colormap_name: str, n_colors: int = 256
    ) -> mcolors.Colormap:
        """
        Convert colormap to matplotlib Colormap object.

        Args:
            colormap_name: Name of the colormap
            n_colors: Number of colors in the matplotlib colormap

        Returns:
            matplotlib.colors.Colormap object

        Raises:
            KeyError: If colormap doesn't exist
            ValueError: If colormap type is not supported for matplotlib conversion
        """
        colormap = self.get_colormap(colormap_name)
        colormap_type = colormap["type"]

        if colormap_type == "continuous":
            colors = colormap["colors"]
            positions = colormap["positions"]

            # Convert hex colors to RGB (0-1 range)
            rgb_colors = []
            for color in colors:
                r, g, b = hex_to_rgb(color)
                rgb_colors.append([r / 255, g / 255, b / 255])

            # Create matplotlib colormap
            cmap = mcolors.LinearSegmentedColormap.from_list(
                colormap_name, list(zip(positions, rgb_colors)), N=n_colors
            )
            return cmap

        elif colormap_type == "categorical":
            colors = colormap["colors"]

            # For categorical, create a discrete colormap
            color_list = list(colors.values())
            rgb_colors = []
            for color in color_list:
                r, g, b = hex_to_rgb(color)
                rgb_colors.append([r / 255, g / 255, b / 255])

            # Create discrete colormap
            cmap = mcolors.ListedColormap(rgb_colors, name=colormap_name)
            return cmap

        else:
            raise ValueError(
                f"Cannot convert colormap type '{colormap_type}' to matplotlib"
            )

    def add_colormap(self, name: str, colormap_data: Dict[str, Any]) -> None:
        """
        Add a new colormap.

        Args:
            name: Name for the new colormap
            colormap_data: Dictionary containing colormap data

        Raises:
            ValueError: If name is invalid or colormap data is invalid
        """
        if not validate_colormap_name(name):
            raise ValueError(f"Invalid colormap name: {name}")

        if name in self._colormaps:
            raise ValueError(f"Colormap '{name}' already exists")

        # Validate the colormap data
        if "type" not in colormap_data:
            raise ValueError("Colormap data must have 'type' field")

        colormap_type = colormap_data["type"]
        if colormap_type == "categorical":
            errors = validate_categorical_colormap(colormap_data)
        elif colormap_type == "continuous":
            errors = validate_continuous_colormap(colormap_data)
        else:
            raise ValueError(f"Unknown colormap type: {colormap_type}")

        if errors:
            raise ValueError(f"Invalid colormap data:\n" + "\n".join(errors))

        # Add the colormap
        self._colormaps[name] = colormap_data
        self._data["colormaps"] = self._colormaps

    def save(self, filepath: Union[str, Path], require_metadata: bool = False) -> None:
        """
        Save current colormaps to file.

        Args:
            filepath: Path to save the JSON file
            require_metadata: Whether metadata is required (True for community colormaps)

        Raises:
            ValueError: If data is invalid
        """
        # Validate the complete data structure
        errors = validate_colormap_data(self._data, require_metadata=require_metadata)
        if errors:
            raise ValueError(f"Invalid data structure:\n" + "\n".join(errors))

        filepath = Path(filepath)
        with open(filepath, "w") as f:
            json.dump(self._data, f, indent=2)

    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the colormap collection.

        Returns:
            Dictionary containing metadata
        """
        return self._metadata.copy()

    def get_colormap_info(self, name: str) -> Dict[str, Any]:
        """
        Get information about a specific colormap.

        Args:
            name: Name of the colormap

        Returns:
            Dictionary containing colormap information

        Raises:
            KeyError: If colormap doesn't exist
        """
        colormap = self.get_colormap(name)
        info = {
            "name": name,
            "type": colormap["type"],
            "description": colormap.get("description", ""),
        }

        if colormap["type"] == "categorical":
            info["categories"] = list(colormap["colors"].keys())
            info["num_categories"] = len(colormap["colors"])
        else:  # continuous
            info["num_colors"] = len(colormap["colors"])
            info["range"] = (colormap["positions"][0], colormap["positions"][-1])
            info["interpolation"] = colormap.get("interpolation", "linear")

        return info

    def plot_colormap(self, name: str, figsize: Tuple[int, int] = (8, 2)) -> None:
        """
        Plot a colormap for visualization.

        Args:
            name: Name of the colormap
            figsize: Figure size (width, height)

        Raises:
            KeyError: If colormap doesn't exist
        """
        colormap = self.get_colormap(name)
        colormap_type = colormap["type"]

        fig, ax = plt.subplots(figsize=figsize)

        if colormap_type == "categorical":
            colors = colormap["colors"]
            categories = list(colors.keys())
            color_values = list(colors.values())

            # Create color patches
            for i, (category, color) in enumerate(zip(categories, color_values)):
                ax.bar(i, 1, color=color, label=category)

            ax.set_xlabel("Categories")
            ax.set_ylabel("Color")
            ax.set_title(f"Categorical Colormap: {name}")
            ax.set_xticks(range(len(categories)))
            ax.set_xticklabels(categories, rotation=45)
            ax.legend()

        else:  # continuous
            colors = colormap["colors"]
            positions = colormap["positions"]

            # Create gradient
            for i in range(len(positions) - 1):
                x_start = positions[i]
                x_end = positions[i + 1]
                color_start = colors[i]
                color_end = colors[i + 1]

                # Interpolate colors for smooth gradient
                n_steps = 50
                for j in range(n_steps):
                    t = j / n_steps
                    x = x_start + t * (x_end - x_start)

                    # Interpolate color
                    rgb1 = hex_to_rgb(color_start)
                    rgb2 = hex_to_rgb(color_end)
                    r = int(rgb1[0] + t * (rgb2[0] - rgb1[0]))
                    g = int(rgb1[1] + t * (rgb2[1] - rgb1[1]))
                    b = int(rgb1[2] + t * (rgb2[2] - rgb1[2]))
                    color = rgb_to_hex(r, g, b)

                    ax.bar(x, 1, color=color, width=(x_end - x_start) / n_steps)

            ax.set_xlabel("Position")
            ax.set_ylabel("Color")
            ax.set_title(f"Continuous Colormap: {name}")
            ax.set_xlim(0, 1)

        plt.tight_layout()
        plt.show()

    def __len__(self) -> int:
        """Return number of colormaps."""
        return len(self._colormaps)

    def __contains__(self, name: str) -> bool:
        """Check if colormap exists."""
        return name in self._colormaps

    def __iter__(self):
        """Iterate over colormap names."""
        return iter(self._colormaps.keys())

    def __getitem__(
        self, colormap_name: str
    ) -> Union[Dict[str, str], ColormapAccessor]:
        """
        Get colormap data for intuitive bracket notation.

        For categorical colormaps: returns the colors dictionary directly
        For continuous colormaps: returns a ColormapAccessor object

        Allows syntax like: bc["sex"]["M"] or bc["sex"].keys() for categorical
        or bc["expression"][0.5] for continuous

        Args:
            colormap_name: Name of the colormap

        Returns:
            Dictionary of category-color mappings for categorical colormaps,
            or ColormapAccessor object for continuous colormaps

        Raises:
            KeyError: If colormap doesn't exist
        """
        if colormap_name not in self._colormaps:
            available = list(self._colormaps.keys())
            raise KeyError(
                f"Colormap '{colormap_name}' not found. Available: {available}"
            )

        colormap = self._colormaps[colormap_name]

        if colormap["type"] == "categorical":
            # Return the colors dictionary directly for categorical colormaps
            return colormap["colors"]
        else:
            # Return ColormapAccessor for continuous colormaps
            return ColormapAccessor(self, colormap_name)

    def validate_expression_range(
        self, colormap_name: str, min_val: float, max_val: float
    ) -> List[str]:
        """
        Validate that a continuous colormap covers the expected expression range.

        Args:
            colormap_name: Name of the colormap to validate
            min_val: Expected minimum value in the data
            max_val: Expected maximum value in the data

        Returns:
            List of validation error messages (empty if valid)

        Raises:
            KeyError: If colormap doesn't exist
        """
        colormap = self.get_colormap(colormap_name)
        return validate_expression_range(colormap, min_val, max_val)

    def is_colorblind_safe(
        self, colormap_name: str, colorblind_type: str = "deuteranopia"
    ) -> bool:
        """
        Check if categorical colormap is distinguishable for colorblind users.

        Args:
            colormap_name: Name of the colormap to check
            colorblind_type: Type of colorblindness to check for

        Returns:
            True if colors are distinguishable for the specified colorblind type

        Raises:
            KeyError: If colormap doesn't exist
        """
        colormap = self.get_colormap(colormap_name)
        if colormap["type"] != "categorical":
            raise ValueError(
                f"Colorblind safety check only applies to categorical colormaps, got {colormap['type']}"
            )

        colors = list(colormap["colors"].values())
        return is_colorblind_safe(colors, colorblind_type)

    def get_colorbar(self, colormap_name: str, **kwargs) -> plt.Figure:
        """
        Return matplotlib colorbar for the colormap.

        Args:
            colormap_name: Name of the colormap
            **kwargs: Additional arguments passed to matplotlib.colorbar.Colorbar

        Returns:
            matplotlib Figure with colorbar

        Raises:
            KeyError: If colormap doesn't exist
        """
        colormap = self.get_colormap(colormap_name)
        colormap_type = colormap["type"]

        # Extract and remove figsize from kwargs if present
        figsize = kwargs.pop("figsize", (1, 6))

        # Create a simple figure with colorbar
        fig, ax = plt.subplots(figsize=figsize)

        if colormap_type == "continuous":
            # Create a gradient image
            colors = colormap["colors"]
            positions = colormap["positions"]

            # Convert to matplotlib colormap
            cmap = self.to_matplotlib(colormap_name)

            # Create gradient data
            gradient = np.linspace(0, 1, 256).reshape(-1, 1)
            im = ax.imshow(gradient, aspect="auto", cmap=cmap)

            # Add colorbar
            cbar = plt.colorbar(im, ax=ax, **kwargs)
            cbar.set_label(colormap.get("description", colormap_name))

        else:  # categorical
            colors = colormap["colors"]
            categories = list(colors.keys())
            color_values = list(colors.values())

            # Create discrete colorbar
            cmap = self.to_matplotlib(colormap_name)
            norm = plt.Normalize(0, len(colors) - 1)

            # Create gradient data
            gradient = np.arange(len(colors)).reshape(-1, 1)
            im = ax.imshow(gradient, aspect="auto", cmap=cmap, norm=norm)

            # Add colorbar with category labels
            cbar = plt.colorbar(im, ax=ax, **kwargs)
            cbar.set_ticks(np.arange(len(colors)) + 0.5)
            cbar.set_ticklabels(categories)
            cbar.set_label(colormap.get("description", colormap_name))

        ax.set_title(f"Colorbar: {colormap_name}")
        plt.tight_layout()

        return fig

    def get_color_lab(
        self,
        colormap_name: str,
        key_or_value: Union[str, float],
        fill_missing: bool = False,
        default_color: str = "#CCCCCC",
    ) -> str:
        """
        Get color using LAB color space interpolation for better perceptual uniformity.

        Args:
            colormap_name: Name of the colormap
            key_or_value: Category name (for categorical) or value (for continuous)
            fill_missing: If True, automatically assign colors for missing categories
            default_color: Default color to use for missing values (default: "#CCCCCC")

        Returns:
            Hex color string

        Raises:
            KeyError: If colormap doesn't exist and fill_missing is False
            ValueError: If value is out of range for continuous colormap
        """
        colormap = self.get_colormap(colormap_name)
        colormap_type = colormap["type"]

        if colormap_type == "categorical":
            colors = colormap["colors"]

            # Handle NaN/nan values
            if key_or_value in [None, "NaN", "nan", "NAN", "Nan"]:
                return default_color

            # Handle missing categories
            if key_or_value not in colors:
                if fill_missing:
                    # Auto-assign a color for missing category
                    return self._assign_color_for_missing_category(
                        colormap_name, key_or_value, colors
                    )
                else:
                    available = list(colors.keys())
                    raise KeyError(
                        f"Category '{key_or_value}' not found in colormap '{colormap_name}'. Available: {available}"
                    )
            return colors[key_or_value]

        elif colormap_type == "continuous":
            colors = colormap["colors"]
            positions = colormap["positions"]

            # Handle NaN/nan values for continuous colormaps
            if key_or_value in [None, "NaN", "nan", "NAN", "Nan"]:
                return default_color

            if not isinstance(key_or_value, (int, float)):
                raise ValueError(
                    f"Value must be numeric for continuous colormap: {key_or_value}"
                )

            value = float(key_or_value)

            # Handle edge cases
            if value <= positions[0]:
                return colors[0]
            if value >= positions[-1]:
                return colors[-1]

            # Find the appropriate segment
            for i in range(len(positions) - 1):
                if positions[i] <= value <= positions[i + 1]:
                    # Interpolate between colors using LAB space
                    t = (value - positions[i]) / (positions[i + 1] - positions[i])
                    color1 = colors[i]
                    color2 = colors[i + 1]

                    return interpolate_color_lab(color1, color2, t)

            # Should not reach here
            raise ValueError(f"Could not interpolate value {value}")

        else:
            raise ValueError(f"Unknown colormap type: {colormap_type}")

    def create_colorblind_safe_colormap(
        self, name: str, n_colors: int, colorblind_type: str = "deuteranopia"
    ) -> None:
        """
        Create a new colorblind-safe categorical colormap.

        Args:
            name: Name for the new colormap
            n_colors: Number of colors needed
            colorblind_type: Type of colorblindness to optimize for

        Raises:
            ValueError: If name is invalid or colormap already exists
        """
        if not validate_colormap_name(name):
            raise ValueError(f"Invalid colormap name: {name}")

        if name in self._colormaps:
            raise ValueError(f"Colormap '{name}' already exists")

        # Get colorblind-safe colors
        colors = get_colorblind_safe_colors(n_colors, colorblind_type)

        # Create colormap data
        colormap_data = {
            "type": "categorical",
            "description": f"Colorblind-safe colormap for {colorblind_type} ({n_colors} colors)",
            "colors": {f"category_{i}": color for i, color in enumerate(colors)},
        }

        # Add the colormap
        self._colormaps[name] = colormap_data
        self._data["colormaps"] = self._colormaps

    def validate_bio_requirements(
        self, colormap_name: str, bio_type: str = "expression"
    ) -> List[str]:
        """
        Validate colormap against biological data type requirements.

        Args:
            colormap_name: Name of the colormap to validate
            bio_type: Type of biological data ("expression", "sequence", "structure", "pathway")

        Returns:
            List of validation error messages (empty if valid)

        Raises:
            KeyError: If colormap doesn't exist
        """
        colormap = self.get_colormap(colormap_name)
        return validate_bio_specific_requirements(colormap, bio_type)

    @classmethod
    def from_community(cls, category: str, name: str) -> "BioCrayon":
        """
        Load colormap from community registry.

        Args:
            category: Category of the colormap (e.g., "neuroscience", "genomics")
            name: Name of the colormap file (without .json extension)

        Returns:
            BioCrayon instance loaded with the community colormap

        Raises:
            FileNotFoundError: If colormap doesn't exist in community collection
            ValueError: If colormap data is invalid
        """
        # GitHub repository URL for community colormaps
        base_url = "https://raw.githubusercontent.com/maflot/bio-crayon/main/community_colormaps"
        colormap_url = f"{base_url}/{category}/{name}.json"

        try:
            # Fetch the colormap from GitHub
            response = requests.get(colormap_url, timeout=10)
            response.raise_for_status()
            colormap_data = response.json()
        except requests.RequestException as e:
            # If not found, get available categories for better error message
            available_categories = cls.list_community_colormaps()
            if available_categories:
                category_list = list(available_categories.keys())
                raise FileNotFoundError(
                    f"Community colormap '{name}' not found in category '{category}'. "
                    f"Available categories: {category_list}. Error: {str(e)}"
                )
            else:
                raise FileNotFoundError(
                    f"Community colormap '{name}' not found in category '{category}'. "
                    f"No community colormaps available. Error: {str(e)}"
                )

        # Create BioCrayon instance with the loaded data
        instance = cls()
        instance.load(colormap_data, require_metadata=True)
        return instance

    @classmethod
    def list_community_colormaps(cls) -> Dict[str, List[str]]:
        """
        List all available community colormaps by category.

        Returns:
            Dictionary mapping category names to lists of available colormap names
        """
        try:
            # GitHub API URL to list contents of community_colormaps directory
            api_url = "https://api.github.com/repos/maflot/bio-crayon/contents/community_colormaps"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()

            categories = {}
            for item in response.json():
                if item["type"] == "dir":
                    category_name = item["name"]
                    # Get contents of each category directory
                    category_url = f"https://api.github.com/repos/maflot/bio-crayon/contents/community_colormaps/{category_name}"
                    category_response = requests.get(category_url, timeout=10)
                    category_response.raise_for_status()

                    colormaps = []
                    for file_item in category_response.json():
                        if file_item["type"] == "file" and file_item["name"].endswith(
                            ".json"
                        ):
                            colormaps.append(file_item["name"].replace(".json", ""))

                    if colormaps:  # Only add categories that have JSON files
                        categories[category_name] = sorted(colormaps)

            return categories
        except requests.RequestException:
            # Fallback: return known categories if API fails
            return {
                "allen_brain": ["single_cell"],
                "allen_immune": ["single_cell"],
                "cell_biology": ["fluorescent_proteins", "organelles"],
                "ecology": ["biodiversity", "habitat_types"],
                "genomics": ["expression_heatmaps", "quality_scores"],
                "imaging": ["he_staining", "ihc_markers"],
                "neuroscience": [],
                "pbmc_adrc": ["adrc"],
                "PBMCPedia": [],
            }

    def contribute_colormap(
        self, name: str, category: str, metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Helper to format colormap for community contribution.

        Args:
            name: Name for the colormap
            category: Category for the colormap
            metadata: Additional metadata for the contribution

        Returns:
            Dictionary with contribution information and formatted colormap data

        Raises:
            ValueError: If colormap doesn't exist or metadata is invalid
        """
        if name not in self._colormaps:
            raise ValueError(f"Colormap '{name}' not found in current instance")

        colormap_data = self._colormaps[name].copy()

        # Add contribution metadata
        contribution_info = {
            "name": name,
            "category": category,
            "contribution_date": metadata.get("contribution_date"),
            "contributor": metadata.get("contributor"),
            "paper_reference": metadata.get("paper_reference"),
            "doi": metadata.get("doi"),
            "use_case": metadata.get("use_case"),
            "accessibility_tested": metadata.get("accessibility_tested", False),
            "example_provided": metadata.get("example_provided", False),
        }

        # Validate accessibility if categorical
        if colormap_data["type"] == "categorical":
            colors = list(colormap_data["colors"].values())
            contribution_info["colorblind_safe"] = is_colorblind_safe(colors)

        return {
            "colormap_data": colormap_data,
            "contribution_info": contribution_info,
            "file_path": f"community_colormaps/{category}/{name}.json",
        }
