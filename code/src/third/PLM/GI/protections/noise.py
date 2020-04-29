# encoding=utf-8
from math import asin, atan2, cos, degrees, e, exp, log, pi, radians, sin
from random import random


class PlanarLaplace:
    """
    2-dimensional (planar) Laplacian mechanism.
    Refer to https://github.com/chatziko/location-guard/blob/master/src/js/laplace.js
    """

    @staticmethod
    def lambertw(x):
        """
        Lambert W function on branch -1.
        Refer to http://en.wikipedia.org/wiki/Lambert_W_function
        and https://github.com/chatziko/location-guard/blob/master/src/js/laplace.js#L45
        :return:
        """

        min_diff = 1e-10
        if x == -1 / e:
            return -1
        elif -1 / e < x < 0:
            q = log(-x)
            p = 1
            while abs(p - q) > min_diff:
                p = (q * q + x / exp(q)) / (q + 1)
                q = (p * p + x / exp(p)) / (p + 1)
            return round(1000000 * q) / 1000000
        else:
            return 0

    @staticmethod
    def inverse_cumulative_gamma(epsilon, z):
        """
        Inverse cumulative polar laplacian distribution function.
        Refer to https://github.com/chatziko/location-guard/blob/master/src/js/laplace.js#L70
        :param epsilon: float, privacy budget
        :param z: float, unknown purpose
        :return: float
        """

        return -(PlanarLaplace.lambertw((z - 1) / e) + 1) / epsilon

    @staticmethod
    def add_vector_to_pos(lonlat, distance, angle):
        """
        Calculate distance, bearing and more between geographic positions.
        Refer to http://www.movable-type.co.uk/scripts/latlong.html
        and https://github.com/chatziko/location-guard/blob/master/src/js/laplace.js#L117
        :param lonlat: tuple, (longitude, latitude)
        :param angle: float, unknown purpose
        :param distance: float, unknown purpose
        :param angle: float, unknown purpose
        :return: tuple, geographic coordinates of a position, (longitude, latitude)
        """

        ang_dist = distance / 6378137
        lon1, lat1 = radians(lonlat[0]), radians(lonlat[1])
        lat2 = asin(sin(lat1) * cos(ang_dist) + cos(lat1) * sin(ang_dist) * cos(angle))
        lon2 = lon1 + atan2(sin(angle) * sin(ang_dist) * cos(lat1), cos(ang_dist) - sin(lat1) * sin(lat2))
        lon2 = (lon2 + 3 * pi) % (2 * pi) - pi
        return degrees(lon2), degrees(lat2)

    @staticmethod
    def perturbate(lonlat, epsilon):
        """
        Generate the noised position given an actual position.
        Refer to https://github.com/chatziko/location-guard/blob/master/src/js/laplace.js#L90
        :param lonlat: tuple, geographic coordinates of the actual position, (longitude, latitude)
        :param epsilon: float, privacy budget
        :return: tuple, geographic coordinates of the noised position, (longitude, latitude)
        """

        theta = random() * pi * 2
        z = random()
        r = PlanarLaplace.inverse_cumulative_gamma(epsilon, z)
        return PlanarLaplace.add_vector_to_pos(lonlat, r, theta)

    @staticmethod
    def perturbate_cartesian(xy, epsilon):
        """
        Generate the noised position given an actual Cartesian position.
        Refer to https://github.com/chatziko/location-guard/blob/master/src/js/laplace.js#L100
        :param xy: tuple, Cartesian coordinates of the actual position, (x-coordinate, y-coordinate)
        :param epsilon: float, privacy budget
        :return: tuple, Cartesian coordinates of the noised position, (x-coordinate, y-coordinate)
        """

        theta = random() * pi * 2
        z = random()
        r = PlanarLaplace.inverse_cumulative_gamma(epsilon, z)
        return xy[0] + r * cos(theta), xy[1] + r * sin(theta)
