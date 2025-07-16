# Community Colormaps

This directory contains community-contributed colormaps organized by biological domain.

## Directory Structure

```
community_colormaps/
├── neuroscience/          # Brain and nervous system colormaps
│   ├── allen_brain.json
│   ├── connectome.json
│   └── cajal_blue_brain.json
├── cell_biology/          # Cellular and molecular biology colormaps
│   ├── fluorescent_proteins.json
│   ├── organelles.json
│   └── cell_cycle.json
├── genomics/              # Genomics and sequencing colormaps
│   ├── expression_heatmaps.json
│   ├── quality_scores.json
│   └── variant_effects.json
├── ecology/               # Ecology and environmental colormaps
│   ├── biodiversity.json
│   └── habitat_types.json
└── imaging/               # Medical and imaging colormaps
    ├── he_staining.json
    └── ihc_markers.json
```

## Usage

### Loading Community Colormaps

```python
import bio_crayon

# Load a specific colormap
bc = bio_crayon.BioCrayon.from_community("neuroscience", "allen_brain")

# List available community colormaps
categories = bio_crayon.BioCrayon.list_community_colormaps()
```

### Contributing New Colormaps

1. **Choose the appropriate category** for your colormap
2. **Create a JSON file** following the schema in `CONTRIBUTING.md`
3. **Include scientific justification** (paper reference, DOI)
4. **Test colorblind accessibility** using `BioCrayon.is_colorblind_safe()`
5. **Add example usage** in the `examples/` directory
6. **Submit a pull request** with the filled template

### Validation Requirements

All community colormaps must pass:

- ✅ JSON schema validation
- ✅ Colorblind accessibility check
- ✅ Scientific justification included
- ✅ Example usage provided
- ✅ Preview image generated

## Category Maintainers

- **Neuroscience**: @brain_researcher, @connectome_expert
- **Cell Biology**: @cell_biologist, @microscopy_expert
- **Genomics**: @genomics_researcher, @bioinformatician
- **Ecology**: @ecologist, @biodiversity_expert
- **Imaging**: @imaging_specialist, @pathologist

## Quality Standards

Each colormap should include:

- **Scientific backing**: Paper reference or established standard
- **Accessibility**: Colorblind-safe design
- **Documentation**: Clear use case and description
- **Examples**: Working code examples
- **Validation**: Automated testing compliance

## Getting Help

- Review existing colormaps for examples
- Open an issue for questions about contribution
- Join community discussions for feedback 