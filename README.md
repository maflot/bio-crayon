# BioCrayon

![BioCrayon Logo](logo.png)
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
git clone https://github.com/yourusername/bio-crayon.git
cd bio-crayon

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests
pytest tests/ -v

# Format code
black bio_crayon/ tests/ examples/

# Lint code
flake8 bio_crayon/ tests/ examples/
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
git clone https://github.com/yourusername/bio-crayon.git
cd bio-crayon
pip install -e .
```

## Examples

### Basic Usage
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
Your Name, 2024
https://github.com/maflot/bio-crayon
```

## Links

- **Documentation**: [Coming soon]
- **PyPI**: [Coming soon]
- **GitHub**: https://github.com/maflot/bio-crayon
- **Issues**: https://github.com/maflot/bio-crayon/issues
- **Discussions**: https://github.com/maflot/bio-crayon/discussions