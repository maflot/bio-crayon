#!/usr/bin/env python3
"""
Simple BioCrayon plotting example using only matplotlib and numpy.

This example demonstrates how to use BioCrayon colormaps with matplotlib
without relying on pandas or seaborn.
"""

import numpy as np
import matplotlib.pyplot as plt
import bio_crayon

# Set matplotlib style
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

def create_artificial_immune_data():
    """Create artificial Allen brain immune data using only numpy."""
    np.random.seed(42)  # For reproducible results
    
    # Define cell types from Allen brain immune colormap (using L1 level)
    cell_types = [
        "T cell", "B cell", "NK cell", "Monocyte", 
        "DC", "ILC", "Progenitor cell", "Platelet"
    ]
    
    # Create artificial data with more realistic distributions
    data = {}
    
    for i, cell_type in enumerate(cell_types):
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
        cell_size = np.random.normal(10, 2, n_cells)
        granularity = np.random.exponential(0.5, n_cells)
        
        data[cell_type] = {
            'expression_level': expression,
            'activation_score': activation,
            'cell_size': cell_size,
            'granularity': granularity
        }
    
    return data

def plot_histograms(data, cell_colors, ax, metric, title, xlabel):
    """Plot overlapping histograms for a given metric."""
    for cell_type, values in data.items():
        ax.hist(values[metric], bins=20, alpha=0.7, 
                label=cell_type, color=cell_colors[cell_type], density=True)
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Density')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax.grid(True, alpha=0.3)

def plot_boxplot(data, cell_colors, ax, metric, title, ylabel):
    """Create a box plot for a given metric."""
    cell_types = list(data.keys())
    metric_data = [data[ct][metric] for ct in cell_types]
    colors = [cell_colors[ct] for ct in cell_types]
    
    bp = ax.boxplot(metric_data, labels=cell_types, patch_artist=True)
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)

def plot_scatter(data, cell_colors, ax, x_metric, y_metric, title, xlabel, ylabel):
    """Create a scatter plot."""
    for cell_type, values in data.items():
        ax.scatter(values[x_metric], values[y_metric], 
                  alpha=0.6, label=cell_type, color=cell_colors[cell_type], s=20)
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    ax.grid(True, alpha=0.3)

def calculate_summary_stats(data):
    """Calculate summary statistics for each cell type."""
    stats = {}
    for cell_type, values in data.items():
        stats[cell_type] = {
            'count': len(values['expression_level']),
            'mean_expression': np.mean(values['expression_level']),
            'mean_activation': np.mean(values['activation_score']),
            'mean_size': np.mean(values['cell_size']),
            'std_expression': np.std(values['expression_level']),
            'std_activation': np.std(values['activation_score']),
            'std_size': np.std(values['cell_size'])
        }
    return stats

def main():
    """Main function demonstrating BioCrayon plotting."""
    print("🎨 BioCrayon Simple Plotting Example")
    print("=" * 50)
    
    try:
        # Load Allen brain immune colormap
        print("Loading Allen brain immune colormap...")
        bc = bio_crayon.BioCrayon.from_community("allen_immune", "single_cell")
        
        # Get colormap for cell types (using L1 level)
        cell_colors = bc["immune_cell_l1"]
        print(f"Available colors for {len(cell_colors)} cell types")
        
    except Exception as e:
        print(f"Error loading BioCrayon colormap: {e}")
        print("Using default colors instead...")
        # Fallback to default colors
        cell_types = ["T cell", "B cell", "NK cell", "Monocyte", 
                     "DC", "ILC", "Progenitor cell", "Platelet"]
        colors = plt.cm.Set3(np.linspace(0, 1, len(cell_types)))
        cell_colors = dict(zip(cell_types, colors))
    
    # Create artificial data
    print("Creating artificial immune cell data...")
    data = create_artificial_immune_data()
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Allen Brain Immune Cell Analysis', fontsize=16, fontweight='bold')
    
    # 1. Expression level histogram
    print("Creating expression level histogram...")
    ax1 = plt.subplot(2, 3, 1)
    plot_histograms(data, cell_colors, ax1, 'expression_level', 
                   'Expression Level Distribution', 'Expression Level')
    
    # 2. Activation score histogram
    print("Creating activation score histogram...")
    ax2 = plt.subplot(2, 3, 2)
    plot_histograms(data, cell_colors, ax2, 'activation_score', 
                   'Activation Score Distribution', 'Activation Score')
    
    # 3. Cell size histogram
    print("Creating cell size histogram...")
    ax3 = plt.subplot(2, 3, 3)
    plot_histograms(data, cell_colors, ax3, 'cell_size', 
                   'Cell Size Distribution', 'Cell Size (μm)')
    
    # 4. Expression level box plot
    print("Creating expression level box plot...")
    ax4 = plt.subplot(2, 3, 4)
    plot_boxplot(data, cell_colors, ax4, 'expression_level', 
                'Expression Level by Cell Type', 'Expression Level')
    
    # 5. Activation score box plot
    print("Creating activation score box plot...")
    ax5 = plt.subplot(2, 3, 5)
    plot_boxplot(data, cell_colors, ax5, 'activation_score', 
                'Activation Score by Cell Type', 'Activation Score')
    
    # 6. Scatter plot
    print("Creating scatter plot...")
    ax6 = plt.subplot(2, 3, 6)
    plot_scatter(data, cell_colors, ax6, 'cell_size', 'expression_level',
                'Cell Size vs Expression Level', 'Cell Size (μm)', 'Expression Level')
    
    plt.tight_layout()
    plt.show()
    
    # Calculate and print summary statistics
    print("\n📊 Summary Statistics:")
    print("-" * 50)
    
    stats = calculate_summary_stats(data)
    total_cells = sum(stats[ct]['count'] for ct in stats)
    
    print(f"Total cells analyzed: {total_cells}")
    print(f"Cell types: {len(data)}")
    
    print(f"\n{'Cell Type':<15} {'Count':<8} {'Expr Mean':<10} {'Expr Std':<10} {'Act Mean':<10} {'Size Mean':<10}")
    print("-" * 80)
    
    for cell_type, stat in stats.items():
        print(f"{cell_type:<15} {stat['count']:<8} {stat['mean_expression']:<10.2f} "
              f"{stat['std_expression']:<10.2f} {stat['mean_activation']:<10.2f} "
              f"{stat['mean_size']:<10.2f}")
    
    # Create a second figure with correlation analysis
    print("\nCreating correlation analysis...")
    fig2, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig2.suptitle('Correlation Analysis', fontsize=16, fontweight='bold')
    
    # Combine all data for correlation analysis
    all_expression = np.concatenate([values['expression_level'] for values in data.values()])
    all_activation = np.concatenate([values['activation_score'] for values in data.values()])
    all_size = np.concatenate([values['cell_size'] for values in data.values()])
    all_granularity = np.concatenate([values['granularity'] for values in data.values()])
    
    # Scatter plots for correlations
    axes[0, 0].scatter(all_expression, all_activation, alpha=0.5, s=10)
    axes[0, 0].set_xlabel('Expression Level')
    axes[0, 0].set_ylabel('Activation Score')
    axes[0, 0].set_title('Expression vs Activation')
    corr1 = np.corrcoef(all_expression, all_activation)[0, 1]
    axes[0, 0].text(0.05, 0.95, f'r = {corr1:.3f}', transform=axes[0, 0].transAxes,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    axes[0, 1].scatter(all_size, all_expression, alpha=0.5, s=10)
    axes[0, 1].set_xlabel('Cell Size')
    axes[0, 1].set_ylabel('Expression Level')
    axes[0, 1].set_title('Size vs Expression')
    corr2 = np.corrcoef(all_size, all_expression)[0, 1]
    axes[0, 1].text(0.05, 0.95, f'r = {corr2:.3f}', transform=axes[0, 1].transAxes,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    axes[1, 0].scatter(all_size, all_activation, alpha=0.5, s=10)
    axes[1, 0].set_xlabel('Cell Size')
    axes[1, 0].set_ylabel('Activation Score')
    axes[1, 0].set_title('Size vs Activation')
    corr3 = np.corrcoef(all_size, all_activation)[0, 1]
    axes[1, 0].text(0.05, 0.95, f'r = {corr3:.3f}', transform=axes[1, 0].transAxes,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    axes[1, 1].scatter(all_granularity, all_expression, alpha=0.5, s=10)
    axes[1, 1].set_xlabel('Granularity')
    axes[1, 1].set_ylabel('Expression Level')
    axes[1, 1].set_title('Granularity vs Expression')
    corr4 = np.corrcoef(all_granularity, all_expression)[0, 1]
    axes[1, 1].text(0.05, 0.95, f'r = {corr4:.3f}', transform=axes[1, 1].transAxes,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    # Show colormap information if BioCrayon loaded successfully
    try:
        print(f"\n🎨 Colormap Information:")
        print("-" * 30)
        print(f"Colormap name: {bc.metadata.get('name', 'Unknown')}")
        print(f"Number of colors: {len(cell_colors)}")
        print(f"Color mapping:")
        for cell_type, color in cell_colors.items():
            if hasattr(color, 'hex'):
                print(f"  {cell_type}: {color.hex}")
            else:
                print(f"  {cell_type}: {color}")
    except:
        print("\nUsed default matplotlib colors")

if __name__ == "__main__":
    main()