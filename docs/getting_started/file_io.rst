.. _file_io:

File I/O
========

This page covers reading and writing raster files with rioxarray. For the basics of
opening files, see :ref:`getting_started`.

Reading Files
-------------

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

    with rioxarray.open_rasterio("my.tif") as xds:
        xds.rio.to_raster("out.tif")
        xds.rio.to_raster("out_deflate.tif", compress="DEFLATE")

Cloud Optimized GeoTIFF (COG)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To write a COG, use GDAL's ``COG`` driver:

.. code-block:: python

    import rioxarray

    with rioxarray.open_rasterio("my.tif") as xds:
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
    import rioxarray

    with rioxarray.open_rasterio("my.tif") as xds:
        with rasterio.Env(CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE="YES"):
            xds.rio.to_raster("/vsis3/bucket/out.tif", driver="COG")

Alternatively, ``rio.to_raster`` accepts a file-like object, such as an ``io.BytesIO``
buffer or a file opened with `fsspec <https://filesystem-spec.readthedocs.io>`__
(writing to ``s3://`` with fsspec requires `s3fs <https://s3fs.readthedocs.io>`__).
The ``driver`` must be set explicitly because it cannot be detected from a file extension.

.. code-block:: python

    import fsspec
    import rioxarray

    with rioxarray.open_rasterio("my.tif") as xds:
        with fsspec.open("s3://bucket/out.tif", "wb") as fobj:
            xds.rio.to_raster(fobj, driver="COG")
