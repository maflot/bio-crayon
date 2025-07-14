"""
Example usage of the gene expression heatmaps colormap from the community collection.
"""

import bio_crayon
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Load the expression heatmaps colormap from community collection
    bc = bio_crayon.BioCrayon.from_community("genomics", "expression_heatmaps")
    
    # Simulate gene expression data (log2 fold changes)
    np.random.seed(42)
    genes = [f"Gene_{i}" for i in range(1, 11)]
    conditions = ["Control", "Treatment_A", "Treatment_B", "Treatment_C"]
    
    # Generate mock expression data with log2 fold changes
    expression_data = np.random.normal(0, 1, (len(genes), len(conditions)))
    
    # Normalize to [-3, 3] range for the colormap
    expression_data = np.clip(expression_data, -3, 3)
    
    # Get colors for expression values
    print("Gene Expression Heatmap Colors:")
    for i, gene in enumerate(genes):
        for j, condition in enumerate(conditions):
            value = expression_data[i, j]
            color = bc.get_color("expression_heatmaps", value)
            print(f"  {gene} ({condition}): {value:.2f} -> {color}")
    
    # Create a heatmap visualization
    print("\nGenerating expression heatmap...")
    
    # Convert to matplotlib colormap
    cmap = bc.to_matplotlib("expression_heatmaps")
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(expression_data, cmap=cmap, aspect='auto')
    
    # Add labels
    ax.set_xticks(range(len(conditions)))
    ax.set_yticks(range(len(genes)))
    ax.set_xticklabels(conditions, rotation=45)
    ax.set_yticklabels(genes)
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Log2 Fold Change')
    
    ax.set_title('Gene Expression Heatmap')
    plt.tight_layout()
    plt.show()
    
    # Get colormap information
    info = bc.get_colormap_info("expression_heatmaps")
    print(f"\nColormap Info:")
    print(f"  Type: {info['type']}")
    print(f"  Range: {info['range']}")
    print(f"  Description: {info['description']}")

if __name__ == "__main__":
    main() 