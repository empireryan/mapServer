from __future__ import print_function
from __future__ import division
from past.utils import old_div
import time
import functools
import math

from geopy.distance import vincenty

from world.mapping.map import PixelPair, Coordinate, Map


def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))

    return newfunc


from engine.server.server_conf import settings

coordinate_a = Coordinate(lat=36.974117, lon=-122.030796)
coordinate_b = Coordinate(lat=37.411891, lon=-122.052183)

_map = Map(settings['FILE_CONFIG']['filename'])


@timeit
def test_map_instance():
    map = Map(settings['FILE_CONFIG']['filename'])


@timeit
def test_lat_lon_to_pixel():
    print("")
    assert _map.lat_lon_to_pixel(coordinate_a) == PixelPair(x=9719, y=25110)


@timeit
def test_pixel_to_lat_lon():
    # print map.pixel_to_lat_lon(PixelPair(0, 0))
    pass


@timeit
def test_distance_on_unit_sphere():
    assert (_map.distance_on_unit_sphere(coordinate_a, coordinate_b, mode='km') - 48.622 < .05 * 48.622)


@timeit
def test_vinc_dist():
    assert (old_div(_map.vinc_inv(_map.flattening, _map.semimajor, coordinate_a, coordinate_b)["distance"], 1000) -
            vincenty((36.974117, -122.030796), (37.411891, -122.052183)).kilometers <= 1e-6)


@timeit
def test_vinc_pt():
    assert (_map.vinc_dir(_map.flattening, _map.semimajor, coordinate_a, math.degrees(6.24423422267), 48621.8048816) ==
            coordinate_b, math.degrees(3.10241592286))


@timeit
def test_map_process():
    # test create instance

    # test starting sub-processes

    pass
