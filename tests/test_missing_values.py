"""
Tests for BioCrayon missing value handling functionality.
"""

import pytest
from bio_crayon import BioCrayon


class TestMissingValues:
    """Test missing value handling functionality."""

    def setup_method(self):
        """Set up test data."""
        self.test_data = {
            "colormaps": {
                "test_categorical": {
                    "type": "categorical",
                    "description": "Test categorical colormap",
                    "colors": {
                        "category1": "#FF0000",
                        "category2": "#00FF00",
                        "category3": "#0000FF"
                    }
                },
                "test_continuous": {
                    "type": "continuous",
                    "description": "Test continuous colormap",
                    "colors": ["#000000", "#FFFFFF"],
                    "positions": [0.0, 1.0]
                }
            }
        }
        self.biocrayon = BioCrayon(self.test_data)

    def test_default_behavior_raises_keyerror(self):
        """Test that missing categories raise KeyError by default."""
        with pytest.raises(KeyError):
            self.biocrayon.get_color("test_categorical", "missing_category")

    def test_fill_missing_assigns_color(self):
        """Test that fill_missing=True assigns colors for missing categories."""
        color = self.biocrayon.get_color("test_categorical", "missing_category", fill_missing=True)
        assert color.startswith("#")
        assert len(color) == 7  # Hex color format

    def test_nan_values_return_default_color(self):
        """Test that NaN values return the default color."""
        nan_values = [None, "NaN", "nan", "NAN", "Nan"]
        for nan_val in nan_values:
            color = self.biocrayon.get_color("test_categorical", nan_val, fill_missing=True)
            assert color == "#CCCCCC"  # Default color

    def test_custom_default_color(self):
        """Test that custom default color is used for NaN values."""
        custom_color = "#FF9999"
        color = self.biocrayon.get_color("test_categorical", None, fill_missing=True, default_color=custom_color)
        assert color == custom_color

    def test_continuous_colormap_nan_handling(self):
        """Test NaN handling in continuous colormaps."""
        nan_values = [None, "NaN", "nan"]
        for nan_val in nan_values:
            color = self.biocrayon.get_color("test_continuous", nan_val, fill_missing=True)
            assert color == "#CCCCCC"  # Default color

    def test_continuous_colormap_normal_values(self):
        """Test that continuous colormap still works with normal values."""
        color = self.biocrayon.get_color("test_continuous", 0.5)
        assert color.startswith("#")
        assert len(color) == 7

    def test_colormap_accessor_fill_missing(self):
        """Test fill_missing with ColormapAccessor."""
        accessor = self.biocrayon["test_categorical"]
        accessor.set_fill_missing(True, default_color="#FF9999")
        
        # Test missing category
        color = accessor["missing_category"]
        assert color.startswith("#")
        assert len(color) == 7
        
        # Test NaN value
        color = accessor[None]
        assert color == "#FF9999"

    def test_colormap_accessor_default_behavior(self):
        """Test that ColormapAccessor respects fill_missing setting."""
        accessor = self.biocrayon["test_categorical"]
        # Default should be False
        with pytest.raises(KeyError):
            _ = accessor["missing_category"]

    def test_auto_assigned_colors_are_distinct(self):
        """Test that auto-assigned colors are distinct from existing colors."""
        existing_colors = set(self.test_data["colormaps"]["test_categorical"]["colors"].values())
        
        # Assign colors for multiple missing categories
        missing_categories = ["missing1", "missing2", "missing3"]
        assigned_colors = set()
        
        for category in missing_categories:
            color = self.biocrayon.get_color("test_categorical", category, fill_missing=True)
            assigned_colors.add(color)
        
        # Check that assigned colors are distinct from existing colors
        assert assigned_colors.isdisjoint(existing_colors)
        
        # Check that assigned colors are distinct from each other
        assert len(assigned_colors) == len(missing_categories)

    def test_colormap_updated_after_auto_assignment(self):
        """Test that colormap is updated after auto-assignment."""
        original_keys = set(self.biocrayon["test_categorical"].keys())
        
        # Assign color for missing category
        self.biocrayon.get_color("test_categorical", "new_category", fill_missing=True)
        
        # Check that the category was added to the colormap
        updated_keys = set(self.biocrayon["test_categorical"].keys())
        assert "new_category" in updated_keys
        assert len(updated_keys) == len(original_keys) + 1

    def test_get_color_lab_with_fill_missing(self):
        """Test that get_color_lab also supports fill_missing."""
        color = self.biocrayon.get_color_lab("test_categorical", "missing_category", fill_missing=True)
        assert color.startswith("#")
        assert len(color) == 7

    def test_get_color_lab_nan_handling(self):
        """Test NaN handling in get_color_lab."""
        color = self.biocrayon.get_color_lab("test_categorical", None, fill_missing=True)
        assert color == "#CCCCCC"  # Default color

    def test_repr_shows_fill_missing_status(self):
        """Test that ColormapAccessor repr shows fill_missing status."""
        accessor = self.biocrayon["test_categorical"]
        
        # Default should not show fill_missing
        repr_str = repr(accessor)
        assert "fill_missing=True" not in repr_str
        
        # After setting fill_missing, should show it
        accessor.set_fill_missing(True)
        repr_str = repr(accessor)
        assert "fill_missing=True" in repr_str

    def test_multiple_missing_categories_same_color(self):
        """Test that the same missing category gets the same color consistently."""
        category = "consistent_category"
        
        # Get color twice for the same missing category
        color1 = self.biocrayon.get_color("test_categorical", category, fill_missing=True)
        color2 = self.biocrayon.get_color("test_categorical", category, fill_missing=True)
        
        # Should be the same color
        assert color1 == color2

    def test_fill_missing_with_existing_category(self):
        """Test that fill_missing doesn't affect existing categories."""
        original_color = self.biocrayon.get_color("test_categorical", "category1")
        new_color = self.biocrayon.get_color("test_categorical", "category1", fill_missing=True)
        
        # Should be the same color
        assert original_color == new_color


if __name__ == "__main__":
    pytest.main([__file__]) 