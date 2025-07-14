## New Colormap Contribution

**Category**: neuroscience/cell_biology/genomics/ecology/imaging/other
**Colormap Name**: `my_awesome_colormap`
**Type**: categorical/continuous

### Scientific Context
- **Paper/Source**: [DOI or URL] (optional)
- **Use Case**: What biological data this represents
- **Why Needed**: Gap this fills in existing colormaps

### Validation Checklist
- [ ] JSON schema validates
- [ ] Colorblind accessibility checked
- [ ] Example usage provided
- [ ] Preview image generated
- [ ] Scientific justification included
- [ ] Appropriate category folder selected

### Example Usage
```python
bc = BioCrayon.from_community("category", "my_awesome_colormap")
bc.plot_colormap("my_awesome_colormap")
```

### Files Changed
- [ ] `community_colormaps/category/my_awesome_colormap.json`
- [ ] `examples/category_my_awesome_colormap.py` (if applicable)
- [ ] Documentation updates (if applicable)

### Additional Notes
Any additional context, special considerations, or notes for reviewers. 