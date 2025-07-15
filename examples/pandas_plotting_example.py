#!/usr/bin/env python3
"""
Pandas plotting example with BioCrayon colormaps.

This example demonstrates how to use BioCrayon colormaps with pandas
for creating histograms with artificial Allen brain immune data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bio_crayon

# Set style for better plots
plt.style.use('default')

def create_artificial_immune_data(n_samples=1000):
    """Create artificial Allen brain immune data."""
    np.random.seed(42)  # For reproducible results
    
    # Define cell types from Allen brain immune colormap (using L1 level)
    cell_types = [
        "T cell", "B cell", "NK cell", "Monocyte", 
        "DC", "ILC", "Progenitor cell", "Platelet"
    ]
    
    # Create artificial data
    data = {
        'cell_type': np.random.choice(cell_types, n_samples),
        'expression_level': np.random.exponential(2, n_samples),
        'cell_count': np.random.poisson(50, n_samples),
        'activation_score': np.random.normal(0.5, 0.2, n_samples)
    }
    
    return pd.DataFrame(data)

def main():
    """Main function demonstrating pandas plotting with BioCrayon."""
    print("🎨 BioCrayon Pandas Plotting Example")
    print("=" * 50)
    
    # Load Allen brain immune colormap
    print("Loading Allen brain immune colormap...")
    bc = bio_crayon.BioCrayon.from_community("allen_immune", "single_cell")
    
    # Create artificial data
    print("Creating artificial immune cell data...")
    df = create_artificial_immune_data(2000)
    
    # Get colormap for cell types
    cell_colors = bc["immune_cell_l1"]
    print(f"Available colors for {len(cell_colors)} cell types")
    
    # Create figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Allen Brain Immune Cell Analysis', fontsize=16, fontweight='bold')
    
    # 1. Histogram of expression levels by cell type
    print("Creating expression level histogram...")
    ax1 = axes[0, 0]
    for cell_type in df['cell_type'].unique():
        subset = df[df['cell_type'] == cell_type]
        color = cell_colors.get(cell_type, '#666666')
        ax1.hist(subset['expression_level'], alpha=0.7, label=cell_type, 
                color=color, bins=20, density=True)
    
    ax1.set_xlabel('Expression Level')
    ax1.set_ylabel('Density')
    ax1.set_title('Expression Level Distribution by Cell Type')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # 2. Histogram of cell counts
    print("Creating cell count histogram...")
    ax2 = axes[0, 1]
    ax2.hist(df['cell_count'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
    ax2.set_xlabel('Cell Count')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Cell Counts')
    ax2.grid(True, alpha=0.3)
    
    # 3. Activation score by cell type
    print("Creating activation score histogram...")
    ax3 = axes[1, 0]
    for cell_type in df['cell_type'].unique():
        subset = df[df['cell_type'] == cell_type]
        color = cell_colors.get(cell_type, '#666666')
        ax3.hist(subset['activation_score'], alpha=0.7, label=cell_type, 
                color=color, bins=15, density=True)
    
    ax3.set_xlabel('Activation Score')
    ax3.set_ylabel('Density')
    ax3.set_title('Activation Score Distribution by Cell Type')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(True, alpha=0.3)
    
    # 4. Cell type frequency
    print("Creating cell type frequency plot...")
    ax4 = axes[1, 1]
    cell_counts = df['cell_type'].value_counts()
    colors = [cell_colors.get(ct, '#666666') for ct in cell_counts.index]
    
    bars = ax4.bar(range(len(cell_counts)), cell_counts.values, color=colors, alpha=0.8)
    ax4.set_xlabel('Cell Type')
    ax4.set_ylabel('Count')
    ax4.set_title('Cell Type Frequency')
    ax4.set_xticks(range(len(cell_counts)))
    ax4.set_xticklabels(cell_counts.index, rotation=45, ha='right')
    ax4.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, count in zip(bars, cell_counts.values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{count}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    # Print summary statistics
    print("\n📊 Summary Statistics:")
    print("-" * 30)
    print(f"Total cells analyzed: {len(df)}")
    print(f"Cell types: {len(df['cell_type'].unique())}")
    print(f"Average expression level: {df['expression_level'].mean():.2f}")
    print(f"Average cell count: {df['cell_count'].mean():.2f}")
    print(f"Average activation score: {df['activation_score'].mean():.2f}")
    
    # Show colormap information
    print(f"\n🎨 Colormap Information:")
    print("-" * 30)
    print(f"Colormap name: {bc.metadata.get('name', 'Unknown')}")
    print(f"Number of colors: {len(cell_colors)}")
    print(f"Colorblind safe: {bc.metadata.get('accessibility', {}).get('colorblind_safe', 'Unknown')}")

if __name__ == "__main__":
    main() 