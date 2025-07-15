import pandas as pd
import matplotlib.pyplot as plt
import bio_crayon as bc

print("\n7. Visualization example:")
print("-" * 40)

# Create sample data with missing values
data = {
    'cell_type': ['Neuron', 'Astrocyte', 'Endothelial', 'Fibroblast', 'Microglia', None, 'nan'],
    'count': [100, 80, 60, 40, 30, 20, 10]
}

# Convert to proper format for pandas
cell_types = []
counts = []
for ct, count in zip(data['cell_type'], data['count']):
    cell_types.append(str(ct) if ct is not None else 'None')
    counts.append(count)

df = pd.DataFrame({
    'cell_type': cell_types,
    'count': counts
})

# Get colors with fill_missing enabled
colors = []
for cell_type in df['cell_type']:
    # Convert back to original format for color lookup
    lookup_type = None if cell_type == 'None' else cell_type
    color = bc.get_color("cell_types", lookup_type, fill_missing=True)
    colors.append(color)

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Bar plot
bars = ax1.bar(range(len(df)), df['count'], color=colors)
ax1.set_title('Cell Type Counts (with missing value handling)')
ax1.set_xlabel('Cell Type')
ax1.set_ylabel('Count')
ax1.set_xticks(range(len(df)))
ax1.set_xticklabels(df['cell_type'], rotation=45)

# Add color legend
for i, (cell_type, color) in enumerate(zip(df['cell_type'], colors)):
    ax1.text(i, df['count'].iloc[i] + 2, color, ha='center', va='bottom', 
            fontsize=8, rotation=90)

# Pie chart
labels = df['cell_type'].tolist()
ax2.pie(df['count'], labels=labels, colors=colors, autopct='%1.1f%%')
ax2.set_title('Cell Type Distribution')

plt.tight_layout()
plt.show()
