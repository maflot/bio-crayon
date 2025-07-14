"""
Example usage of the Allen Immune Atlas colormap from the community collection.
"""

import bio_crayon

def main():
    # Load the Allen Immune Atlas colormap from community collection
    bc = bio_crayon.BioCrayon.from_community("allen_immune", "allen_immune_single_cell")
    
    # Example immune cell types
    immune_cells_l1 = [
        "T cell", "B cell", "NK cell", "Monocyte", "DC", "ILC"
    ]
    
    # Get colors for each cell type
    print("Allen Immune Atlas L1 Color Mapping:")
    for cell_type in immune_cells_l1:
        color = bc.get_color("immune_cell_l1", cell_type)
        print(f"  {cell_type}: {color}")
    
    # Test lymphoid cells
    print("\nLymphoid Cells:")
    lymphoid_cells = ["T cell", "B cell", "NK cell", "ILC"]
    for cell_type in lymphoid_cells:
        color = bc.get_color("lymphoid_cells", cell_type)
        print(f"  {cell_type}: {color}")
    
    # Test myeloid cells
    print("\nMyeloid Cells:")
    myeloid_cells = ["Monocyte", "DC"]
    for cell_type in myeloid_cells:
        color = bc.get_color("myeloid_cells", cell_type)
        print(f"  {cell_type}: {color}")
    
    # Test continuous expression
    print("\nImmune Expression Levels:")
    expression_levels = [0.0, 0.25, 0.5, 0.75, 1.0]
    for level in expression_levels:
        color = bc.get_color("immune_expression", level)
        print(f"  Level {level}: {color}")
    
    # Check colorblind safety
    is_safe = bc.is_colorblind_safe("immune_cell_l1")
    print(f"\nColorblind safe: {is_safe}")
    
    # Get colormap information
    info = bc.get_colormap_info("immune_cell_l1")
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