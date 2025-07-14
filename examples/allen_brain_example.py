"""
Example usage of the Allen Brain Atlas colormap from the community collection.
"""

import bio_crayon


def main():
    # Load the Allen Brain colormap from community collection
    bc = bio_crayon.BioCrayon.from_community("allen_brain", "single_cell")

    # Example cell types from the single cell colormap
    cell_types = ["L2/3 IT", "L4 IT", "L5 IT", "L6 IT", "Pvalb", "Sst", "Vip", "Lamp5"]

    # Get colors for each cell type
    print("Allen Brain Atlas Single Cell Color Mapping:")
    for cell_type in cell_types:
        color = bc.get_color("subclass_name", cell_type)
        print(f"  {cell_type}: {color}")

    # Plot the colormap
    print("\nGenerating colormap visualization...")
    bc.plot_colormap("neuronal_types")

    # Check colorblind safety
    is_safe = bc.is_colorblind_safe("subclass_name")
    print(f"\nColorblind safe: {is_safe}")

    # Get colormap information
    info = bc.get_colormap_info("class_name")
    print(f"\nColormap Info:")
    print(f"  Type: {info['type']}")
    print(f"  Categories: {info['categories']}")
    print(f"  Description: {info['description']}")

    # Get metadata
    metadata = bc.get_metadata()
    print(f"\nMetadata:")
    print(f"  Name: {metadata.get('name', 'N/A')}")
    print(f"  Author: {metadata.get('author', 'N/A')}")
    print(f"  DOI: {metadata.get('doi', 'N/A')}")
    print(f"  Keywords: {metadata.get('keywords', [])}")


if __name__ == "__main__":
    main()
