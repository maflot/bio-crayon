Contributing
============

We welcome contributions to bio-crayon!

Development Setup
-----------------

1. Fork the repository
2. Clone your fork:

.. code-block:: bash

   git clone https://github.com/yourusername/bio-crayon.git
   cd bio-crayon

3. Install in development mode:

.. code-block:: bash

   pip install -e ".[dev]"

Running Tests
-------------

.. code-block:: bash

   pytest tests/

Code Style
----------

We use black for code formatting:

.. code-block:: bash

   black bio_crayon/ tests/

Adding Colormaps
----------------

Community colormaps are stored in the `community_colormaps/` directory. 
To add a new colormap:

1. Create a JSON file following the schema in `schemas/colormap_schema.json`
2. Place it in the appropriate category folder
3. Add tests in `tests/`
4. Update documentation
