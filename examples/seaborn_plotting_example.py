#!/usr/bin/env python3
"""
Seaborn plotting example with BioCrayon colormaps.

This example demonstrates how to use BioCrayon colormaps with seaborn
for creating histograms with artificial Allen brain immune data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import bio_crayon

# Set seaborn style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def create_artificial_immune_data(n_samples=1500):
    """Create artificial Allen brain immune data for seaborn plotting."""
    np.random.seed(42)  # For reproducible results
    
    # Define cell types from Allen brain immune colormap (using L1 level)
    cell_types = [
        "T cell", "B cell", "NK cell", "Monocyte", 
        "DC", "ILC", "Progenitor cell", "Platelet"
    ]
    
    # Create artificial data with more realistic distributions
    data = []
    for cell_type in cell_types:
        n_cells = np.random.randint(100, 300)
        
        # Different distributions for different cell types
        if cell_type == "B cell":
            expression = np.random.normal(3.5, 1.2, n_cells)
            activation = np.random.beta(2, 5, n_cells)
        elif cell_type == "T cell":
            expression = np.random.normal(4.2, 1.0, n_cells)
            activation = np.random.beta(3, 3, n_cells)
        elif cell_type == "NK cell":
            expression = np.random.normal(2.8, 0.8, n_cells)
            activation = np.random.beta(4, 2, n_cells)
        elif cell_type == "Monocyte":
            expression = np.random.normal(3.8, 1.5, n_cells)
            activation = np.random.beta(2, 4, n_cells)
        elif cell_type == "DC":
            expression = np.random.normal(3.0, 1.1, n_cells)
            activation = np.random.beta(3, 4, n_cells)
        elif cell_type == "ILC":
            expression = np.random.normal(2.5, 0.9, n_cells)
            activation = np.random.beta(1, 3, n_cells)
        elif cell_type == "Progenitor cell":
            expression = np.random.normal(2.2, 0.7, n_cells)
            activation = np.random.beta(1, 4, n_cells)
        else:  # Platelet
            expression = np.random.normal(1.8, 0.6, n_cells)
            activation = np.random.beta(1, 5, n_cells)
        
        # Add some noise and ensure positive values
        expression = np.abs(expression)
        activation = np.clip(activation, 0, 1)
        
        for i in range(n_cells):
            data.append({
                'cell_type': cell_type,
                'expression_level': expression[i],
                'activation_score': activation[i],
                'cell_size': np.random.normal(10, 2),
                'granularity': np.random.exponential(0.5)
            })
    
    return pd.DataFrame(data)

def main():
    """Main function demonstrating seaborn plotting with BioCrayon."""
    print("🎨 BioCrayon Seaborn Plotting Example")
    print("=" * 50)
    
    # Load Allen brain immune colormap
    print("Loading Allen brain immune colormap...")
    bc = bio_crayon.BioCrayon.from_community("allen_immune", "single_cell")
    
    # Create artificial data
    print("Creating artificial immune cell data...")
    df = create_artificial_immune_data()
    
    # Get colormap for cell types (using L1 level)
    cell_colors = bc["immune_cell_l1"]
    print(f"Available colors for {len(cell_colors)} cell types")
    
    # Create a custom color palette for seaborn
    color_palette = list(cell_colors.values())
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Allen Brain Immune Cell Analysis with Seaborn', 
                 fontsize=16, fontweight='bold')
    
    # 1. Histogram of expression levels by cell type
    print("Creating expression level histogram with seaborn...")
    plt.subplot(2, 3, 1)
    sns.histplot(data=df, x='expression_level', hue='cell_type', 
                palette=color_palette, alpha=0.7, bins=20, kde=True)
    plt.title('Expression Level Distribution by Cell Type')
    plt.xlabel('Expression Level')
    plt.ylabel('Count')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 2. Histogram of activation scores
    print("Creating activation score histogram...")
    plt.subplot(2, 3, 2)
    sns.histplot(data=df, x='activation_score', hue='cell_type', 
                palette=color_palette, alpha=0.7, bins=15, kde=True)
    plt.title('Activation Score Distribution by Cell Type')
    plt.xlabel('Activation Score')
    plt.ylabel('Count')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 3. Cell size distribution
    print("Creating cell size histogram...")
    plt.subplot(2, 3, 3)
    sns.histplot(data=df, x='cell_size', hue='cell_type', 
                palette=color_palette, alpha=0.7, bins=20, kde=True)
    plt.title('Cell Size Distribution by Cell Type')
    plt.xlabel('Cell Size (μm)')
    plt.ylabel('Count')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 4. Box plot of expression levels
    print("Creating expression level box plot...")
    plt.subplot(2, 3, 4)
    sns.boxplot(data=df, x='cell_type', y='expression_level', 
               palette=color_palette)
    plt.title('Expression Level by Cell Type')
    plt.xlabel('Cell Type')
    plt.ylabel('Expression Level')
    plt.xticks(rotation=45, ha='right')
    
    # 5. Violin plot of activation scores
    print("Creating activation score violin plot...")
    plt.subplot(2, 3, 5)
    sns.violinplot(data=df, x='cell_type', y='activation_score', 
                  palette=color_palette, inner='box')
    plt.title('Activation Score Distribution by Cell Type')
    plt.xlabel('Cell Type')
    plt.ylabel('Activation Score')
    plt.xticks(rotation=45, ha='right')
    
    # 6. Scatter plot with cell size vs expression
    print("Creating scatter plot...")
    plt.subplot(2, 3, 6)
    sns.scatterplot(data=df, x='cell_size', y='expression_level', 
                   hue='cell_type', palette=color_palette, alpha=0.7, s=50)
    plt.title('Cell Size vs Expression Level')
    plt.xlabel('Cell Size (μm)')
    plt.ylabel('Expression Level')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()
    
    # Create a separate figure for advanced seaborn plots
    print("Creating advanced seaborn visualizations...")
    fig2, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig2.suptitle('Advanced Seaborn Visualizations', fontsize=16, fontweight='bold')
    
    # 1. Joint plot
    print("Creating joint plot...")
    sns.jointplot(data=df, x='expression_level', y='activation_score', 
                 hue='cell_type', palette=color_palette, alpha=0.7, 
                 height=6, ax=axes[0, 0])
    axes[0, 0].set_title('Expression vs Activation by Cell Type')
    
    # 2. Pair plot (subset of variables)
    print("Creating pair plot...")
    subset_df = df[['expression_level', 'activation_score', 'cell_size', 'cell_type']]
    sns.pairplot(subset_df, hue='cell_type', palette=color_palette, 
                diag_kind='kde', height=2.5)
    
    # 3. Heatmap of correlations
    print("Creating correlation heatmap...")
    numeric_cols = ['expression_level', 'activation_score', 'cell_size', 'granularity']
    corr_matrix = df[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
               square=True, ax=axes[1, 0])
    axes[1, 0].set_title('Correlation Matrix')
    
    # 4. Faceted histogram
    print("Creating faceted histogram...")
    g = sns.FacetGrid(df, col='cell_type', col_wrap=4, height=2.5)
    g.map_dataframe(sns.histplot, x='expression_level', bins=15, alpha=0.7)
    g.set_titles(col_template='{col_name}')
    g.fig.suptitle('Expression Level Distribution by Cell Type', y=1.02)
    
    plt.tight_layout()
    plt.show()
    
    # Print summary statistics
    print("\n📊 Summary Statistics:")
    print("-" * 30)
    print(f"Total cells analyzed: {len(df)}")
    print(f"Cell types: {len(df['cell_type'].unique())}")
    
    for cell_type in df['cell_type'].unique():
        subset = df[df['cell_type'] == cell_type]
        print(f"\n{cell_type}:")
        print(f"  Count: {len(subset)}")
        print(f"  Avg expression: {subset['expression_level'].mean():.2f}")
        print(f"  Avg activation: {subset['activation_score'].mean():.2f}")
        print(f"  Avg size: {subset['cell_size'].mean():.2f}")
    
    # Show colormap information
    print(f"\n🎨 Colormap Information:")
    print("-" * 30)
    print(f"Colormap name: {bc.metadata.get('name', 'Unknown')}")
    print(f"Number of colors: {len(cell_colors)}")
    print(f"Colorblind safe: {bc.metadata.get('accessibility', {}).get('colorblind_safe', 'Unknown')}")

if __name__ == "__main__":
    main() 