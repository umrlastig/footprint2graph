:Author: Marie-Dominique Van Damme
:Version: 1.0
:License: --
:Date: 05/06/2026



Installation
=============

**footprint2graph** is supported on Python versions 3.10+.


Dependencies
^^^^^^^^^^^^

**System dependencies**

* **GDAL** is required for the vectorization workflow and must be installed separately before installing **footprint2graph**. Installation instructions are available on the `GDAL download page <https://gdal.org/en/stable/download.html>`_.

  The Python package `osgeo` (including the GDAL, OGR and OSR modules) is used by **footprint2graph** for vectorization.

**Python dependencies**

* **footprint2graph** depends on the following Python packages, which are installed automatically with the library:

  * `tracklib <https://pypi.org/project/tracklib/>`_ : a GPS trajectory processing library used for filtering, resampling, summarization, selection, generalization, map matching and trajectory aggregation.
  * `matplotlib <https://pypi.org/project/matplotlib/>`_ : used for colormaps and 2D plotting.
  * `Shapely <https://pypi.org/project/shapely/>`_ : used for centerline extraction and smoothing.
  * `Fiona <https://pypi.org/project/fiona/>`_ and `Rasterio <https://pypi.org/project/rasterio/>`_ : used to load vector (SHP) and raster (TIF) data.



Install standard release
^^^^^^^^^^^^^^^^^^^^^^^^^

Users can install footprint2graph from PyPI using the pip package manager (`PyPI <https://pypi.org/project/footprint2graph/>`_). To install the latest stable release, run:


.. code-block:: bash

   pip install footprint2graph






Install as an editable library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Coming soon*

.. Obtain the source code
.. """""""""""""""""""""""







