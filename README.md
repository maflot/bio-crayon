

![BioCrayon Logo](logo_small.png)    

# BioCrayon
![pypi](https://img.shields.io/pypi/v/bio-crayon)

A community-driven Python package for managing biological data colormaps with support for both categorical and continuous color mappings.

## Community-Driven Architecture

BioCrayon follows a community-driven approach with:

- **Core Package**: Stable, well-tested functionality
- **Community Registry**: Domain-specific colormaps contributed by researchers
- **Automated Validation**: GitHub Actions ensure quality and accessibility
- **Scientific Standards**: Peer-reviewed colormaps with proper attribution

## Features

- **Flexible Input Sources**: Load colormaps from JSON files, URLs, or Python dictionaries
- **Two Colormap Types**: Support for both categorical (discrete) and continuous colormaps
- **Robust Validation**: JSON schema validation and color format checking
- **Matplotlib Integration**: Convert colormaps to matplotlib Colormap objects
- **Color Utilities**: Color conversion, interpolation, and distance calculations
- **LAB Color Space Interpolation**: Perceptually uniform color gradients for biological data
- **Colorblind Safety**: Built-in validation and generation of colorblind-safe colormaps
- **Biological Data Validation**: Expression range validation and bio-specific requirements
- **Enhanced Colorbar Support**: Matplotlib colorbar generation with customization
- **Built-in Examples**: Allen Brain Atlas colormaps included

## Contributibng

WARNING: This is a work in progress. There might be changes in the colormap schema and the package will be updated accordingly, as well as in the folder structure.

BioCrayon welcomes community contributions! We follow a structured approach to ensure quality and scientific accuracy.

### Contributing Colormaps

1. **Choose a category** that fits your colormap:
   - `neuroscience/` - Brain and nervous system
   - `cell_biology/` - Cellular and molecular biology
   - `genomics/` - Gene expression and sequencing
   - `ecology/` - Biodiversity and environmental
   - `imaging/` - Medical imaging and pathology
   - `allen_immune/` - Immune cell types

2. **Create your colormap** following the JSON schema requirements:
   - **Community colormaps**: Must include metadata with `name` and `version`
   - **User colormaps**: Metadata is optional
   - Include scientific justification (paper reference, DOI)
   - Test colorblind accessibility

3. **Submit a pull request** with:
   - Your colormap JSON file
   - Scientific justification
   - Example usage
   - Accessibility testing results

### Quality Standards

- ✅ Valid JSON schema
- ✅ Scientific justification included
- ✅ Colorblind accessibility tested
- ✅ Example usage provided
- ✅ Metadata requirements met (for community colormaps)

### Development Setup

```bash
# Clone the repository
git clone https://github.com/maflot/bio-crayon.git
cd bio-crayon

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/ -v

# Format code (recommended)
black bio_crayon/ tests/ examples/

# Lint code (recommended)
flake8 bio_crayon/ tests/ examples/
```

## Code Quality (Recommended)

While not required for tests to pass, we recommend maintaining code quality:

### Code Formatting
```bash
# Format code with black
black bio_crayon/ tests/ examples/

# Check formatting without changing files
black --check bio_crayon/ tests/ examples/
```

### Linting
```bash
# Run flake8 for style and error checking
flake8 bio_crayon/ tests/ examples/

# Run mypy for type checking
mypy bio_crayon/ --ignore-missing-imports
```

### Import Sorting
```bash
# Sort imports with isort
isort bio_crayon/ tests/ examples/
```

## Testing

BioCrayon includes comprehensive testing:

### Unit Tests
```bash
pytest tests/ -v
```

### Integration Tests
```bash
python examples/minimal_colormap_example.py
python test_allen_brain_colormaps.py
python test_allen_immune_colormaps.py
```

### GitHub Actions
- **Test Package**: Multi-platform testing across Python 3.8-3.11
- **Test Core**: Essential functionality testing
- **Validate Colormaps**: Community colormap validation

## Installation

### From PyPI
COMING SOON
```bash
pip install bio-crayon
```
FOR NOW:
### From Source
```bash
git clone https://github.com/maflot/bio-crayon.git
cd bio-crayon
pip install -e .
```

## Examples

### Basic Usage using getters
```python
from bio_crayon import BioCrayon

# Load community colormaps
bc = BioCrayon.from_community("allen_immune", "single_cell")

# Get colors
color = bc.get_color("immune_cell_l1", "T cell")
print(color)  # "#5480A3"

# Convert to matplotlib
cmap = bc.to_matplotlib("immune_expression")
```

### Community Colormaps: List, Load, and Plot
```python
import bio_crayon as bc
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# List all available community colormaps by category
print("Available community colormaps:")
community = bc.BioCrayon.list_community_colormaps()
for category, colormaps in community.items():
    print(f"  {category}: {colormaps}")

# Load a specific community colormap (e.g., Allen Brain single cell)
allen_bc = bc.BioCrayon.from_community("allen_brain", "single_cell")
print("\nLoaded colormaps in 'allen_brain/single_cell':")
print(allen_bc.list_colormaps())

# Access a specific colormap and print its categories (if categorical)
colormap_name = allen_bc.list_colormaps()[0]
colormap = allen_bc.get_colormap(colormap_name)
if colormap["type"] == "categorical":
    print(f"\nCategories in '{colormap_name}':")
    categories = list(colormap["colors"].keys())
    print(categories)

    # Convert hex colors to RGB for plotting
    colors = [mcolors.to_rgb(colormap["colors"][cat]) for cat in categories]
    color_array = [colors]

    fig, ax = plt.subplots(figsize=(max(6, len(categories)), 1))
    ax.imshow(color_array, aspect="auto")
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, rotation=45, ha="right", fontsize=8)
    ax.set_yticks([])
    ax.set_title(f"Colormap: {colormap_name}")
    plt.tight_layout()
    plt.show()
else:
    print(f"\n'{colormap_name}' is a continuous colormap.")
    cmap = allen_bc.to_matplotlib(colormap_name)
    fig, ax = plt.subplots(figsize=(8, 1))
    gradient = [list(range(256))]
    ax.imshow(gradient, aspect="auto", cmap=cmap)
    ax.set_axis_off()
    ax.set_title(f"Colormap: {colormap_name}")
    plt.show()
```

### User Colormaps
```python
# Create simple user colormap (no metadata required)
user_data = {
    "colormaps": {
        "my_colors": {
            "type": "categorical",
            "colors": {"red": "#FF0000", "green": "#00FF00"}
        }
    }
}

bc = BioCrayon(user_data)
color = bc.get_color("my_colors", "red")
```

### Basic Usage using bracket notation
```python
from bio_crayon import BioCrayon

# Load community colormaps
bc = BioCrayon.from_community("allen_immune", "single_cell")

bc["subclass_name"]["Astrocyte"]
```
### Locally stored colormaps
```python 
from bio_crayon import BioCrayon

# Load your colormap
bc = BioCrayon("/path/to/rosmap_compass.json", require_metadata=True)

# Intuitive bracket access
bc["sex"]["M"]           # Get color for male: "#4B7837"
bc["sex"]["F"]           # Get color for female: "#983A94"
bc["study"]["Fujita 2024"]  # Get color for study: "#A4DBD2"

# Dictionary-like methods
bc["sex"].keys()         # Get all categories: ['M', 'F', 'Male', 'Female', '0', '1']
bc["sex"].values()       # Get all colors: ['#4B7837', '#983A94', ...]
bc["sex"].items()        # Get category-color pairs
bc["sex"].get("M")      # Get with default: "#4B7837"
bc["sex"].get("X", "#000000")  # Get with custom default: "#000000"

# Check if category exists
"M" in bc["sex"]        # True
"X" in bc["sex"]        # False

# Get info about the colormap
print(bc["sex"])        
```

### Community Colormaps
```python
# Community colormaps require metadata
community_data = {
    "metadata": {
        "name": "My Research Colormaps",
        "version": "1.0",
        "description": "Colormaps for my research",
        "author": "Your Name",
        "doi": "10.1000/example.doi"
    },
    "colormaps": {
        "my_colors": {
            "type": "categorical",
            "colors": {"red": "#FF0000", "green": "#00FF00"}
        }
    }
}

bc = BioCrayon(community_data, require_metadata=True)

# get full color map
bc.get_colormap("my_colors")

# get color for a specific key
bc.get_color("my_colors", "red")

# get colorblind safe colormap
```

### Plotting with pandas
```python
import pandas as pd
import bio_crayon

# Load colormap
bc = bio_crayon.BioCrayon.from_community("allen_immune", "single_cell")

# Create DataFrame with color values
df = pd.DataFrame(bc["subclass_name"].items(), columns=["Subclass", "Color"])

# Plot using matplotlib
plt.figure(figsize=(10, 6))
sns.barplot(x="Subclass", y="Color", data=df, palette="viridis")
plt.xticks(rotation=45)
plt.show()
```

**Complete Example**: See `examples/pandas_plotting_example.py` for a full example with artificial data and multiple histogram visualizations.
First setup fresh environment:
```bash
#!/bin/bash
# Simple BioCrayon Setup

echo "🎨 Setting up BioCrayon..."

# Create environment
conda create -n bio-crayon python=3.10 -y
conda activate bio-crayon

# Install packages
conda install matplotlib numpy -y
pip install bio-crayon

# Test
python -c "
import matplotlib.pyplot as plt
import bio_crayon
print('✅ Setup complete!')
"

echo "Done! Run: conda activate bio-crayon"
```

### Plotting with seaborn
```python
import seaborn as sns
import bio_crayon

# Load colormap
bc = bio_crayon.BioCrayon.from_community("allen_immune", "single_cell")

# Plot using seaborn
sns.palplot(bc["subclass_name"])
```

**Complete Example**: See `examples/seaborn_plotting_example.py` for a full example with artificial data, histograms, box plots, and advanced seaborn visualizations.

### Plotting with matplotlib
```python
import matplotlib.pyplot as plt
import bio_crayon

# Load colormap
bc = bio_crayon.BioCrayon.from_community("allen_immune", "single_cell")

# Use colors in matplotlib plots
colors = bc["subclass_name"]
```

**Complete Example**: See `examples/matplotlib_plotting_example.py` for a full example with artificial data, histograms, box plots, and advanced matplotlib visualizations.

## Architecture

### Core Components
- **`bio_crayon/core.py`**: Main BioCrayon class
- **`bio_crayon/utils.py`**: Color utilities and interpolation
- **`bio_crayon/validators.py`**: Validation logic
- **`schemas/colormap_schema.json`**: JSON schema definition

### Community Structure
```
community_colormaps/
├── allen_immune/          # Immune cell colormaps
├── neuroscience/          # Brain and nervous system
├── cell_biology/          # Cellular biology
├── genomics/              # Gene expression
├── ecology/               # Biodiversity
└── imaging/               # Medical imaging
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Allen Institute for Brain Science**: Brain atlas colormaps
- **Allen Institute for Immunology**: Immune cell colormaps, Claire E. Gustafson (ORCiD 0000-0002-1437-6709) and [Heidi Gustafson](https://earlyfutures.com/) for the single cell colormaps
- **Community Contributors**: Scientific colormap collections

## Citation

If you use BioCrayon in your research, please cite:

```
BioCrayon: A Python package for managing biological data colormaps
Matthias Flotho, 2025
https://github.com/maflot/bio-crayon
```

## Links

- **Documentation**: [Coming soon]
- **PyPI**: [Coming soon]
- **GitHub**: https://github.com/maflot/bio-crayon
- **Issues**: https://github.com/maflot/bio-crayon/issues
- **Discussions**: https://github.com/maflot/bio-crayon/discussions