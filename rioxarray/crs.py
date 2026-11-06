"""
This module contains helper methods for rasterio.crs.CRS.
"""

from typing import Any

import rasterio.crs
from pyproj import CRS
from rasterio.errors import CRSError


def crs_from_user_input(crs_input: Any) -> rasterio.crs.CRS:
    """
    Return a rasterio.crs.CRS from user input.

    This is to deal with change in rasterio.crs.CRS
    as well as to assist in the transition between GDAL 2/3.

    Parameters
    ----------
    crs_input: Any
        Input to create a CRS.

    Returns
    -------
    rasterio.crs.CRS

    """
    if isinstance(crs_input, rasterio.crs.CRS):
        return crs_input
    try:
        return rasterio.crs.CRS.from_user_input(crs_input)
    except CRSError:
        pass
    # use pyproj for edge cases
    crs = CRS.from_user_input(crs_input)
    return rasterio.crs.CRS.from_wkt(crs.to_wkt())


def get_crs_repr(crs_input: Any) -> str:
    """
    Get CRS representation: 'CRS name | EPSG:code' (if existing)

    Parameters
    ----------
    crs_input: Any
        Input to create a CRS.

    Returns
    -------
    str:

    """
    if crs_input is None:
        return "Undefined"
    else:
        pyproj_crs = CRS(crs_input)
        epsg_auth = pyproj_crs.to_authority(min_confidence=100)
        epsg_repr = f" | {':'.join(epsg_auth)}" if epsg_auth is not None else ""
        return f"{pyproj_crs.name}{epsg_repr}"
