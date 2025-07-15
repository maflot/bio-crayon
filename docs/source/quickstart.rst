Quick Start
===========

Basic Usage
-----------

.. code-block:: python

   import bio_crayon

   # Load a colormap
   colormap = bio_crayon.load_colormap('allen_brain')
   
   # Apply to your data
   colored_data = bio_crayon.apply_colormap(data, colormap)

Loading Custom Colormaps
-------------------------

.. code-block:: python

   # Load from community colormaps
   colormap = bio_crayon.load_colormap('cell_biology/fluorescent_proteins')
   
   # Load custom colormap
   colormap = bio_crayon.load_custom_colormap('path/to/your/colormap.json')

Integration with Plotting Libraries
------------------------------------

matplotlib
~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   import bio_crayon

   colormap = bio_crayon.get_matplotlib_colormap('allen_brain')
   plt.scatter(x, y, c=values, cmap=colormap)

seaborn
~~~~~~~

.. code-block:: python

   import seaborn as sns
   import bio_crayon

   colors = bio_crayon.get_seaborn_palette('cell_biology/organelles')
   sns.scatterplot(data=df, x='x', y='y', hue='category', palette=colors)
