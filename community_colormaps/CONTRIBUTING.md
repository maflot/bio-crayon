# Contributing Community Colormaps

Thank you for contributing to BioCrayon's community colormaps! This guide will help you create high-quality, scientifically-backed colormaps for biological data visualization.

## Quick Start

1. **Choose a category** for your colormap (neuroscience, cell_biology, genomics, ecology, imaging)
2. **Create a JSON file** following the schema below
3. **Test accessibility** using `BioCrayon.is_colorblind_safe()`
4. **Add scientific justification** (paper reference, DOI)
5. **Create an example** in the `examples/` directory
6. **Submit a pull request**

## JSON Schema

All community colormaps must follow this schema:

```json
{
  "metadata": {
    "name": "Your Colormap Collection Name",
    "version": "1.0.0",
    "description": "Brief description of the colormap collection",
    "author": "Your Name or Organization",
    "source": "URL or reference to the source",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "use_case": "Description of when to use this colormap",
    "accessibility": {
      "colorblind_safe": true,
      "tested_types": ["deuteranopia", "protanopia", "tritanopia"],
      "contrast_ratio": "AA compliant"
    },
    "primary_paper": {
      "doi": "10.xxxx/xxxxx",
      "title": "Paper Title",
      "year": 2023,
      "journal": "Journal Name"
    }
  },
  "colormaps": {
    "your_colormap_name": {
      "type": "categorical",
      "description": "Description of this specific colormap",
      "colors": {
        "category1": "#FF0000",
        "category2": "#00FF00",
        "category3": "#0000FF"
      }
    },
    "your_continuous_colormap": {
      "type": "continuous",
      "description": "Description of continuous colormap",
      "colors": ["#000000", "#FFFFFF"],
      "positions": [0.0, 1.0],
      "interpolation": "linear"
    }
  }
}
```

## Required Metadata Fields

### Required for Community Colormaps
- `name`: Collection name
- `version`: Semantic versioning (e.g., "1.0.0")
- `description`: Clear description of the collection
- `author`: Author or organization
- `source`: URL or reference to the source
- `keywords`: Array of relevant keywords
- `use_case`: When to use this colormap
- `accessibility.colorblind_safe`: Boolean indicating colorblind safety
- `primary_paper`: Scientific backing (DOI, title, year, journal)

### Optional Metadata Fields
- `palette_credits`: Designer credits
- `atlas_citation`: Atlas-specific citation
- `data_source`: Specific dataset source
- `taxonomic_levels`: Hierarchy levels if applicable
- `license`: License information
- `created`: Creation date (ISO format)

## Colormap Types

### Categorical Colormaps
For discrete categories (e.g., cell types, species):

```json
{
  "type": "categorical",
  "description": "Description of the categories",
  "colors": {
    "category1": "#FF0000",
    "category2": "#00FF00"
  }
}
```

### Continuous Colormaps
For continuous data (e.g., expression levels, time series):

```json
{
  "type": "continuous",
  "description": "Description of the continuous scale",
  "colors": ["#000000", "#FFFFFF"],
  "positions": [0.0, 1.0],
  "interpolation": "linear"
}
```

## Validation Requirements

### 1. JSON Schema Validation
Your colormap must pass schema validation:

```python
import bio_crayon
from bio_crayon.validators import validate_colormap_schema

# Validate your JSON file
is_valid = validate_colormap_schema("your_colormap.json")
```

### 2. Colorblind Accessibility
Test your colormap for colorblind safety:

```python
import bio_crayon

bc = bio_crayon.BioCrayon.from_file("your_colormap.json")
is_safe = bc.is_colorblind_safe()
print(f"Colorblind safe: {is_safe}")
```

### 3. Scientific Justification
- Include DOI of the primary paper
- Provide clear use case description
- Reference established standards if applicable

### 4. Example Usage
Create an example in the `examples/` directory:

```python
# examples/your_colormap_example.py
import bio_crayon
import matplotlib.pyplot as plt
import numpy as np

# Load your colormap
bc = bio_crayon.BioCrayon.from_community("category", "your_colormap")

# Create example visualization
# ... your example code here
```

## File Naming Convention

- Use descriptive, lowercase names with underscores
- Include the primary data type or source
- Examples: `allen_brain_single_cell.json`, `fluorescent_proteins.json`

## Directory Structure

Place your colormap in the appropriate category:

```
community_colormaps/
├── neuroscience/          # Brain and nervous system
├── cell_biology/          # Cellular and molecular biology
├── genomics/              # Genomics and sequencing
├── ecology/               # Ecology and environmental
└── imaging/               # Medical and imaging
```

## Quality Standards

### Accessibility
- Test for colorblind safety (deuteranopia, protanopia, tritanopia) (recommended)
- Ensure adequate contrast ratios
- Consider grayscale printing

### Documentation
- Clear description of use cases
- Proper categorization
- Relevant keywords

### Examples
- Working code examples
- Realistic data visualization
- Multiple use case demonstrations

## Pull Request Template

When submitting your contribution, include:

```markdown
## Colormap Contribution

### Category
[ ] neuroscience
[ ] cell_biology  
[ ] genomics
[ ] ecology
[ ] imaging

### Scientific Backing
- **Paper**: [Title]
- **DOI**: [DOI]
- **Year**: [Year]
- **Journal**: [Journal]

### Accessibility
- [ ] Colorblind safe (tested)
- [ ] Adequate contrast ratios
- [ ] Grayscale compatible

### Files Added
- `community_colormaps/[category]/[filename].json`
- `examples/[filename]_example.py`

### Testing
- [ ] JSON schema validation passes
- [ ] Colorblind accessibility test passes
- [ ] Example code runs successfully
- [ ] Documentation updated
```

## Getting Help

- Review existing colormaps for examples
- Check the [schema documentation](../schemas/colormap_schema.json)
- Open an issue for questions
- Join community discussions

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Follow scientific standards
- Ensure accessibility compliance

Thank you for contributing to the biological visualization community! 