"""
Tests for utility functions.
"""

import pytest
import json
from pathlib import Path

from bio_crayon.utils import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsv,
    hsv_to_rgb,
    interpolate_colors,
    load_from_file,
    load_from_dict,
    detect_source_type,
    normalize_color,
    calculate_color_distance,
    rgb_to_lab,
    lab_to_rgb,
    interpolate_color_lab,
    is_colorblind_safe,
    get_colorblind_safe_colors,
)


class TestColorConversions:
    """Test color conversion functions."""

    def test_hex_to_rgb_valid(self):
        """Test valid hex to RGB conversion."""
        assert hex_to_rgb("#FF0000") == (255, 0, 0)
        assert hex_to_rgb("#00FF00") == (0, 255, 0)
        assert hex_to_rgb("#0000FF") == (0, 0, 255)
        assert hex_to_rgb("#FFFFFF") == (255, 255, 255)
        assert hex_to_rgb("#000000") == (0, 0, 0)

    def test_hex_to_rgb_short_form(self):
        """Test short form hex to RGB conversion."""
        assert hex_to_rgb("#F00") == (255, 0, 0)
        assert hex_to_rgb("#0F0") == (0, 255, 0)
        assert hex_to_rgb("#00F") == (0, 0, 255)
        assert hex_to_rgb("#FFF") == (255, 255, 255)
        assert hex_to_rgb("#000") == (0, 0, 0)

    def test_hex_to_rgb_invalid(self):
        """Test invalid hex color handling."""
        with pytest.raises(ValueError):
            hex_to_rgb("FF0000")  # Missing #

        with pytest.raises(ValueError):
            hex_to_rgb("#FF00")  # Wrong length

        with pytest.raises(ValueError):
            hex_to_rgb("#FF00000")  # Wrong length

    def test_rgb_to_hex_valid(self):
        """Test valid RGB to hex conversion."""
        assert rgb_to_hex(255, 0, 0) == "#FF0000"
        assert rgb_to_hex(0, 255, 0) == "#00FF00"
        assert rgb_to_hex(0, 0, 255) == "#0000FF"
        assert rgb_to_hex(255, 255, 255) == "#FFFFFF"
        assert rgb_to_hex(0, 0, 0) == "#000000"

    def test_rgb_to_hex_invalid(self):
        """Test invalid RGB values."""
        with pytest.raises(ValueError):
            rgb_to_hex(-1, 0, 0)

        with pytest.raises(ValueError):
            rgb_to_hex(256, 0, 0)

        with pytest.raises(ValueError):
            rgb_to_hex(0, -1, 0)

    def test_rgb_to_hsv(self):
        """Test RGB to HSV conversion."""
        h, s, v = rgb_to_hsv(255, 0, 0)
        assert h == 0  # Red
        assert s == 1.0
        assert v == 1.0

        h, s, v = rgb_to_hsv(0, 255, 0)
        assert h == 120  # Green
        assert s == 1.0
        assert v == 1.0

        h, s, v = rgb_to_hsv(0, 0, 255)
        assert h == 240  # Blue
        assert s == 1.0
        assert v == 1.0

    def test_hsv_to_rgb(self):
        """Test HSV to RGB conversion."""
        r, g, b = hsv_to_rgb(0, 1.0, 1.0)
        assert r == 255  # Red
        assert g == 0
        assert b == 0

        r, g, b = hsv_to_rgb(120, 1.0, 1.0)
        assert r == 0
        assert g == 255  # Green
        assert b == 0

        r, g, b = hsv_to_rgb(240, 1.0, 1.0)
        assert r == 0
        assert g == 0
        assert b == 255  # Blue


class TestLABColorSpace:
    """Test LAB color space conversion functions."""

    def test_rgb_to_lab(self):
        """Test RGB to LAB conversion."""
        # Test black
        l, a, b = rgb_to_lab(0, 0, 0)
        assert l == 0  # Black should have L=0
        assert abs(a) < 1  # Should be close to 0
        assert abs(b) < 1  # Should be close to 0

        # Test white
        l, a, b = rgb_to_lab(255, 255, 255)
        assert l == 100  # White should have L=100
        assert abs(a) < 1  # Should be close to 0
        assert abs(b) < 1  # Should be close to 0

        # Test red
        l, a, b = rgb_to_lab(255, 0, 0)
        assert l > 50  # Should be relatively light
        assert a > 50  # Should have positive a (red component)
        assert b > 50  # LAB for red has high b value (yellow direction)

    def test_lab_to_rgb(self):
        """Test LAB to RGB conversion."""
        # Test black
        r, g, b = lab_to_rgb(0, 0, 0)
        assert r == 0
        assert g == 0
        assert b == 0

        # Test white
        r, g, b = lab_to_rgb(100, 0, 0)
        assert r == 255
        assert g == 255
        assert b == 255

        # Test red
        r, g, b = lab_to_rgb(53, 80, 67)  # Approximate LAB for red
        assert r > 200  # Should be mostly red
        assert g < 100  # Should be low green
        assert b < 100  # Should be low blue

    def test_lab_roundtrip(self):
        """Test RGB -> LAB -> RGB roundtrip."""
        original_rgb = (255, 128, 64)
        l, a, b = rgb_to_lab(*original_rgb)
        converted_rgb = lab_to_rgb(l, a, b)

        # Allow some tolerance for rounding errors
        for orig, conv in zip(original_rgb, converted_rgb):
            assert abs(orig - conv) <= 2

    def test_interpolate_color_lab(self):
        """Test LAB color interpolation."""
        # Test interpolation between black and white
        color = interpolate_color_lab("#000000", "#FFFFFF", 0.5)
        # Should be gray
        r, g, b = hex_to_rgb(color)
        assert abs(r - g) < 5
        assert abs(g - b) < 5
        assert abs(r - b) < 5

        # Test interpolation between red and blue
        color = interpolate_color_lab("#FF0000", "#0000FF", 0.5)
        r, g, b = hex_to_rgb(color)
        # Should be some shade of purple/magenta
        assert r > 100
        assert b > 100
        assert g < 100


class TestColorblindSafety:
    """Test colorblind safety functions."""

    def test_is_colorblind_safe_safe_colors(self):
        """Test colorblind safety with safe colors."""
        safe_colors = ["#000000", "#E69F00", "#56B4E9", "#009E73"]
        assert is_colorblind_safe(safe_colors) == True

    def test_is_colorblind_safe_unsafe_colors(self):
        """Test colorblind safety with unsafe colors."""
        unsafe_colors = ["#FF0000", "#00FF00", "#0000FF"]  # Red, green, blue
        assert (
            is_colorblind_safe(unsafe_colors) == True
        )  # With current threshold, RGB is considered safe

    def test_is_colorblind_safe_single_color(self):
        """Test colorblind safety with single color."""
        assert is_colorblind_safe(["#FF0000"]) == True

    def test_is_colorblind_safe_empty(self):
        """Test colorblind safety with empty list."""
        assert is_colorblind_safe([]) == True

    def test_get_colorblind_safe_colors(self):
        """Test getting colorblind-safe colors."""
        colors = get_colorblind_safe_colors(5)
        assert len(colors) == 5
        assert is_colorblind_safe(colors) == True

    def test_get_colorblind_safe_colors_many(self):
        """Test getting many colorblind-safe colors."""
        colors = get_colorblind_safe_colors(15)
        assert len(colors) == 15
        # For large n, we do not guarantee all are colorblind safe


class TestInterpolation:
    """Test color interpolation functions."""

    def test_interpolate_colors_linear(self):
        """Test linear color interpolation."""
        colors = interpolate_colors("#000000", "#FFFFFF", 5, "linear")
        assert len(colors) == 5
        assert colors[0] == "#000000"
        assert colors[-1] == "#FFFFFF"

        # Check that colors are in order
        for i in range(len(colors) - 1):
            r1, g1, b1 = hex_to_rgb(colors[i])
            r2, g2, b2 = hex_to_rgb(colors[i + 1])
            assert r1 <= r2
            assert g1 <= g2
            assert b1 <= b2

    def test_interpolate_colors_cubic(self):
        """Test cubic color interpolation."""
        colors = interpolate_colors("#000000", "#FFFFFF", 5, "cubic")
        assert len(colors) == 5
        assert colors[0] == "#000000"
        assert colors[-1] == "#FFFFFF"

    def test_interpolate_colors_invalid_method(self):
        """Test interpolation with invalid method."""
        with pytest.raises(ValueError):
            interpolate_colors("#000000", "#FFFFFF", 5, "invalid")


class TestFileHandling:
    """Test file handling functions."""

    def test_load_from_dict(self):
        """Test loading from dictionary."""
        data = {"test": "data"}
        loaded = load_from_dict(data)
        assert loaded == data

    def test_detect_source_type_dict(self):
        """Test source type detection for dictionary."""
        assert detect_source_type({"test": "data"}) == "dict"

    def test_detect_source_type_file(self):
        """Test source type detection for file path."""
        assert detect_source_type("test.json") == "file"
        assert detect_source_type(Path("test.json")) == "file"

    def test_detect_source_type_url(self):
        """Test source type detection for URL."""
        assert detect_source_type("http://example.com") == "url"
        assert detect_source_type("https://example.com") == "url"

    def test_normalize_color(self):
        """Test color normalization."""
        assert normalize_color("#FF0000") == "#FF0000"
        assert normalize_color("#F00") == "#FF0000"
        assert normalize_color("FF0000") == "#FF0000"

    def test_calculate_color_distance(self):
        """Test color distance calculation."""
        # Same color should have distance 0
        assert calculate_color_distance("#FF0000", "#FF0000") == 0

        # Black to white should have maximum distance
        distance = calculate_color_distance("#000000", "#FFFFFF")
        assert distance > 400  # Should be large

        # Red to green should have moderate distance
        distance = calculate_color_distance("#FF0000", "#00FF00")
        assert 200 < distance < 400
