# encoding=utf-8
from typing import Union

import numpy as np
from jenkspy import jenks_breaks
from math import atan, degrees, exp, log, pi, radians, tan, sqrt


class ArrayConverter:
    @staticmethod
    def dict2list(d, ordered_keys: tuple) -> list:
        """
        Return the list of values in a dict following the given order of the keys.
        :param d: dict
        :param ordered_keys: tuple, ordered keys
        :return: list
        """

        assert isinstance(d, dict) and isinstance(ordered_keys, tuple) and set(ordered_keys).issubset(d.keys())

        return [d[key] for key in ordered_keys]

    @staticmethod
    def dict2ndarray(d, ordered_keys: tuple) -> np.ndarray:
        """
        Return the ndarray of values in a dict following the given order of keys.
        :param d: dict
        :param ordered_keys: tuple, ordered keys
        :return: ndarray
        """

        assert isinstance(d, dict) and isinstance(ordered_keys, tuple) and set(ordered_keys).issubset(d.keys())

        return np.asarray(ArrayConverter.dict2list(d, ordered_keys))

    @staticmethod
    def jenks_breaks(values: tuple, num_interval: int) -> tuple:
        """
        Divide a tuple of values into some intervals by Jenks Natual Breaks algorithm.
        :param values: tuple, a tuple of values
        :param num_interval: int, number of intervals
        :return: tuple, a tuple of tuples, where each tuple represents an interval
        """

        assert isinstance(values, tuple)
        assert isinstance(num_interval, int)

        breaks = jenks_breaks(values=values, nb_class=num_interval)

        # extend the right endpoint by adding 1.0 to make each bin to be a left-closed and right-open interval
        return tuple([(breaks[i], breaks[i + 1]) for i in range(len(breaks) - 2)] + [(breaks[-2], breaks[-1] + 1.0)])


class CoordinatesConverter:
    """
    A converter between geographic coordinates and Cartesian coordinates.
    Refer to: https://wiki.openstreetmap.org/wiki/Mercator#C
    """
    EARTH_RADIUS = 6378137  # equatorial radius of the earth in meters

    @staticmethod
    def cartesian2geographic(position: Union[tuple, list]) -> tuple:
        """
        Convert from Cartesian coordinates to geographic coordinates.
        :param position: Union[tuple, list], (x-coordinate, y-coordinate).
        The coordinates are in something close to meters along the equator.
        :return: tuple, geographic coordinates of the location, (longitude, latitude)
        """

        assert isinstance(position, (tuple, list)) and len(position) == 2

        return (degrees(position[0] / CoordinatesConverter.EARTH_RADIUS),
                degrees(2 * atan(exp(position[1] / CoordinatesConverter.EARTH_RADIUS)) - pi / 2))

    @staticmethod
    def geographic2cartesian(position: Union[tuple, list]) -> tuple:
        """
        Convert from geographic coordinates to Cartesian coordinates.
        :param position, Union[tuple, list], (longitude, latitude)
        :return: tuple, Cartesian coordinates of the location, (x, y)
        The coordinates are in something close to meters along the equator.
        """

        assert isinstance(position, (tuple, list)) and len(position) == 2

        return (CoordinatesConverter.EARTH_RADIUS * radians(position[0]),
                CoordinatesConverter.EARTH_RADIUS * log(tan(pi / 4 + radians(position[1]) / 2)))

    @staticmethod
    def to_cartesian_boundary(geo_boundary: tuple) -> tuple:
        """
        Convert the boundary represented by geographic coordinates to that by Cartesian coordinates.
        :param geo_boundary: tuple,(longitude of lower left corner, lat..., longitude of upper right corner, lat...)
        :return: tuple, a boundary represented by Cartesian coordinates
        """

        assert isinstance(geo_boundary, tuple) and len(geo_boundary) == 4

        return (*CoordinatesConverter.geographic2cartesian(geo_boundary[:2]),
                *CoordinatesConverter.geographic2cartesian(geo_boundary[2:]))


class Spatial:
    """
    Spatial distance calculator.
    """

    @staticmethod
    def euclidean(position1: tuple, position2: tuple) -> float:
        """
        Calculate the Euclidean distance between two positions.
        :param position1: tuple, coordinates of one position
        :param position2: tuple, coordinates of another position
        :return: float, distance
        """

        return sqrt(Spatial.sqeuclidean(position1, position2))

    @staticmethod
    def inside(boundary: tuple, position: tuple):
        """
        Checkin whether a position is inside a rectangular area with a specified boundary.
        :param boundary: tuple, a rectangular area, (min x-coordinate, min y-..., max x-coordinate, max y-...)
        :param position: tuple, a 2D position, (x-coordinate, y-coordinate)
        :return: bool, True indicates that the position is inside the area while False not
        """

        assert isinstance(boundary, tuple) and len(boundary) == 4
        assert isinstance(position, tuple) and len(position) == 2

        return boundary[0] <= position[0] <= boundary[1] and boundary[2] <= position[1] <= boundary[3]

    @staticmethod
    def sqeuclidean(position1: tuple, position2: tuple) -> float:
        """
        Calculate the Euclidean distance between two positions.
        :param position1: tuple, coordinates of one position
        :param position2: tuple, coordinates of another position
        :return: float, distance
        """

        assert isinstance(position1, tuple)
        assert isinstance(position2, tuple)
        assert len(position1) == len(position2)

        return sum((coordinate1 - coordinate2) ** 2 for coordinate1, coordinate2 in zip(position1, position2))

    @staticmethod
    def perpendicular(position1: tuple, position2: tuple, position3: tuple) -> float:
        """
        Calculate the perpendicular distance from position1 to the line bounded by position2 and position3.
        :param position1: tuple, a 2D position
        :param position2: tuple, a 2D position
        :param position3: tuple, a 2D position
        :return: float, distance
        """

        assert isinstance(position1, tuple) and len(position1) == 2
        assert isinstance(position2, tuple) and len(position2) == 2
        assert isinstance(position3, tuple) and len(position3) == 2

        a = (position2[0] - position1[0], position2[1] - position1[0])
        b = (position3[0] - position2[0], position3[1] - position2[0])
        cross_product_norm = abs(a[0] * b[1] - a[1] * b[0])  # norm of "a X b"
        return cross_product_norm / sqrt(b[0] ** 2 + b[1] ** 2)
