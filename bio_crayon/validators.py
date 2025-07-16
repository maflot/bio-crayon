"""
Validation utilities for BioCrayon colormaps.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Union, List

import jsonschema
from jsonschema import ValidationError


def load_schema() -> Dict[str, Any]:
    """Load the colormap JSON schema."""
    import importlib.resources
    
    try:
        # Try to load from package data (installed package)
        with importlib.resources.files("bio_crayon").joinpath("schemas/colormap_schema.json").open("r") as f:
            return json.load(f)
    except (FileNotFoundError, ModuleNotFoundError):
        # Fallback to relative path for development
        schema_path = Path(__file__).parent / "schemas" / "colormap_schema.json"
        with open(schema_path, "r") as f:
            return json.load(f)


def validate_colormap_data(
    data: Dict[str, Any], require_metadata: bool = False
) -> List[str]:
    """
    Validate colormap data against the JSON schema.

    Args:
        data: Dictionary containing colormap data
        require_metadata: Whether metadata is required (True for community colormaps)

    Returns:
        List of validation error messages (empty if valid)
    """
    schema = load_schema()
    validator = jsonschema.Draft7Validator(schema)

    errors = []
    for error in validator.iter_errors(data):
        errors.append(f"{error.path}: {error.message}")

    # Additional validation for metadata requirements
    if require_metadata:
        metadata_errors = validate_metadata_required(data.get("metadata", {}))
        errors.extend(metadata_errors)

    return errors


def validate_metadata_required(metadata: Dict[str, Any]) -> List[str]:
    """
    Validate that metadata contains all required fields for community colormaps.

    Args:
        metadata: Dictionary containing metadata

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    required_fields = ["name", "version", "description"]
    for field in required_fields:
        if field not in metadata:
            errors.append(f"Community colormaps must have '{field}' field in metadata")

    if "description" in metadata and not isinstance(metadata["description"], str):
        errors.append("Metadata 'description' must be a string")

    if "name" in metadata and not isinstance(metadata["name"], str):
        errors.append("Metadata 'name' must be a string")

    if "version" in metadata:
        version = metadata["version"]
        if not isinstance(version, str):
            errors.append("Metadata 'version' must be a string")
        elif not re.match(r"^\d+\.\d+(\.\d+)?$", version):
            errors.append("Metadata 'version' must be in format 'X.Y' or 'X.Y.Z'")

    return errors


def validate_hex_color(color: str) -> bool:
    """
    Validate if a string is a valid hex color.

    Args:
        color: Color string to validate

    Returns:
        True if valid hex color, False otherwise
    """
    if not isinstance(color, str):
        return False

    # Match 3 or 6 digit hex colors
    pattern = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    return bool(re.match(pattern, color))


def validate_continuous_colormap(colormap: Dict[str, Any]) -> List[str]:
    """
    Validate a continuous colormap structure.

    Args:
        colormap: Dictionary containing continuous colormap data

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if "colors" not in colormap:
        errors.append("Continuous colormap must have 'colors' field")
        return errors

    if "positions" not in colormap:
        errors.append("Continuous colormap must have 'positions' field")
        return errors

    colors = colormap["colors"]
    positions = colormap["positions"]

    if not isinstance(colors, list) or len(colors) < 2:
        errors.append("Colors must be a list with at least 2 elements")

    if not isinstance(positions, list) or len(positions) < 2:
        errors.append("Positions must be a list with at least 2 elements")

    if len(colors) != len(positions):
        errors.append("Number of colors must match number of positions")

    # Validate individual colors
    for i, color in enumerate(colors):
        if not validate_hex_color(color):
            errors.append(f"Invalid hex color at index {i}: {color}")

    # Validate positions are in [0, 1] range
    for i, pos in enumerate(positions):
        if not isinstance(pos, (int, float)) or pos < 0 or pos > 1:
            errors.append(
                f"Position at index {i} must be a number between 0 and 1: {pos}"
            )

    # Check if positions are sorted
    if len(positions) > 1 and positions != sorted(positions):
        errors.append("Positions must be in ascending order")

    return errors


def validate_categorical_colormap(colormap: Dict[str, Any]) -> List[str]:
    """
    Validate a categorical colormap structure.

    Args:
        colormap: Dictionary containing categorical colormap data

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if "colors" not in colormap:
        errors.append("Categorical colormap must have 'colors' field")
        return errors

    colors = colormap["colors"]

    if not isinstance(colors, dict):
        errors.append("Colors must be a dictionary mapping category names to colors")
        return errors

    if len(colors) == 0:
        errors.append("Colors dictionary cannot be empty")
        return errors

    # Validate each color
    for category, color in colors.items():
        if not isinstance(category, str):
            errors.append(f"Category name must be a string: {category}")

        if not validate_hex_color(color):
            errors.append(f"Invalid hex color for category '{category}': {color}")

    return errors


def validate_colormap_name(name: str) -> bool:
    """
    Validate if a colormap name is valid.

    Args:
        name: Name to validate

    Returns:
        True if valid name, False otherwise
    """
    if not isinstance(name, str):
        return False

    # Must start with letter or underscore, contain only alphanumeric and underscore
    pattern = r"^[a-zA-Z_][a-zA-Z0-9_]*$"
    return bool(re.match(pattern, name))


def validate_metadata(metadata: Dict[str, Any]) -> List[str]:
    """
    Validate metadata structure.

    Args:
        metadata: Dictionary containing metadata

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    required_fields = ["name", "version"]
    for field in required_fields:
        if field not in metadata:
            errors.append(f"Metadata must have '{field}' field")

    if "name" in metadata and not isinstance(metadata["name"], str):
        errors.append("Metadata 'name' must be a string")

    if "version" in metadata:
        version = metadata["version"]
        if not isinstance(version, str):
            errors.append("Metadata 'version' must be a string")
        elif not re.match(r"^\d+\.\d+(\.\d+)?$", version):
            errors.append("Metadata 'version' must be in format 'X.Y' or 'X.Y.Z'")

    return errors


def validate_expression_range(
    colormap: Dict[str, Any], min_val: float, max_val: float
) -> List[str]:
    """
    Validate that a continuous colormap covers the expected expression range.

    Args:
        colormap: Dictionary containing continuous colormap data
        min_val: Expected minimum value in the data
        max_val: Expected maximum value in the data

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if colormap.get("type") != "continuous":
        errors.append(
            "Expression range validation only applies to continuous colormaps"
        )
        return errors

    if "positions" not in colormap:
        errors.append("Continuous colormap must have 'positions' field")
        return errors

    positions = colormap["positions"]

    # Check if colormap positions cover the expected range
    colormap_min = min(positions)
    colormap_max = max(positions)

    # Allow some tolerance for normalized ranges
    tolerance = 0.1

    if colormap_min > min_val + tolerance:
        errors.append(
            f"Colormap minimum ({colormap_min}) is higher than expected minimum ({min_val})"
        )

    if colormap_max < max_val - tolerance:
        errors.append(
            f"Colormap maximum ({colormap_max}) is lower than expected maximum ({max_val})"
        )

    return errors


def validate_colorblind_safety(
    colormap: Dict[str, Any], colorblind_type: str = "deuteranopia"
) -> List[str]:
    """
    Validate that a categorical colormap is distinguishable for colorblind users.

    Args:
        colormap: Dictionary containing categorical colormap data
        colorblind_type: Type of colorblindness to check for

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if colormap.get("type") != "categorical":
        errors.append(
            "Colorblind safety validation only applies to categorical colormaps"
        )
        return errors

    if "colors" not in colormap:
        errors.append("Categorical colormap must have 'colors' field")
        return errors

    colors = list(colormap["colors"].values())

    # Import here to avoid circular imports
    from .utils import is_colorblind_safe

    if not is_colorblind_safe(colors, colorblind_type):
        errors.append(
            f"Colormap colors are not distinguishable for {colorblind_type} colorblind users"
        )

    return errors


def validate_bio_specific_requirements(
    colormap: Dict[str, Any], bio_type: str = "expression"
) -> List[str]:
    """
    Validate colormap against biological data type requirements.

    Args:
        colormap: Dictionary containing colormap data
        bio_type: Type of biological data ("expression", "sequence", "structure", "pathway")

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if bio_type == "expression":
        # Expression data should have good contrast for low/high values
        if colormap.get("type") == "continuous":
            colors = colormap.get("colors", [])
            if len(colors) >= 2:
                # Check if first and last colors have good contrast
                from .utils import calculate_color_distance

                distance = calculate_color_distance(colors[0], colors[-1])
                if distance < 100:  # Threshold for good contrast
                    errors.append(
                        "Expression colormap should have high contrast between low and high values"
                    )

    elif bio_type == "sequence":
        # Sequence data often benefits from categorical colors
        if colormap.get("type") != "categorical":
            errors.append("Sequence data typically requires categorical colormap")

    elif bio_type == "structure":
        # Structure data should have perceptually uniform gradients
        if colormap.get("type") == "continuous":
            # Check if using perceptually uniform interpolation
            interpolation = colormap.get("interpolation", "linear")
            if interpolation not in ["lab", "perceptually_uniform"]:
                errors.append(
                    "Structure data should use perceptually uniform color interpolation"
                )

    return errors
