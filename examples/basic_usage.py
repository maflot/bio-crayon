#!/usr/bin/env python3
"""
Basic usage example for BioCrayon.

This example demonstrates the main features of the BioCrayon package
including loading colormaps, accessing colors, and matplotlib integration.
"""

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from bio_crayon import BioCrayon


def main():
    """Demonstrate basic BioCrayon usage."""

    # Load the built-in Allen Brain Atlas colormaps
    allen_brain_path = (
        Path(__file__).parent.parent
        / "bio_crayon"
        / "builtin_colormaps"
        / "allen_brain.json"
    )
    bc = BioCrayon(allen_brain_path)

    print("=== BioCrayon Basic Usage Example ===\n")

    # Display metadata
    metadata = bc.get_metadata()
    print(f"Loaded colormap collection: {metadata['name']}")
    print(f"Version: {metadata['version']}")
    print(f"Description: {metadata.get('description', 'No description')}")
    print()

    # List available colormaps
    colormaps = bc.list_colormaps()
    print(f"Available colormaps: {colormaps}")
    print()

    # Demonstrate categorical colormap usage
    print("=== Categorical Colormap Example ===")
    brain_regions = bc.get_colormap("brain_regions")
    print(f"Type: {brain_regions['type']}")
    print(f"Description: {brain_regions.get('description', 'No description')}")

    # Get colors for specific categories
    categories = ["cortex", "hippocampus", "cerebellum"]
    for category in categories:
        color = bc.get_color("brain_regions", category)
        print(f"  {category}: {color}")
    print()

    # Demonstrate continuous colormap usage
    print("=== Continuous Colormap Example ===")
    activity_heatmap = bc.get_colormap("activity_heatmap")
    print(f"Type: {activity_heatmap['type']}")
    print(f"Description: {activity_heatmap.get('description', 'No description')}")

    # Get colors for different values
    values = [0.0, 0.25, 0.5, 0.75, 1.0]
    for value in values:
        color = bc.get_color("activity_heatmap", value)
        print(f"  Value {value}: {color}")
    print()

    # Demonstrate matplotlib integration
    print("=== Matplotlib Integration ===")

    # Create a simple heatmap using the continuous colormap
    data = np.random.rand(10, 10)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Use the continuous colormap
    cmap = bc.to_matplotlib("activity_heatmap")
    im1 = ax1.imshow(data, cmap=cmap)
    ax1.set_title("Activity Heatmap (Continuous)")
    plt.colorbar(im1, ax=ax1)

    # Create a categorical plot
    categories = list(brain_regions["colors"].keys())[:5]  # Use first 5 categories
    values = np.random.randint(0, len(categories), 20)

    colors = [bc.get_color("brain_regions", categories[i]) for i in values]
    ax2.scatter(range(len(values)), values, c=colors, s=100)
    ax2.set_title("Brain Regions (Categorical)")
    ax2.set_yticks(range(len(categories)))
    ax2.set_yticklabels(categories)

    plt.tight_layout()
    plt.show()

    # Demonstrate adding a new colormap
    print("=== Adding Custom Colormap ===")

    # Create a custom colormap
    custom_colormap = {
        "type": "categorical",
        "description": "Custom test colormap",
        "colors": {"test1": "#FF6B6B", "test2": "#4ECDC4", "test3": "#45B7D1"},
    }

    bc.add_colormap("custom_test", custom_colormap)
    print(f"Added custom colormap. Available colormaps: {bc.list_colormaps()}")

    # Get information about the new colormap
    info = bc.get_colormap_info("custom_test")
    print(f"Custom colormap info: {info}")
    print()

    # Demonstrate saving
    print("=== Saving Colormaps ===")
    output_path = Path(__file__).parent / "output_colormaps.json"
    bc.save(output_path)
    print(f"Saved colormaps to: {output_path}")

    # Verify the saved file
    bc2 = BioCrayon(output_path)
    print(f"Loaded saved colormaps. Available: {bc2.list_colormaps()}")

    # Clean up
    output_path.unlink()
    print("Cleaned up temporary file.")


def demonstrate_color_utilities():
    """Demonstrate color utility functions."""
    print("\n=== Color Utility Examples ===")

    from bio_crayon.utils import hex_to_rgb, rgb_to_hex, interpolate_colors

    # Color conversion
    hex_color = "#FF6B6B"
    rgb = hex_to_rgb(hex_color)
    back_to_hex = rgb_to_hex(*rgb)

    print(f"Hex: {hex_color} -> RGB: {rgb} -> Hex: {back_to_hex}")

    # Color interpolation
    colors = interpolate_colors("#000000", "#FFFFFF", steps=5)
    print(f"Interpolated colors: {colors}")

    # Color distance
    from bio_crayon.utils import calculate_color_distance

    distance = calculate_color_distance("#FF0000", "#00FF00")
    print(f"Distance between red and green: {distance:.2f}")


if __name__ == "__main__":
    main()
    demonstrate_color_utilities()
