from affine import Affine
from numpy.testing import assert_array_equal

from rioxarray._spatial_utils import affine_to_coords


def test_affine_to_coords():
    coords = affine_to_coords(Affine(1.0, 0.0, 0.0, 0.0, -1.0, 2.0), width=3, height=2)
    assert_array_equal(coords["x"], [0.5, 1.5, 2.5])
    assert_array_equal(coords["y"], [1.5, 0.5])


def test_affine_to_coords__rotation():
    coords = affine_to_coords(Affine(1.0, 1.0, 0.0, 0.0, -1.0, 2.0), width=2, height=2)
    assert_array_equal(coords["x"], [[1.0, 2.0], [2.0, 3.0]])
    assert_array_equal(coords["y"], [[1.5, 1.5], [0.5, 0.5]])
