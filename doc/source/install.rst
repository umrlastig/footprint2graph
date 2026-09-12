:Author: Marie-Dominique Van Damme
:Version: 1.0
:License: --
:Date: 05/06/2026



Installation
=============

**footprint2graph** is supported on Python versions 3.10+.


Dependencies
^^^^^^^^^^^^

**footprint2graph** depends on the following Python packages (installed automatically with the library):

* `tracklib <https://pypi.org/project/tracklib/>`_ : a GPS trajectory processing library used for filtering, resampling, summarization, selection, generalization, map matching and trajectory aggregation.selection, generalization, map matching and trajectory aggregation.
* `matplotlib <https://pypi.org/project/matplotlib/>`_ - Used for colormaps and 2D plotting.
* Shapely <https://pypi.org/project/shapely/>_ : used for centerline extraction and smoothing.
* Fiona <https://pypi.org/project/fiona/>_ and Rasterio <https://pypi.org/project/rasterio/>_ : used to load vector (SHP) and raster (TIF) data.


**GDAL** is also required for the vectorization workflow. It must be installed separately on the system. Installation instructions are available on the GDAL download page <https://gdal.org/en/stable/download.html>_.

The Python package osgeo (including the GDAL, OGR and OSR modules) is used by footprint2graph for vectorization.


Install standard release
^^^^^^^^^^^^^^^^^^^^^^^^^

Users can install footprint2graph from PyPI using the pip package manager (`PyPI <https://pypi.org/project/footprint2graph/>`_). To install the latest stable release, run:


**Sous Ubuntu :**

.. code-block:: bash

   sudo apt install gdal-bin libgdal-dev

   pip install GDAL==$(gdal-config --version)

   pip install footprint2graph






Install as an editable library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Coming soon*

.. Obtain the source code
.. """""""""""""""""""""""







