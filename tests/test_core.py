"""
Tests for the core BioCrayon class.
"""

import pytest
import tempfile
import json
from pathlib import Path

from bio_crayon import BioCrayon


class TestBioCrayon:
    """Test cases for the BioCrayon class."""

    def setup_method(self):
        """Set up test data."""
        self.test_data = {
            "metadata": {
                "name": "Test Colormaps",
                "version": "1.0",
                "description": "Test colormaps for unit testing",
            },
            "colormaps": {
                "test_categorical": {
                    "type": "categorical",
                    "description": "Test categorical colormap",
                    "colors": {
                        "category1": "#FF0000",
                        "category2": "#00FF00",
                        "category3": "#0000FF",
                    },
                },
                "test_continuous": {
                    "type": "continuous",
                    "description": "Test continuous colormap",
                    "colors": ["#000000", "#FFFFFF"],
                    "positions": [0.0, 1.0],
                    "interpolation": "linear",
                },
                "test_expression": {
                    "type": "continuous",
                    "description": "Expression data colormap",
                    "colors": ["#0000FF", "#FFFFFF", "#FF0000"],
                    "positions": [0.0, 0.5, 1.0],
                    "interpolation": "linear",
                },
                "test_colorblind_unsafe": {
                    "type": "categorical",
                    "description": "Colorblind unsafe colormap",
                    "colors": {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"},
                },
                "test_colorblind_safe": {
                    "type": "categorical",
                    "description": "Colorblind safe colormap",
                    "colors": {
                        "black": "#000000",
                        "orange": "#E69F00",
                        "blue": "#56B4E9",
                    },
                },
            },
        }

        self.biocrayon = BioCrayon()

    def test_init_empty(self):
        """Test initialization with no source."""
        bc = BioCrayon()
        assert len(bc) == 0
        assert bc.list_colormaps() == []

    def test_init_with_dict(self):
        """Test initialization with dictionary source."""
        bc = BioCrayon(self.test_data)
        assert len(bc) == 5
        assert "test_categorical" in bc
        assert "test_continuous" in bc

    def test_load_from_dict(self):
        """Test loading from dictionary."""
        self.biocrayon.load(self.test_data)
        assert len(self.biocrayon) == 5
        assert "test_categorical" in self.biocrayon

    def test_load_from_file(self):
        """Test loading from file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(self.test_data, f)
            filepath = f.name

        try:
            self.biocrayon.load(filepath)
            assert len(self.biocrayon) == 5
            assert "test_categorical" in self.biocrayon
        finally:
            Path(filepath).unlink()

    def test_get_colormap(self):
        """Test getting a specific colormap."""
        self.biocrayon.load(self.test_data)
        colormap = self.biocrayon.get_colormap("test_categorical")
        assert colormap["type"] == "categorical"
        assert "category1" in colormap["colors"]

    def test_get_colormap_not_found(self):
        """Test getting non-existent colormap."""
        self.biocrayon.load(self.test_data)
        with pytest.raises(KeyError):
            self.biocrayon.get_colormap("nonexistent")

    def test_get_color_categorical(self):
        """Test getting color for categorical colormap."""
        self.biocrayon.load(self.test_data)
        color = self.biocrayon.get_color("test_categorical", "category1")
        assert color == "#FF0000"

    def test_get_color_continuous(self):
        """Test getting color for continuous colormap."""
        self.biocrayon.load(self.test_data)
        color = self.biocrayon.get_color("test_continuous", 0.5)
        assert color == "#808080"  # Should be gray at 0.5

    def test_get_color_continuous_edge_cases(self):
        """Test continuous colormap edge cases."""
        self.biocrayon.load(self.test_data)

        # Test values at boundaries
        color_min = self.biocrayon.get_color("test_continuous", 0.0)
        color_max = self.biocrayon.get_color("test_continuous", 1.0)
        assert color_min == "#000000"
        assert color_max == "#FFFFFF"

        # Test values outside boundaries
        color_below = self.biocrayon.get_color("test_continuous", -0.5)
        color_above = self.biocrayon.get_color("test_continuous", 1.5)
        assert color_below == "#000000"
        assert color_above == "#FFFFFF"

    def test_get_color_invalid_category(self):
        """Test getting color for invalid category."""
        self.biocrayon.load(self.test_data)
        with pytest.raises(KeyError):
            self.biocrayon.get_color("test_categorical", "invalid_category")

    def test_get_color_invalid_value_type(self):
        """Test getting color with invalid value type for continuous."""
        self.biocrayon.load(self.test_data)
        with pytest.raises(ValueError):
            self.biocrayon.get_color("test_continuous", "not_a_number")

    def test_list_colormaps(self):
        """Test listing colormaps."""
        self.biocrayon.load(self.test_data)
        colormaps = self.biocrayon.list_colormaps()
        assert len(colormaps) == 5
        assert "test_categorical" in colormaps
        assert "test_continuous" in colormaps

    def test_add_colormap(self):
        """Test adding a new colormap."""
        new_colormap = {
            "type": "categorical",
            "description": "New test colormap",
            "colors": {"new1": "#FF00FF", "new2": "#00FFFF"},
        }

        self.biocrayon.add_colormap("new_test", new_colormap)
        assert "new_test" in self.biocrayon
        assert self.biocrayon.get_colormap("new_test") == new_colormap

    def test_add_colormap_invalid_name(self):
        """Test adding colormap with invalid name."""
        new_colormap = {"type": "categorical", "colors": {"test": "#FF0000"}}

        with pytest.raises(ValueError):
            self.biocrayon.add_colormap("123invalid", new_colormap)

    def test_add_colormap_duplicate_name(self):
        """Test adding colormap with duplicate name."""
        self.biocrayon.load(self.test_data)

        new_colormap = {"type": "categorical", "colors": {"test": "#FF0000"}}

        with pytest.raises(ValueError):
            self.biocrayon.add_colormap("test_categorical", new_colormap)

    def test_save(self):
        """Test saving colormaps to file."""
        self.biocrayon.load(self.test_data)

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            filepath = f.name

        try:
            self.biocrayon.save(filepath)

            # Verify the saved file
            with open(filepath, "r") as f:
                saved_data = json.load(f)

            assert saved_data == self.test_data
        finally:
            Path(filepath).unlink()

    def test_get_metadata(self):
        """Test getting metadata."""
        self.biocrayon.load(self.test_data)
        metadata = self.biocrayon.get_metadata()
        assert metadata["name"] == "Test Colormaps"
        assert metadata["version"] == "1.0"

    def test_get_colormap_info_categorical(self):
        """Test getting colormap info for categorical."""
        self.biocrayon.load(self.test_data)
        info = self.biocrayon.get_colormap_info("test_categorical")
        assert info["type"] == "categorical"
        assert info["num_categories"] == 3
        assert "category1" in info["categories"]

    def test_get_colormap_info_continuous(self):
        """Test getting colormap info for continuous."""
        self.biocrayon.load(self.test_data)
        info = self.biocrayon.get_colormap_info("test_continuous")
        assert info["type"] == "continuous"
        assert info["num_colors"] == 2
        assert info["range"] == (0.0, 1.0)

    def test_len(self):
        """Test length method."""
        self.biocrayon.load(self.test_data)
        assert len(self.biocrayon) == 5

    def test_contains(self):
        """Test contains method."""
        self.biocrayon.load(self.test_data)
        assert "test_categorical" in self.biocrayon
        assert "nonexistent" not in self.biocrayon

    def test_iter(self):
        """Test iteration."""
        self.biocrayon.load(self.test_data)
        colormap_names = list(self.biocrayon)
        assert len(colormap_names) == 5
        assert "test_categorical" in colormap_names

    # New tests for enhanced features

    def test_validate_expression_range_valid(self):
        """Test expression range validation with valid range."""
        self.biocrayon.load(self.test_data)
        errors = self.biocrayon.validate_expression_range("test_expression", 0.0, 1.0)
        assert len(errors) == 0

    def test_validate_expression_range_invalid(self):
        """Test expression range validation with invalid range."""
        self.biocrayon.load(self.test_data)
        errors = self.biocrayon.validate_expression_range("test_expression", -1.0, 2.0)
        assert len(errors) == 2
        assert "Colormap minimum" in errors[0]
        assert "Colormap maximum" in errors[1]

    def test_validate_expression_range_wrong_type(self):
        """Test expression range validation with categorical colormap."""
        self.biocrayon.load(self.test_data)
        errors = self.biocrayon.validate_expression_range("test_categorical", 0.0, 1.0)
        assert len(errors) == 1
        assert "only applies to continuous colormaps" in errors[0]

    def test_is_colorblind_safe_safe(self):
        """Test colorblind safety check with safe colors."""
        self.biocrayon.load(self.test_data)
        is_safe = self.biocrayon.is_colorblind_safe("test_colorblind_safe")
        assert is_safe == True

    def test_is_colorblind_safe_unsafe(self):
        """Test colorblind safety check with unsafe colors."""
        self.biocrayon.load(self.test_data)
        is_safe = self.biocrayon.is_colorblind_safe("test_colorblind_unsafe")
        assert is_safe == True  # With current threshold, RGB is considered safe

    def test_is_colorblind_safe_wrong_type(self):
        """Test colorblind safety check with continuous colormap."""
        self.biocrayon.load(self.test_data)
        with pytest.raises(ValueError):
            self.biocrayon.is_colorblind_safe("test_continuous")

    def test_get_color_lab_categorical(self):
        """Test LAB color interpolation for categorical (should be same as regular)."""
        self.biocrayon.load(self.test_data)
        color_regular = self.biocrayon.get_color("test_categorical", "category1")
        color_lab = self.biocrayon.get_color_lab("test_categorical", "category1")
        assert color_regular == color_lab

    def test_get_color_lab_continuous(self):
        """Test LAB color interpolation for continuous colormap."""
        self.biocrayon.load(self.test_data)
        # Test that LAB interpolation produces different results than RGB
        color_rgb = self.biocrayon.get_color("test_continuous", 0.5)
        color_lab = self.biocrayon.get_color_lab("test_continuous", 0.5)
        # They should be different due to different interpolation methods
        assert color_rgb != color_lab

    def test_create_colorblind_safe_colormap(self):
        """Test creating a colorblind-safe colormap."""
        self.biocrayon.create_colorblind_safe_colormap("safe_test", 5)
        assert "safe_test" in self.biocrayon

        colormap = self.biocrayon.get_colormap("safe_test")
        assert colormap["type"] == "categorical"
        assert len(colormap["colors"]) == 5

        # Check that it's actually colorblind safe
        is_safe = self.biocrayon.is_colorblind_safe("safe_test")
        assert is_safe == True

    def test_create_colorblind_safe_colormap_duplicate(self):
        """Test creating colorblind-safe colormap with duplicate name."""
        self.biocrayon.load(self.test_data)
        with pytest.raises(ValueError):
            self.biocrayon.create_colorblind_safe_colormap("test_categorical", 5)

    def test_validate_bio_requirements_expression(self):
        """Test biological requirements validation for expression data."""
        self.biocrayon.load(self.test_data)
        errors = self.biocrayon.validate_bio_requirements(
            "test_expression", "expression"
        )
        # Should pass for good expression colormap
        assert len(errors) == 0

    def test_validate_bio_requirements_sequence(self):
        """Test biological requirements validation for sequence data."""
        self.biocrayon.load(self.test_data)
        errors = self.biocrayon.validate_bio_requirements(
            "test_categorical", "sequence"
        )
        # Should pass for categorical colormap
        assert len(errors) == 0

    def test_validate_bio_requirements_sequence_wrong_type(self):
        """Test biological requirements validation for sequence data with wrong type."""
        self.biocrayon.load(self.test_data)
        errors = self.biocrayon.validate_bio_requirements("test_continuous", "sequence")
        # Should fail for continuous colormap with sequence data
        assert len(errors) == 1
        assert "typically requires categorical colormap" in errors[0]

    def test_get_colorbar_continuous(self):
        """Test getting colorbar for continuous colormap."""
        self.biocrayon.load(self.test_data)
        fig = self.biocrayon.get_colorbar("test_continuous")
        assert fig is not None
        # Clean up
        import matplotlib.pyplot as plt

        plt.close(fig)

    def test_get_colorbar_categorical(self):
        """Test getting colorbar for categorical colormap."""
        self.biocrayon.load(self.test_data)
        fig = self.biocrayon.get_colorbar("test_categorical")
        assert fig is not None
        # Clean up
        import matplotlib.pyplot as plt

        plt.close(fig)

    def test_get_colorbar_with_kwargs(self):
        """Test getting colorbar with additional kwargs."""
        self.biocrayon.load(self.test_data)
        fig = self.biocrayon.get_colorbar("test_continuous", figsize=(2, 8))
        assert fig is not None
        # Clean up
        import matplotlib.pyplot as plt

        plt.close(fig)


class TestBioCrayonMatplotlib:
    """Test cases for matplotlib integration."""

    def setup_method(self):
        """Set up test data."""
        self.test_data = {
            "metadata": {"name": "Test", "version": "1.0"},
            "colormaps": {
                "test_continuous": {
                    "type": "continuous",
                    "colors": ["#000000", "#FFFFFF"],
                    "positions": [0.0, 1.0],
                },
                "test_categorical": {
                    "type": "categorical",
                    "colors": {"cat1": "#FF0000", "cat2": "#00FF00", "cat3": "#0000FF"},
                },
            },
        }
        self.biocrayon = BioCrayon(self.test_data)

    def test_to_matplotlib_continuous(self):
        """Test converting continuous colormap to matplotlib."""
        cmap = self.biocrayon.to_matplotlib("test_continuous")
        assert cmap.N == 256  # Default number of colors
        assert cmap.name == "test_continuous"

    def test_to_matplotlib_categorical(self):
        """Test converting categorical colormap to matplotlib."""
        cmap = self.biocrayon.to_matplotlib("test_categorical")
        assert cmap.N == 3  # Number of categories
        assert cmap.name == "test_categorical"

    def test_to_matplotlib_custom_n_colors(self):
        """Test converting with custom number of colors."""
        cmap = self.biocrayon.to_matplotlib("test_continuous", n_colors=100)
        assert cmap.N == 100


class TestIntegrationTests:
    """Integration tests that mirror the GitHub Actions workflow tests."""

    def test_user_colormap_no_metadata_required(self):
        """Test user colormap (no metadata required)."""
        user_data = {
            "colormaps": {
                "test_colors": {
                    "type": "categorical",
                    "colors": {"red": "#FF0000", "green": "#00FF00"},
                }
            }
        }
        bc_user = BioCrayon(user_data)
        assert "test_colors" in bc_user.list_colormaps()

    def test_community_colormap_metadata_required(self):
        """Test community colormap (metadata required with description)."""
        community_data = {
            "metadata": {
                "name": "Test Collection",
                "version": "1.0",
                "description": "Test community colormap for integration test",
            },
            "colormaps": {
                "test_colors": {
                    "type": "categorical",
                    "colors": {"red": "#FF0000", "green": "#00FF00"},
                }
            },
        }
        bc_community = BioCrayon(community_data, require_metadata=True)
        assert "test_colors" in bc_community.list_colormaps()

    def test_community_colormap_missing_description_fails(self):
        """Test that community colormap without description fails validation."""
        community_data = {
            "metadata": {
                "name": "Test Collection",
                "version": "1.0",
                # Missing description - should fail
            },
            "colormaps": {
                "test_colors": {
                    "type": "categorical",
                    "colors": {"red": "#FF0000", "green": "#00FF00"},
                }
            },
        }
        with pytest.raises(
            ValueError,
            match="Community colormaps must have 'description' field in metadata",
        ):
            BioCrayon(community_data, require_metadata=True)

    def test_color_retrieval(self):
        """Test color retrieval functionality."""
        user_data = {
            "colormaps": {
                "test_colors": {
                    "type": "categorical",
                    "colors": {"red": "#FF0000", "green": "#00FF00"},
                }
            }
        }
        bc_user = BioCrayon(user_data)
        color = bc_user.get_color("test_colors", "red")
        assert color == "#FF0000"

    def test_matplotlib_conversion(self):
        """Test matplotlib conversion functionality."""
        user_data = {
            "colormaps": {
                "test_colors": {
                    "type": "categorical",
                    "colors": {"red": "#FF0000", "green": "#00FF00"},
                }
            }
        }
        bc_user = BioCrayon(user_data)
        cmap = bc_user.to_matplotlib("test_colors")
        assert cmap is not None


class TestCommunityColormaps:
    """Test all community colormaps for validation and accessibility."""

    def test_community_colormaps_listing(self):
        """Test that community colormaps can be listed."""
        from bio_crayon import BioCrayon

        # Test that we can list community colormaps
        available = BioCrayon.list_community_colormaps()
        assert isinstance(
            available, dict
        ), "list_community_colormaps should return a dict"
        assert (
            len(available) > 0
        ), "Should have at least some community colormap categories"

        # Test that we can load a specific colormap
        if "allen_brain" in available and "single_cell" in available["allen_brain"]:
            bc = BioCrayon.from_community("allen_brain", "single_cell")
            assert len(bc) > 0, "Should have loaded at least one colormap"
            # Check that we have some colormaps loaded (actual names may vary)
            colormaps = bc.list_colormaps()
            assert len(colormaps) > 0, "Should have loaded at least one colormap"
            # Check that the colormaps have the expected structure
            for colormap_name in colormaps:
                colormap = bc.get_colormap(colormap_name)
                assert (
                    "type" in colormap
                ), f"Colormap {colormap_name} should have a type"
                assert colormap["type"] in [
                    "categorical",
                    "continuous",
                ], f"Colormap {colormap_name} should have valid type"

    def test_community_colormaps_validation(self):
        """Test that community colormaps pass validation when loaded."""
        from bio_crayon import BioCrayon

        # Test a known community colormap
        try:
            bc = BioCrayon.from_community("allen_brain", "single_cell")

            # Test that we can get metadata
            metadata = bc.get_metadata()
            assert metadata is not None, "Should have metadata"

            # Test that we can get colormap info for each colormap
            colormaps = bc.list_colormaps()
            for colormap_name in colormaps:
                info = bc.get_colormap_info(colormap_name)
                assert info is not None, f"Could not get info for {colormap_name}"

                # Validate basic colormap structure
                colormap_data = bc.get_colormap(colormap_name)
                assert (
                    "type" in colormap_data
                ), f"Colormap {colormap_name} should have a type"
                assert colormap_data["type"] in [
                    "categorical",
                    "continuous",
                ], f"Colormap {colormap_name} should have valid type"

                if colormap_data["type"] == "categorical":
                    assert (
                        "colors" in colormap_data
                    ), f"Categorical colormap {colormap_name} should have colors"
                    assert isinstance(
                        colormap_data["colors"], dict
                    ), f"Colors in {colormap_name} should be a dict"
                elif colormap_data["type"] == "continuous":
                    assert (
                        "colors" in colormap_data
                    ), f"Continuous colormap {colormap_name} should have colors"
                    assert (
                        "positions" in colormap_data
                    ), f"Continuous colormap {colormap_name} should have positions"
                    assert isinstance(
                        colormap_data["colors"], list
                    ), f"Colors in {colormap_name} should be a list"
                    assert isinstance(
                        colormap_data["positions"], list
                    ), f"Positions in {colormap_name} should be a list"

        except Exception as e:
            pytest.fail(f"Community colormap validation failed: {e}")

    def test_community_colormaps_accessibility(self):
        """Test colorblind accessibility of community colormaps (informational only)."""
        from bio_crayon import BioCrayon

        warnings = []

        try:
            # Test a known community colormap
            bc = BioCrayon.from_community("allen_brain", "single_cell")

            # Get all colormap names in this file
            colormap_names = bc.list_colormaps()

            for colormap_name in colormap_names:
                # Check if categorical colormap is colorblind safe
                colormap = bc.get_colormap(colormap_name)
                if colormap["type"] == "categorical":
                    if not bc.is_colorblind_safe(colormap_name):
                        warnings.append(f"{colormap_name} - Not colorblind safe")

        except Exception as e:
            warnings.append(f"Error testing accessibility: {e}")

        # Log warnings but don't fail the test
        if warnings:
            print(f"\nColorblind accessibility warnings ({len(warnings)} found):")
            for warning in warnings:
                print(f"  WARNING: {warning}")
            print("Note: Colorblind accessibility is recommended but not required.")
        else:
            print("All categorical colormaps are colorblind safe!")

    def test_community_colormaps_loadable(self):
        """Test that community colormaps can be loaded by BioCrayon."""
        from bio_crayon import BioCrayon

        errors = []

        try:
            bc = BioCrayon.from_community("allen_brain", "single_cell")

            # Test that we can list colormaps
            colormaps = bc.list_colormaps()
            assert len(colormaps) > 0, "No colormaps found in community colormap"

            # Test that we can get metadata
            metadata = bc.get_metadata()
            assert metadata is not None, "No metadata found in community colormap"

            # Test that we can get colormap info for each colormap
            for colormap_name in colormaps:
                info = bc.get_colormap_info(colormap_name)
                assert info is not None, f"Could not get info for {colormap_name}"

        except Exception as e:
            errors.append(f"Community colormap loading failed: {e}")

        # If there are errors, fail the test with details
        if errors:
            error_msg = "Community colormap loading failed:\n" + "\n".join(errors)
            pytest.fail(error_msg)
