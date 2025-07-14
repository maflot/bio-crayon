"""
Utility functions for BioCrayon color operations and file handling.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Union, Optional
from urllib.parse import urlparse

import numpy as np
import requests

# Add colorblind-safe color sets
COLORBLIND_SAFE_COLORS = [
    "#000000",
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
    "#999999",
    "#FFFFFF",
]

# Deuteranopia (red-green colorblind) safe colors
DEUTERANOPIA_SAFE_COLORS = [
    "#000000",
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#F0E442",
    "#0072B2",
    "#D55E00",
    "#CC79A7",
    "#999999",
    "#FFFFFF",
]


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex color to RGB tuple.

    Args:
        hex_color: Hex color string (e.g., '#FF0000' or '#F00')

    Returns:
        RGB tuple (r, g, b) with values 0-255

    Raises:
        ValueError: If hex_color is not a valid hex color
    """
    if not hex_color.startswith("#"):
        raise ValueError(f"Hex color must start with '#': {hex_color}")

    hex_color = hex_color[1:]  # Remove '#'

    if len(hex_color) == 3:
        # Expand 3-digit hex to 6-digit
        hex_color = "".join([c + c for c in hex_color])
    elif len(hex_color) != 6:
        raise ValueError(f"Invalid hex color length: {hex_color}")

    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_color}")


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values to hex color string.

    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)

    Returns:
        Hex color string (e.g., '#FF0000')

    Raises:
        ValueError: If RGB values are out of range
    """
    for component, name in [(r, "red"), (g, "green"), (b, "blue")]:
        if not isinstance(component, int) or component < 0 or component > 255:
            raise ValueError(f"{name} component must be integer 0-255: {component}")

    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Convert RGB to HSV color space.

    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)

    Returns:
        HSV tuple (h, s, v) with h in [0, 360), s and v in [0, 1]
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    cmax = max(r, g, b)
    cmin = min(r, g, b)
    diff = cmax - cmin

    # Hue calculation
    if diff == 0:
        h = 0
    elif cmax == r:
        h = (60 * ((g - b) / diff) + 360) % 360
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
    else:  # cmax == b
        h = (60 * ((r - g) / diff) + 240) % 360

    # Saturation calculation
    s = 0 if cmax == 0 else diff / cmax

    # Value calculation
    v = cmax

    return (h, s, v)


def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """
    Convert HSV to RGB color space.

    Args:
        h: Hue (0-360)
        s: Saturation (0-1)
        v: Value (0-1)

    Returns:
        RGB tuple (r, g, b) with values 0-255
    """
    if s == 0:
        r = g = b = v
    else:
        h = h / 60
        i = int(h)
        f = h - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))

        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:  # i == 5
            r, g, b = v, p, q

    return (int(r * 255), int(g * 255), int(b * 255))


def rgb_to_lab(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Convert RGB to LAB color space for perceptually uniform interpolation.

    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)

    Returns:
        LAB tuple (l, a, b) with L in [0, 100], a and b in [-128, 127]
    """
    # First convert to XYZ
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    # Apply gamma correction
    r_norm = r_norm**2.2 if r_norm > 0.04045 else r_norm / 12.92
    g_norm = g_norm**2.2 if g_norm > 0.04045 else g_norm / 12.92
    b_norm = b_norm**2.2 if b_norm > 0.04045 else b_norm / 12.92

    # Convert to XYZ
    x = r_norm * 0.4124 + g_norm * 0.3576 + b_norm * 0.1805
    y = r_norm * 0.2126 + g_norm * 0.7152 + b_norm * 0.0722
    z = r_norm * 0.0193 + g_norm * 0.1192 + b_norm * 0.9505

    # Convert to LAB
    x_norm = x / 0.9505
    y_norm = y / 1.0000
    z_norm = z / 1.0890

    x_norm = x_norm ** (1 / 3) if x_norm > 0.008856 else (7.787 * x_norm) + (16 / 116)
    y_norm = y_norm ** (1 / 3) if y_norm > 0.008856 else (7.787 * y_norm) + (16 / 116)
    z_norm = z_norm ** (1 / 3) if z_norm > 0.008856 else (7.787 * z_norm) + (16 / 116)

    l = (116 * y_norm) - 16
    a = 500 * (x_norm - y_norm)
    b = 200 * (y_norm - z_norm)

    return (l, a, b)


def lab_to_rgb(l: float, a: float, b: float) -> Tuple[int, int, int]:
    """
    Convert LAB to RGB color space.

    Args:
        l: L component (0-100)
        a: a component (-128 to 127)
        b: b component (-128 to 127)

    Returns:
        RGB tuple (r, g, b) with values 0-255
    """
    # Convert LAB to XYZ
    y_norm = (l + 16) / 116
    x_norm = a / 500 + y_norm
    z_norm = y_norm - b / 200

    # Convert to XYZ
    x = 0.9505 * (x_norm**3 if x_norm > 0.206897 else (x_norm - 16 / 116) / 7.787)
    y = 1.0000 * (y_norm**3 if y_norm > 0.206897 else (y_norm - 16 / 116) / 7.787)
    z = 1.0890 * (z_norm**3 if z_norm > 0.206897 else (z_norm - 16 / 116) / 7.787)

    # Convert to RGB
    r_norm = x * 3.2406 + y * -1.5372 + z * -0.4986
    g_norm = x * -0.9689 + y * 1.8758 + z * 0.0415
    b_norm = x * 0.0557 + y * -0.2040 + z * 1.0570

    # Apply gamma correction
    r_norm = r_norm ** (1 / 2.2) if r_norm > 0.0031308 else 12.92 * r_norm
    g_norm = g_norm ** (1 / 2.2) if g_norm > 0.0031308 else 12.92 * g_norm
    b_norm = b_norm ** (1 / 2.2) if b_norm > 0.0031308 else 12.92 * b_norm

    # Clamp to [0, 1] and convert to 0-255
    r = max(0, min(255, int(r_norm * 255)))
    g = max(0, min(255, int(g_norm * 255)))
    b = max(0, min(255, int(b_norm * 255)))

    return (r, g, b)


def interpolate_color_lab(color1: str, color2: str, t: float) -> str:
    """
    Interpolate in LAB color space for better perceptual uniformity.

    Args:
        color1: Starting hex color
        color2: Ending hex color
        t: Interpolation factor (0-1)

    Returns:
        Interpolated hex color string

    This method is particularly useful for biological data visualization
    where perceptual uniformity is important for accurate data interpretation.
    """
    # Convert to LAB
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    lab1 = rgb_to_lab(*rgb1)
    lab2 = rgb_to_lab(*rgb2)

    # Interpolate in LAB space
    l = lab1[0] + t * (lab2[0] - lab1[0])
    a = lab1[1] + t * (lab2[1] - lab1[1])
    b = lab1[2] + t * (lab2[2] - lab1[2])

    # Convert back to RGB
    rgb_interp = lab_to_rgb(l, a, b)

    return rgb_to_hex(*rgb_interp)


def is_colorblind_safe(
    colors: List[str], colorblind_type: str = "deuteranopia"
) -> bool:
    """
    Check if a set of colors is distinguishable for colorblind users.

    Args:
        colors: List of hex color strings
        colorblind_type: Type of colorblindness to check for ("deuteranopia", "protanopia", "tritanopia")

    Returns:
        True if colors are distinguishable for the specified colorblind type
    """
    if len(colors) <= 1:
        return True

    # For now, implement a simple check using color distance
    # In a full implementation, you would use specialized colorblind simulation
    min_required_distance = 80  # Stricter threshold for colorblind safety

    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            distance = calculate_color_distance(colors[i], colors[j])
            if distance < min_required_distance:
                return False
    return True


def get_colorblind_safe_colors(
    n_colors: int, colorblind_type: str = "deuteranopia"
) -> List[str]:
    """
    Get a set of colorblind-safe colors.

    Args:
        n_colors: Number of colors needed
        colorblind_type: Type of colorblindness to optimize for

    Returns:
        List of hex color strings that are colorblind-safe
    """
    if colorblind_type == "deuteranopia":
        base_colors = DEUTERANOPIA_SAFE_COLORS
    else:
        base_colors = COLORBLIND_SAFE_COLORS

    if n_colors <= len(base_colors):
        return base_colors[:n_colors]

    # If more colors needed, interpolate between safe colors
    colors = []
    for i in range(n_colors):
        t = i / (n_colors - 1)
        idx1 = int(t * (len(base_colors) - 1))
        idx2 = min(idx1 + 1, len(base_colors) - 1)
        t_local = (t * (len(base_colors) - 1)) - idx1

        color = interpolate_color_lab(base_colors[idx1], base_colors[idx2], t_local)
        colors.append(color)

    return colors


def interpolate_colors(
    color1: str, color2: str, steps: int = 10, interpolation: str = "linear"
) -> List[str]:
    """
    Interpolate between two hex colors.

    Args:
        color1: Starting hex color
        color2: Ending hex color
        steps: Number of interpolation steps
        interpolation: Interpolation method ('linear', 'cubic', 'spline')

    Returns:
        List of hex colors including start and end colors

    Raises:
        ValueError: If interpolation method is not supported
    """
    if interpolation not in ["linear", "cubic", "spline"]:
        raise ValueError(f"Unsupported interpolation method: {interpolation}")

    # Convert to RGB
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    if interpolation == "linear":
        # Linear interpolation in RGB space
        colors = []
        for i in range(steps):
            t = i / (steps - 1)
            r = int(round(rgb1[0] * (1 - t) + rgb2[0] * t))
            g = int(round(rgb1[1] * (1 - t) + rgb2[1] * t))
            b = int(round(rgb1[2] * (1 - t) + rgb2[2] * t))
            colors.append(rgb_to_hex(r, g, b))
        return colors

    elif interpolation == "cubic":
        # Cubic interpolation in HSV space for smoother transitions
        hsv1 = rgb_to_hsv(*rgb1)
        hsv2 = rgb_to_hsv(*rgb2)

        colors = []
        for i in range(steps):
            t = i / (steps - 1)
            # Use cubic easing
            t_cubic = 3 * t * t - 2 * t * t * t

            h = hsv1[0] + t_cubic * (hsv2[0] - hsv1[0])
            s = hsv1[1] + t_cubic * (hsv2[1] - hsv1[1])
            v = hsv1[2] + t_cubic * (hsv2[2] - hsv1[2])

            rgb = hsv_to_rgb(h, s, v)
            colors.append(rgb_to_hex(*rgb))
        return colors

    else:  # spline
        try:
            from scipy.interpolate import interp1d
        except ImportError:
            raise ValueError("Spline interpolation requires scipy")

        x = [0, 1]
        y_r = [rgb1[0], rgb2[0]]
        y_g = [rgb1[1], rgb2[1]]
        y_b = [rgb1[2], rgb2[2]]

        f_r = interp1d(x, y_r, kind="cubic")
        f_g = interp1d(x, y_g, kind="cubic")
        f_b = interp1d(x, y_b, kind="cubic")

        colors = []
        for i in range(steps):
            t = i / (steps - 1)
            r = int(round(f_r(t)))
            g = int(round(f_g(t)))
            b = int(round(f_b(t)))
            colors.append(rgb_to_hex(r, g, b))
        return colors


def load_from_file(filepath: Union[str, Path]) -> Dict[str, Any]:
    """
    Load colormap data from a JSON file.

    Args:
        filepath: Path to JSON file

    Returns:
        Dictionary containing colormap data

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, "r") as f:
        return json.load(f)


def load_from_url(url: str) -> Dict[str, Any]:
    """
    Load colormap data from a URL.

    Args:
        url: URL to JSON file

    Returns:
        Dictionary containing colormap data

    Raises:
        requests.RequestException: If request fails
        json.JSONDecodeError: If response is not valid JSON
    """
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def load_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Load colormap data from a dictionary.

    Args:
        data: Dictionary containing colormap data

    Returns:
        The input dictionary (for consistency)
    """
    return data


def detect_source_type(source: Union[str, Path, Dict[str, Any]]) -> str:
    """
    Detect the type of source (file, URL, or dict).

    Args:
        source: Source to analyze

    Returns:
        Source type: 'file', 'url', or 'dict'
    """
    if isinstance(source, dict):
        return "dict"
    elif isinstance(source, (str, Path)):
        source_str = str(source)
        if source_str.startswith(("http://", "https://")):
            return "url"
        else:
            return "file"
    else:
        raise ValueError(f"Unsupported source type: {type(source)}")


def normalize_color(color: str) -> str:
    """
    Normalize a hex color to 6-digit format, uppercase, with leading '#'.

    Args:
        color: Hex color string (with or without '#')

    Returns:
        Normalized 6-digit hex color (e.g., '#FF0000')
    """
    if not isinstance(color, str):
        raise ValueError(f"Color must be a string: {color}")
    if color.startswith("#"):
        color = color[1:]
    if len(color) == 3:
        color = "".join([c + c for c in color])
    if len(color) != 6:
        raise ValueError(f"Invalid hex color length: {color}")
    try:
        int(color, 16)
    except ValueError:
        raise ValueError(f"Invalid hex color: {color}")
    return f"#{color.upper()}"


def calculate_color_distance(color1: str, color2: str) -> float:
    """
    Calculate Euclidean distance between two colors in RGB space.

    Args:
        color1: First hex color
        color2: Second hex color

    Returns:
        Distance value (0 = identical, higher = more different)
    """
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    return np.sqrt(sum((a - b) ** 2 for a, b in zip(rgb1, rgb2)))
