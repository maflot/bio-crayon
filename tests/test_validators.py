"""
Tests for validation functions.
"""

import pytest
import json
from pathlib import Path

from bio_crayon.validators import (
    validate_colormap_data,
    validate_hex_color,
    validate_colormap_name,
    validate_continuous_colormap,
    validate_categorical_colormap,
    validate_metadata,
    validate_metadata_required,
)


class TestHexColorValidation:
    """Test hex color validation."""

    def test_valid_hex_colors(self):
        """Test valid hex colors."""
        valid_colors = [
            "#FF0000",
            "#00FF00",
            "#0000FF",
            "#F00",
            "#0F0",
            "#00F",
            "#FFFFFF",
            "#000000",
            "#FFF",
            "#000",
        ]

        for color in valid_colors:
            assert validate_hex_color(color) is True

    def test_invalid_hex_colors(self):
        """Test invalid hex colors."""
        invalid_colors = [
            "FF0000",  # Missing #
            "#GG0000",  # Invalid characters
            "#FF00",  # Wrong length
            "#FF00000",  # Too long
            "#F",  # Too short
            "",  # Empty string
            None,  # None
            123,  # Number
        ]

        for color in invalid_colors:
            assert validate_hex_color(color) is False


class TestColormapNameValidation:
    """Test colormap name validation."""

    def test_valid_names(self):
        """Test valid colormap names."""
        valid_names = [
            "test",
            "test123",
            "test_name",
            "TestName",
            "_test",
            "test_",
            "_test_",
            "name123",
        ]

        for name in valid_names:
            assert validate_colormap_name(name) is True

    def test_invalid_names(self):
        """Test invalid colormap names."""
        invalid_names = [
            "123test",  # Starts with number
            "test-name",  # Contains hyphen
            "test.name",  # Contains dot
            "test name",  # Contains space
            "",  # Empty string
            None,  # None
            123,  # Number
        ]

        for name in invalid_names:
            assert validate_colormap_name(name) is False


class TestCategoricalColormapValidation:
    """Test categorical colormap validation."""

    def test_valid_categorical_colormap(self):
        """Test valid categorical colormap."""
        colormap = {
            "type": "categorical",
            "colors": {
                "category1": "#FF0000",
                "category2": "#00FF00",
                "category3": "#0000FF",
            },
        }

        errors = validate_categorical_colormap(colormap)
        assert len(errors) == 0

    def test_missing_colors_field(self):
        """Test categorical colormap without colors field."""
        colormap = {"type": "categorical"}

        errors = validate_categorical_colormap(colormap)
        assert len(errors) == 1
        assert "must have 'colors' field" in errors[0]

    def test_colors_not_dict(self):
        """Test categorical colormap with colors not being a dict."""
        colormap = {"type": "categorical", "colors": ["#FF0000", "#00FF00"]}

        errors = validate_categorical_colormap(colormap)
        assert len(errors) == 1
        assert "must be a dictionary" in errors[0]

    def test_empty_colors_dict(self):
        """Test categorical colormap with empty colors dict."""
        colormap = {"type": "categorical", "colors": {}}

        errors = validate_categorical_colormap(colormap)
        assert len(errors) == 1
        assert "cannot be empty" in errors[0]

    def test_invalid_color_in_categorical(self):
        """Test categorical colormap with invalid color."""
        colormap = {
            "type": "categorical",
            "colors": {"category1": "#FF0000", "category2": "invalid_color"},
        }

        errors = validate_categorical_colormap(colormap)
        assert len(errors) == 1
        assert "Invalid hex color" in errors[0]

    def test_invalid_category_name(self):
        """Test categorical colormap with invalid category name."""
        colormap = {
            "type": "categorical",
            "colors": {"category1": "#FF0000", 123: "#00FF00"},  # Invalid category name
        }

        errors = validate_categorical_colormap(colormap)
        assert len(errors) == 1
        assert "must be a string" in errors[0]


class TestContinuousColormapValidation:
    """Test continuous colormap validation."""

    def test_valid_continuous_colormap(self):
        """Test valid continuous colormap."""
        colormap = {
            "type": "continuous",
            "colors": ["#000000", "#FFFFFF"],
            "positions": [0.0, 1.0],
        }

        errors = validate_continuous_colormap(colormap)
        assert len(errors) == 0

    def test_missing_colors_field(self):
        """Test continuous colormap without colors field."""
        colormap = {"type": "continuous", "positions": [0.0, 1.0]}

        errors = validate_continuous_colormap(colormap)
        assert len(errors) == 1
        assert "must have 'colors' field" in errors[0]

    def test_missing_positions_field(self):
        """Test continuous colormap without positions field."""
        colormap = {"type": "continuous", "colors": ["#000000", "#FFFFFF"]}

        errors = validate_continuous_colormap(colormap)
        assert len(errors) == 1
        assert "must have 'positions' field" in errors[0]

    def test_colors_not_list(self):
        """Test continuous colormap with colors not being a list."""
        colormap = {
            "type": "continuous",
            "colors": {"#000000": 0.0, "#FFFFFF": 1.0},
            "positions": [0.0, 1.0],
        }

        errors = validate_continuous_colormap(colormap)
        assert len(errors) == 1
        assert "must be a list" in errors[0]

    def test_positions_not_list(self):
        """Test continuous colormap with positions not being a list."""
        colormap = {
            "type": "continuous",
            "colors": ["#000000", "#FFFFFF"],
            "positions": {"0.0": "#000000", "1.0": "#FFFFFF"},
        }

        errors = validate_continuous_colormap(colormap)
        assert len(errors) >= 1

    def test_insufficient_colors(self):
        """Test continuous colormap with insufficient colors."""
        colormap = {
            "type": "continuous",
            "colors": ["#000000"],
            "positions": [0.0, 1.0],
        }

        errors = validate_continuous_colormap(colormap)
        assert len(errors) >= 1

    def test_insufficient_positions(self):
        """Test continuous colormap with insufficient positions."""
        colormap = {
            "type": "continuous",
            "colors": ["#000000", "#FFFFFF"],
            "positions": [0.0],
        }

        errors = validate_continuous_colormap(colormap)
        assert len(errors) >= 1

    def test_mismatched_lengths(self):
        """Test continuous colormap with mismatched colors and positions."""
        colormap = {
            "type": "continuous",
            "colors": ["#000000", "#FFFFFF"],
            "positions": [0.0, 0.5, 1.0],
        }

        errors = validate_continuous_colormap(colormap)
        assert len(errors) == 1
        assert "must match" in errors[0]

    def test_invalid_color_in_continuous(self):
        """Test continuous colormap with invalid color."""
        colormap = {
            "type": "continuous",
            "colors": ["#000000", "invalid_color"],
            "positions": [0.0, 1.0],
        }

        errors = validate_continuous_colormap(colormap)
        assert len(errors) == 1
        assert "Invalid hex color" in errors[0]

    def test_invalid_position(self):
        """Test continuous colormap with invalid position."""
        colormap = {
            "type": "continuous",
            "colors": ["#000000", "#FFFFFF"],
            "positions": [0.0, 1.5],  # Out of range
        }

        errors = validate_continuous_colormap(colormap)
        assert len(errors) == 1
        assert "between 0 and 1" in errors[0]

    def test_unsorted_positions(self):
        """Test continuous colormap with unsorted positions."""
        colormap = {
            "type": "continuous",
            "colors": ["#000000", "#FFFFFF"],
            "positions": [1.0, 0.0],  # Not sorted
        }

        errors = validate_continuous_colormap(colormap)
        assert len(errors) == 1
        assert "ascending order" in errors[0]


class TestMetadataValidation:
    """Test metadata validation."""

    def test_valid_metadata(self):
        """Test valid metadata."""
        metadata = {"name": "Test Colormaps", "version": "1.0"}

        errors = validate_metadata(metadata)
        assert len(errors) == 0

    def test_missing_required_fields(self):
        """Test metadata with missing required fields."""
        metadata = {
            "name": "Test Colormaps"
            # Missing version
        }

        errors = validate_metadata(metadata)
        assert len(errors) == 1
        assert "must have 'version' field" in errors[0]

    def test_invalid_name_type(self):
        """Test metadata with invalid name type."""
        metadata = {"name": 123, "version": "1.0"}  # Should be string

        errors = validate_metadata(metadata)
        assert len(errors) == 1
        assert "must be a string" in errors[0]

    def test_invalid_version_format(self):
        """Test metadata with invalid version format."""
        metadata = {"name": "Test Colormaps", "version": "invalid_version"}

        errors = validate_metadata(metadata)
        assert len(errors) == 1
        assert "format 'X.Y' or 'X.Y.Z'" in errors[0]

    def test_valid_version_formats(self):
        """Test valid version formats."""
        valid_versions = ["1.0", "1.0.0", "2.1.3"]

        for version in valid_versions:
            metadata = {"name": "Test Colormaps", "version": version}

            errors = validate_metadata(metadata)
            assert len(errors) == 0


class TestCompleteDataValidation:
    """Test complete colormap data validation."""

    def test_valid_complete_data(self):
        """Test valid complete colormap data."""
        data = {
            "metadata": {"name": "Test Colormaps", "version": "1.0"},
            "colormaps": {
                "test_categorical": {
                    "type": "categorical",
                    "colors": {"category1": "#FF0000", "category2": "#00FF00"},
                },
                "test_continuous": {
                    "type": "continuous",
                    "colors": ["#000000", "#FFFFFF"],
                    "positions": [0.0, 1.0],
                },
            },
        }

        errors = validate_colormap_data(data)
        assert len(errors) == 0

    def test_valid_data_without_metadata(self):
        """Test data without metadata (valid for user colormaps)."""
        data = {
            "colormaps": {"test": {"type": "categorical", "colors": {"cat": "#FF0000"}}}
        }

        errors = validate_colormap_data(data, require_metadata=False)
        assert len(errors) == 0

    def test_missing_metadata_for_community(self):
        """Test data without metadata when metadata is required."""
        data = {
            "colormaps": {"test": {"type": "categorical", "colors": {"cat": "#FF0000"}}}
        }

        errors = validate_colormap_data(data, require_metadata=True)
        assert len(errors) > 0
        assert any("must have 'name' field" in error for error in errors)
        assert any("must have 'version' field" in error for error in errors)

    def test_incomplete_metadata_for_community(self):
        """Test data with incomplete metadata when metadata is required."""
        data = {
            "metadata": {
                "name": "Test Colormaps"
                # Missing version
            },
            "colormaps": {
                "test": {"type": "categorical", "colors": {"cat": "#FF0000"}}
            },
        }

        errors = validate_colormap_data(data, require_metadata=True)
        assert len(errors) > 0
        assert any("must have 'version' field" in error for error in errors)

    def test_missing_colormaps(self):
        """Test data without colormaps."""
        data = {"metadata": {"name": "Test", "version": "1.0"}}

        errors = validate_colormap_data(data)
        assert len(errors) > 0
        assert any("colormaps" in error for error in errors)

    def test_invalid_colormap_name(self):
        """Test data with invalid colormap name."""
        data = {
            "metadata": {"name": "Test", "version": "1.0"},
            "colormaps": {
                "123invalid": {  # Invalid name
                    "type": "categorical",
                    "colors": {"cat": "#FF0000"},
                }
            },
        }

        errors = validate_colormap_data(data)
        assert len(errors) > 0


class TestMetadataRequiredValidation:
    """Test metadata required validation for community colormaps."""

    def test_valid_metadata_required(self):
        """Test valid metadata for community colormaps."""
        metadata = {
            "name": "Test Colormaps",
            "version": "1.0",
            "description": "Test description",
        }

        errors = validate_metadata_required(metadata)
        assert len(errors) == 0

    def test_missing_name_field(self):
        """Test metadata missing name field."""
        metadata = {
            "version": "1.0",
            "description": "Test description",
            # Missing name
        }

        errors = validate_metadata_required(metadata)
        assert len(errors) == 1
        assert "must have 'name' field" in errors[0]

    def test_missing_version_field(self):
        """Test metadata missing version field."""
        metadata = {
            "name": "Test Colormaps",
            "description": "Test description",
            # Missing version
        }

        errors = validate_metadata_required(metadata)
        assert len(errors) == 1
        assert "must have 'version' field" in errors[0]

    def test_invalid_name_type(self):
        """Test metadata with invalid name type."""
        metadata = {
            "name": 123,
            "version": "1.0",
            "description": "Test description",
        }  # Should be string

        errors = validate_metadata_required(metadata)
        assert len(errors) == 1
        assert "must be a string" in errors[0]

    def test_invalid_version_format(self):
        """Test metadata with invalid version format."""
        metadata = {
            "name": "Test Colormaps",
            "version": "invalid_version",
            "description": "Test description",
        }

        errors = validate_metadata_required(metadata)
        assert len(errors) == 1
        assert "format 'X.Y' or 'X.Y.Z'" in errors[0]

    def test_missing_description_field(self):
        """Test metadata missing description field."""
        metadata = {
            "name": "Test Colormaps",
            "version": "1.0",
            # Missing description
        }

        errors = validate_metadata_required(metadata)
        assert len(errors) == 1
        assert "must have 'description' field" in errors[0]
