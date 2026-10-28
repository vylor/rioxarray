.. _getting_started:

Getting Started
================

Welcome! This page aims to help you gain a foundational understanding of rioxarray.

rio accessor
-------------

rioxarray `extends xarray <https://docs.xarray.dev/en/stable/internals/extending-xarray.html>`__
with the `rio` accessor. The `rio` accessor is activated by importing rioxarray like so:

.. code-block:: python

    import rioxarray


You can learn how to `clip`, `merge`, and `reproject` rasters in the :ref:`usage_examples`
section of the documentation. Need to export to a raster (GeoTiff)? There is an example for
that as well.


Reading Files
-------------

xarray
~~~~~~~

Since `rioxarray` is an extension of `xarray`, you can load in files using the standard
`xarray` open methods. If you use one of xarray's open methods such as ``xarray.open_dataset``
to load netCDF files with the default engine, it is recommended to use `decode_coords="all"`.
This will load the grid mapping variable into coordinates for compatibility with rioxarray.

.. code-block:: python

    import xarray

    xds = xarray.open_dataset("file.nc", decode_coords="all")


rioxarray
~~~~~~~~~~

rioxarray 0.4+ enables passing `engine="rasterio"` to ``xarray.open_dataset``
and ``xarray.open_mfdataset`` for xarray 0.18+. This uses
:func:`rioxarray.open_rasterio` as the backend and always returns an ``xarray.Dataset``.

.. code-block:: python

    import xarray

    xds = xarray.open_dataset("my.tif", engine="rasterio")

You can also use :func:`rioxarray.open_rasterio`. This objects returned depend on
your input file type.

.. code-block:: python

    import rioxarray

    xds = rioxarray.open_rasterio("my.tif")


Why use :func:`rioxarray.open_rasterio` instead of `xarray.open_rasterio`?

1. It supports multidimensional datasets such as netCDF.
2. It stores the CRS as a WKT, which is the recommended format (`PROJ FAQ <https://proj.org/faq.html#what-is-the-best-format-for-describing-coordinate-reference-systems>`__).
3. It loads in the CRS, transform, and nodata metadata in standard CF & GDAL locations.
4. It supports masking and scaling data with the `masked` and `mask_and_scale` kwargs.
5. It adds the coordinate axis CF metadata.
6. It loads raster metadata into the attributes.
7. `xarray.open_rasterio` is deprecated (since v0.20.0)


Cloud storage
~~~~~~~~~~~~~~

Paths are passed through to rasterio/GDAL, so you can also read files directly
from HTTP(S) URLs and cloud storage (e.g. ``s3://``). See :ref:`gdal_env` for
configuring GDAL when working with cloud-stored data.

.. code-block:: python

    import xarray

    xds = xarray.open_dataset("s3://bucket/my.tif", engine="rasterio")


Writing Files
-------------

GeoTIFF
~~~~~~~~

Use ``rio.to_raster`` on an ``xarray.DataArray`` or ``xarray.Dataset`` to write a raster.
The driver is detected from the ``.tif``/``.tiff`` extension. Additional keyword arguments
are passed to rasterio as GDAL creation options.

.. code-block:: python

    import rioxarray

    xds = rioxarray.open_rasterio("my.tif")
    xds.rio.to_raster("out.tif")
    xds.rio.to_raster("out_lzw.tif", compress="LZW")

Cloud Optimized GeoTIFF (COG)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To write a COG, use GDAL's ``COG`` driver:

.. code-block:: python

    xds.rio.to_raster("out_cog.tif", driver="COG")

For more examples, including writing large rasters with ``windowed=True`` or with dask,
see :doc:`../examples/convert_to_raster`, :doc:`../examples/COG`,
and :doc:`../examples/dask_read_write`.

Cloud storage
~~~~~~~~~~~~~~

To write directly to cloud storage, use a
`GDAL virtual file system <https://gdal.org/en/stable/user/virtual_file_systems.html>`__
path such as ``/vsis3/`` (``/vsigs/`` and ``/vsiaz/`` work similarly).
These file systems only support sequential writes, so set
``CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE`` to have GDAL write to a local temporary file
and upload it when the file is closed:

.. code-block:: python

    import rasterio

    with rasterio.Env(CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE="YES"):
        xds.rio.to_raster("/vsis3/bucket/out.tif", driver="COG")

Alternatively, ``rio.to_raster`` accepts a file-like object, such as an ``io.BytesIO``
buffer or a file opened with `fsspec <https://filesystem-spec.readthedocs.io>`__
(writing to ``s3://`` with fsspec requires `s3fs <https://s3fs.readthedocs.io>`__).
The ``driver`` must be set explicitly because it cannot be detected from a file extension.

.. code-block:: python

    import fsspec

    with fsspec.open("s3://bucket/out.tif", "wb") as fobj:
        xds.rio.to_raster(fobj, driver="COG")


Introductory Information
--------------------------

.. toctree::
   :maxdepth: 1

   switching_from_rasterio
   crs_management.ipynb
   nodata_management.ipynb
   manage_information_loss.ipynb
   gdal_env
