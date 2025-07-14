"""
Enhanced BioCrayon Features for Biological Data Visualization

This example demonstrates the new features added to BioCrayon:
1. LAB color space interpolation for perceptually uniform gradients
2. Colorblind-safe colormap validation and generation
3. Expression range validation for biological data
4. Matplotlib colorbar generation
5. Biological data type-specific validation
"""

import numpy as np
import matplotlib.pyplot as plt
from bio_crayon import BioCrayon


def demonstrate_lab_interpolation():
    """Demonstrate LAB color space interpolation for better perceptual uniformity."""
    print("=== LAB Color Space Interpolation ===")
    
    # Create a BioCrayon instance with test data
    test_data = {
        "metadata": {"name": "Bio Examples", "version": "1.0"},
        "colormaps": {
            "expression_gradient": {
                "type": "continuous",
                "description": "Gene expression gradient",
                "colors": ["#0000FF", "#FFFFFF", "#FF0000"],
                "positions": [0.0, 0.5, 1.0]
            }
        }
    }
    
    bc = BioCrayon(test_data)
    
    # Compare RGB vs LAB interpolation
    values = np.linspace(0, 1, 10)
    
    print("Comparing RGB vs LAB interpolation:")
    print("Value | RGB Color    | LAB Color")
    print("-" * 35)
    
    for value in values:
        rgb_color = bc.get_color("expression_gradient", value)
        lab_color = bc.get_color_lab("expression_gradient", value)
        print(f"{value:.1f}  | {rgb_color} | {lab_color}")
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # RGB interpolation
    rgb_colors = [bc.get_color("expression_gradient", v) for v in values]
    for i, color in enumerate(rgb_colors):
        ax1.bar(i, 1, color=color, width=0.8)
    ax1.set_title("RGB Interpolation")
    ax1.set_xlabel("Value")
    ax1.set_ylabel("Color")
    
    # LAB interpolation
    lab_colors = [bc.get_color_lab("expression_gradient", v) for v in values]
    for i, color in enumerate(lab_colors):
        ax2.bar(i, 1, color=color, width=0.8)
    ax2.set_title("LAB Interpolation (Perceptually Uniform)")
    ax2.set_xlabel("Value")
    ax2.set_ylabel("Color")
    
    plt.tight_layout()
    plt.show()


def demonstrate_colorblind_safety():
    """Demonstrate colorblind-safe colormap validation and generation."""
    print("\n=== Colorblind Safety Features ===")
    
    # Test data with both safe and unsafe colormaps
    test_data = {
        "metadata": {"name": "Colorblind Test", "version": "1.0"},
        "colormaps": {
            "unsafe_categorical": {
                "type": "categorical",
                "description": "Red-green-blue (problematic for colorblind)",
                "colors": {
                    "low": "#FF0000",
                    "medium": "#00FF00", 
                    "high": "#0000FF"
                }
            },
            "safe_categorical": {
                "type": "categorical",
                "description": "Colorblind-safe colors",
                "colors": {
                    "low": "#000000",
                    "medium": "#E69F00",
                    "high": "#56B4E9"
                }
            }
        }
    }
    
    bc = BioCrayon(test_data)
    
    # Check colorblind safety
    print("Colorblind Safety Check:")
    print(f"Unsafe colormap: {bc.is_colorblind_safe('unsafe_categorical')}")
    print(f"Safe colormap: {bc.is_colorblind_safe('safe_categorical')}")
    
    # Create a new colorblind-safe colormap
    bc.create_colorblind_safe_colormap("auto_safe", 6)
    print(f"Auto-generated safe colormap: {bc.is_colorblind_safe('auto_safe')}")
    
    # Visualize the colormaps
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    colormaps = ["unsafe_categorical", "safe_categorical", "auto_safe"]
    titles = ["Unsafe (Red-Green-Blue)", "Safe (Black-Orange-Blue)", "Auto-Generated Safe"]
    
    for ax, cmap_name, title in zip(axes, colormaps, titles):
        colormap = bc.get_colormap(cmap_name)
        colors = list(colormap["colors"].values())
        categories = list(colormap["colors"].keys())
        
        for i, (color, category) in enumerate(zip(colors, categories)):
            ax.bar(i, 1, color=color, label=category)
        
        ax.set_title(title)
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories)
        ax.set_ylabel("Color")
    
    plt.tight_layout()
    plt.show()


def demonstrate_expression_validation():
    """Demonstrate expression range validation for biological data."""
    print("\n=== Expression Range Validation ===")
    
    # Create test data with different expression ranges
    test_data = {
        "metadata": {"name": "Expression Test", "version": "1.0"},
        "colormaps": {
            "expression_0_1": {
                "type": "continuous",
                "description": "Expression 0-1 range",
                "colors": ["#0000FF", "#FFFFFF", "#FF0000"],
                "positions": [0.0, 0.5, 1.0]
            },
            "expression_0_10": {
                "type": "continuous", 
                "description": "Expression 0-10 range",
                "colors": ["#0000FF", "#FFFFFF", "#FF0000"],
                "positions": [0.0, 5.0, 10.0]
            }
        }
    }
    
    bc = BioCrayon(test_data)
    
    # Test validation with different expected ranges
    test_cases = [
        ("expression_0_1", 0.0, 1.0, "Should pass"),
        ("expression_0_1", -1.0, 2.0, "Should pass with tolerance"),
        ("expression_0_10", 0.0, 10.0, "Should pass"),
        ("expression_0_10", 0.0, 5.0, "Should fail - range too small")
    ]
    
    print("Expression Range Validation Results:")
    print("Colormap | Expected Range | Status | Errors")
    print("-" * 60)
    
    for colormap, min_val, max_val, description in test_cases:
        errors = bc.validate_expression_range(colormap, min_val, max_val)
        status = "PASS" if len(errors) == 0 else "FAIL"
        error_msg = "; ".join(errors) if errors else "None"
        print(f"{colormap:15} | {min_val:5.1f}-{max_val:5.1f} | {status:6} | {error_msg}")


def demonstrate_colorbar_generation():
    """Demonstrate matplotlib colorbar generation."""
    print("\n=== Matplotlib Colorbar Generation ===")
    
    test_data = {
        "metadata": {"name": "Colorbar Test", "version": "1.0"},
        "colormaps": {
            "continuous_example": {
                "type": "continuous",
                "description": "Continuous gradient for expression data",
                "colors": ["#0000FF", "#FFFFFF", "#FF0000"],
                "positions": [0.0, 0.5, 1.0]
            },
            "categorical_example": {
                "type": "categorical",
                "description": "Categorical colors for cell types",
                "colors": {
                    "neuron": "#FF0000",
                    "glia": "#00FF00", 
                    "endothelial": "#0000FF",
                    "immune": "#FFFF00"
                }
            }
        }
    }
    
    bc = BioCrayon(test_data)
    
    # Generate colorbars
    fig1 = bc.get_colorbar("continuous_example", figsize=(1, 6))
    fig1.suptitle("Continuous Colormap Colorbar")
    
    fig2 = bc.get_colorbar("categorical_example", figsize=(1, 6))
    fig2.suptitle("Categorical Colormap Colorbar")
    
    plt.show()


def demonstrate_bio_validation():
    """Demonstrate biological data type-specific validation."""
    print("\n=== Biological Data Type Validation ===")
    
    test_data = {
        "metadata": {"name": "Bio Validation Test", "version": "1.0"},
        "colormaps": {
            "good_expression": {
                "type": "continuous",
                "description": "Good expression colormap with high contrast",
                "colors": ["#0000FF", "#FFFFFF", "#FF0000"],
                "positions": [0.0, 0.5, 1.0]
            },
            "poor_expression": {
                "type": "continuous",
                "description": "Poor expression colormap with low contrast",
                "colors": ["#808080", "#909090", "#A0A0A0"],
                "positions": [0.0, 0.5, 1.0]
            },
            "sequence_colormap": {
                "type": "categorical",
                "description": "Categorical colormap for sequence data",
                "colors": {
                    "A": "#FF0000",
                    "T": "#00FF00",
                    "G": "#0000FF",
                    "C": "#FFFF00"
                }
            }
        }
    }
    
    bc = BioCrayon(test_data)
    
    # Test validation for different biological data types
    test_cases = [
        ("good_expression", "expression", "Should pass"),
        ("poor_expression", "expression", "Should fail - low contrast"),
        ("sequence_colormap", "sequence", "Should pass"),
        ("good_expression", "sequence", "Should fail - wrong type")
    ]
    
    print("Biological Data Type Validation Results:")
    print("Colormap | Data Type | Status | Errors")
    print("-" * 50)
    
    for colormap, bio_type, description in test_cases:
        errors = bc.validate_bio_requirements(colormap, bio_type)
        status = "PASS" if len(errors) == 0 else "FAIL"
        error_msg = "; ".join(errors) if errors else "None"
        print(f"{colormap:15} | {bio_type:10} | {status:6} | {error_msg}")


def demonstrate_complete_workflow():
    """Demonstrate a complete biological data visualization workflow."""
    print("\n=== Complete Biological Data Workflow ===")
    
    # Simulate gene expression data
    np.random.seed(42)
    expression_data = np.random.normal(5, 2, (10, 10))
    
    # Create a BioCrayon instance
    bc = BioCrayon()
    
    # Create a colorblind-safe expression colormap
    bc.create_colorblind_safe_colormap("expression_safe", 8)
    
    # Validate the colormap for expression data
    errors = bc.validate_bio_requirements("expression_safe", "expression")
    if errors:
        print(f"Warning: {errors}")
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot expression data with regular interpolation
    im1 = ax1.imshow(expression_data, cmap=bc.to_matplotlib("expression_safe"))
    ax1.set_title("Expression Data (Regular Interpolation)")
    plt.colorbar(im1, ax=ax1)
    
    # Plot expression data with LAB interpolation
    # Note: We'd need to create a custom colormap with LAB interpolation
    # For now, we'll use the same colormap but demonstrate the concept
    im2 = ax2.imshow(expression_data, cmap=bc.to_matplotlib("expression_safe"))
    ax2.set_title("Expression Data (LAB Interpolation - Concept)")
    plt.colorbar(im2, ax=ax2)
    
    plt.tight_layout()
    plt.show()
    
    print("Workflow completed successfully!")


if __name__ == "__main__":
    print("BioCrayon Enhanced Features Demonstration")
    print("=" * 50)
    
    # Run all demonstrations
    demonstrate_lab_interpolation()
    demonstrate_colorblind_safety()
    demonstrate_expression_validation()
    demonstrate_colorbar_generation()
    demonstrate_bio_validation()
    demonstrate_complete_workflow()
    
    print("\nAll demonstrations completed!") 