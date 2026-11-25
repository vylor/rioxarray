import numpy
import xarray
from affine import Affine
from rasterio.crs import CRS

from rioxarray import set_options
from rioxarray.enum import Convention


def test_reproject_cf_to_zarr_conventions():
    data = xarray.DataArray(
        numpy.random.rand(10, 10),
        dims=["y", "x"],
        coords={"y": numpy.arange(10), "x": numpy.arange(10)},
    )
    transform = Affine(1.0, 0.0, 0.0, 0.0, -1.0, 10.0)
    data.rio.write_transform(transform, inplace=True, convention=Convention.CF)
    data.rio.write_crs(CRS.from_epsg(4326), inplace=True, convention=Convention.CF)
    assert sorted(data.coords) == ["spatial_ref", "x", "y"]
    assert "grid_mapping" in data.encoding
    with set_options(convention=Convention.ZARR):
        out = data.rio.reproject("EPSG:6933")
        assert out.rio.crs == CRS.from_epsg(6933)
        assert sorted(out.coords) == ["x", "y"]
        assert "grid_mapping" not in out.encoding
        assert {
            "proj:wkt2",
            "spatial:bbox",
            "spatial:dimensions",
            "spatial:registration",
            "spatial:shape",
            "spatial:transform",
            "zarr_conventions",
        } & set(out.attrs)


def test_reproject_zarr_to_cf_conventions():
    data = xarray.DataArray(
        numpy.random.rand(10, 10),
        dims=["y", "x"],
        coords={"y": numpy.arange(10), "x": numpy.arange(10)},
    )
    transform = Affine(1.0, 0.0, 0.0, 0.0, -1.0, 10.0)
    data.rio.write_transform(transform, inplace=True, convention=Convention.ZARR)
    data.rio.write_crs(CRS.from_epsg(4326), inplace=True, convention=Convention.ZARR)
    assert sorted(data.coords) == ["x", "y"]
    assert {
        "proj:wkt2",
        "spatial:bbox",
        "spatial:dimensions",
        "spatial:registration",
        "spatial:shape",
        "spatial:transform",
        "zarr_conventions",
    } & set(data.attrs)
    with set_options(convention=Convention.CF):
        out = data.rio.reproject("EPSG:6933")
        assert out.rio.crs == CRS.from_epsg(6933)
        assert sorted(out.coords) == ["spatial_ref", "x", "y"]
        assert sorted(out.encoding) == ["grid_mapping"]
        assert sorted(out.attrs) == ["_FillValue"]


def test_clip_cf_to_zarr_conventions():
    data = xarray.DataArray(
        numpy.random.rand(10, 10),
        dims=["y", "x"],
        coords={"y": numpy.arange(10), "x": numpy.arange(10)},
    )
    transform = Affine(1.0, 0.0, 0.0, 0.0, -1.0, 10.0)
    data.rio.write_nodata(-1, inplace=True)
    data.rio.write_transform(transform, inplace=True, convention=Convention.CF)
    data.rio.write_crs(CRS.from_epsg(4326), inplace=True, convention=Convention.CF)
    assert sorted(data.coords) == ["spatial_ref", "x", "y"]
    assert "grid_mapping" in data.encoding
    geom = {
        "type": "Polygon",
        "coordinates": [[[5.0, 0.0], [5.0, 5.0], [0.0, 5.0], [0.0, 0.0], [5.0, 0.0]]],
    }
    with set_options(convention=Convention.ZARR):
        out = data.rio.clip([geom], crs="EPSG:4326")
        assert out.rio.crs == CRS.from_epsg(4326)
        assert sorted(out.coords) == ["x", "y"]
        assert out.encoding == {}
        assert {
            "proj:wkt2",
            "spatial:bbox",
            "spatial:dimensions",
            "spatial:registration",
            "spatial:shape",
            "spatial:transform",
            "zarr_conventions",
        } & set(out.attrs)


def test_clip_zarr_to_cf_conventions():
    data = xarray.DataArray(
        numpy.random.rand(10, 10),
        dims=["y", "x"],
        coords={"y": numpy.arange(10), "x": numpy.arange(10)},
    )
    transform = Affine(1.0, 0.0, 0.0, 0.0, -1.0, 10.0)
    data.rio.write_nodata(-1, inplace=True)
    data.rio.write_transform(transform, inplace=True, convention=Convention.ZARR)
    data.rio.write_crs(CRS.from_epsg(4326), inplace=True, convention=Convention.ZARR)
    assert sorted(data.coords) == ["x", "y"]
    assert {
        "proj:wkt2",
        "spatial:bbox",
        "spatial:dimensions",
        "spatial:registration",
        "spatial:shape",
        "spatial:transform",
        "zarr_conventions",
    } & set(data.attrs)
    geom = {
        "type": "Polygon",
        "coordinates": [[[5.0, 0.0], [5.0, 5.0], [0.0, 5.0], [0.0, 0.0], [5.0, 0.0]]],
    }
    with set_options(convention=Convention.CF):
        out = data.rio.clip([geom], crs="EPSG:4326")
        assert out.rio.crs == CRS.from_epsg(4326)
        assert sorted(out.coords) == ["spatial_ref", "x", "y"]
        assert sorted(out.encoding) == ["grid_mapping"]
        assert sorted(out.attrs) == ["_FillValue"]
