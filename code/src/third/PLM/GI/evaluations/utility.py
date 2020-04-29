# encoding=utf-8
from collections import OrderedDict
from operator import itemgetter
from random import random

import numpy as np
from sklearn.preprocessing import normalize

from GI.models.base import Dataset, UniformGridDataset, Trajectory
from GI.models.tools import ArrayConverter, Spatial


def f(u):
    return u.trajectory.diameter()


class CellVisitFrequency:
    """
    Calculate the frequencies of visit cells of a dataset.
    """

    @staticmethod
    def evaluate(dataset: Dataset, cells: tuple) -> np.ndarray:
        """
        Calculate the visit frequency of cells.
        :param dataset: Dataset, a dataset
        :param cells: tuple, a tuple of cells
        :return: np.ndarray, frequency distribution
        """

        assert isinstance(dataset, Dataset) and isinstance(cells, tuple)

        cell_frequency = {cell: 0 for cell in cells}

        cnt_checkin = 0
        for user in dataset.users:
            cnt_checkin += len(user.trajectory.checkins)
            for checkin in user.trajectory.checkins:
                for cell in cells:
                    if cell.contains(checkin.location):
                        cell_frequency[cell] += 1
                        break

        # transform frequency counts to frequencies
        for cell in cell_frequency.keys():
            cell_frequency[cell] /= cnt_checkin

        return ArrayConverter.dict2ndarray(cell_frequency, cells)


class CategoryVisitFrequency:
    """
    Calculate the frequencies of visit location categories of a dataset.
    """

    @staticmethod
    def evaluate(dataset: Dataset, categories: tuple) -> np.ndarray:
        """
        Calculate the frequencies of venue categories at the specified category level in the venue categories tree.
        :param dataset: Dataset, a dataset
        :param categories: tuple, a tuple of venue category_ids (strings)
        :return: np.ndarray, category frequency distribution
        """

        assert isinstance(dataset, Dataset) and isinstance(categories, tuple)

        category_frequency = {category: 0 for category in categories}

        cnt_checkin = 0
        for user in dataset.users:
            cnt_checkin += len(user.trajectory.checkins)
            for checkin in user.trajectory.checkins:
                for category in checkin.location.category:
                    if category in category_frequency.keys():
                        category_frequency[category] += 1

        # transform frequency counts to frequencies
        for category in category_frequency.keys():
            category_frequency[category] /= cnt_checkin

        return ArrayConverter.dict2ndarray(category_frequency, categories)


class DiameterDistribution:
    """
    Calculate the diameter distribution of a dataset, where the diameter of a user (trajectory) refer to the
    larges distance of pairwise check-ins in the trajectory of the user.
    """

    @staticmethod
    def evaluate(dataset: Dataset, bins: tuple) -> np.ndarray:
        """
        Calculate the diameter distribution of users.
        :param dataset: Dataset, a dataset
        :param bins: tuple, a tuple of tuples, where each tuple represents an interval [start, end)
        Range of the travel distance is divided into a series of bins (intervals).
        :return: np.ndarray, diameter distribution
        """

        assert isinstance(dataset, Dataset) and isinstance(bins, tuple)

        bin_frequency = {bin_: 0 for bin_ in bins}

        for user in dataset.users:
            diameter = user.trajectory.diameter()
            for bin_ in bin_frequency.keys():
                if bin_[0] <= diameter < bin_[1]:
                    bin_frequency[bin_] += 1
                    break

        # transform counts to frequencies
        for bin_ in bin_frequency.keys():
            bin_frequency[bin_] /= len(dataset.users)

        return ArrayConverter.dict2ndarray(bin_frequency, bins)


class TravelDistanceDistribution:
    """
    Calculate the distribution of travel distance of a dataset, where the travel distance of a user (trajectory)
    refers to the sum of all of pairwise consecutive check-ins in the trajectory of the user.
    """

    @staticmethod
    def evaluate(dataset: Dataset, bins: tuple) -> np.ndarray:
        """
        Calculate the diameter distribution of a dataset.
        :param dataset: Dataset, a dataset
        :param bins: tuple, a tuple of tuples, where each tuple represents an interval [start, end)
        Range of the travel distance is divided into a series of bins (intervals).
        :return: np.ndarray, travel distance distribution
        """

        assert type(dataset) == Dataset and isinstance(bins, tuple)

        bin_frequency = {bin_: 0 for bin_ in bins}

        for user in dataset.users:
            dist = user.trajectory.length()
            for bin_ in bin_frequency.keys():
                if bin_[0] <= dist < bin_[1]:
                    bin_frequency[bin_] += 1
                    break

        # transform counts to frequencies
        for bin_ in bin_frequency.keys():
            bin_frequency[bin_] /= len(dataset.users)

        return ArrayConverter.dict2ndarray(bin_frequency, bins)


class TripDistribution:
    """
    Calculate the distribution of trips of a dataset, where the trip refers to a pair of endpoints of a trajectory,
    and the trip distribution refers to the frequency distribution of trips.
    """

    @staticmethod
    def evaluate(dataset: UniformGridDataset) -> np.ndarray:
        """
        Calculate the trip distribution of a grid dataset.
        :param dataset: UniformGridDataset, a grid dataset
        :return: ndarray: a 2D ndarray with shape (number of cells in the grid x number of cells in the grid)
        """

        assert isinstance(dataset, UniformGridDataset)

        frequencies = np.zeros(shape=(len(dataset.grid.cells), len(dataset.grid.cells)))

        for user in dataset.users:
            startcell_idx = user.trajectory.checkins[0].location.id_
            endcell_idx = user.trajectory.checkins[-1].location.id_
            frequencies[startcell_idx][endcell_idx] += 1

        # transform counts to frequencies
        normalize(frequencies, norm='l1', axis=1, copy=False)

        return frequencies


class CircularQuery:
    """
    A circular query is represented by a circular area, which is specified by a query center position and a radius.
    Given a trajectory, we say that it pass through the query area if any check-in fall in that area,
    or the distance between the query center and the line segment bounded by some two consecutive check-ins is
    less than the radius.
    """

    def __init__(self, center: tuple, radius: float):

        assert isinstance(center, tuple) and isinstance(radius, float)

        self.center = center
        self.radius = radius
        self.sqradius = radius * radius

    def __eq__(self, other):
        return isinstance(other, CircularQuery) and other.center == self.center and other.radius == self.radius

    def is_passed_through_by(self, trajectory: Trajectory) -> bool:
        """
        Check whether the trajectory passed through the circular query area.
        :param trajectory: Trajectory
        :return: bool
        """
        assert isinstance(trajectory, Trajectory)

        # check whether there exists a location that is inside the circle
        for checkin in trajectory.checkins:
            if Spatial.sqeuclidean(self.center, checkin.location.coordinates()) <= self.sqradius:
                return True

        # check whether there exists two consectutive locations that the perpendicular distance
        # from the center to the line bounded by those two locations is not larger than the radius
        for i in range(len(trajectory.checkins) - 1):
            if Spatial.perpendicular(self.center,
                                     trajectory.checkins[i].location.coordinates(),
                                     trajectory.checkins[i + 1].location.coordinates()) <= self.radius:
                return True
        return False

    @staticmethod
    def random_queries(boundary: tuple, num: int) -> tuple:
        """
        Generate some random queries.
        :param boundary: tuple, (x-coordinate of lower left corner, y-..., x-coordiante of upper right corner, y-...)
        :param num: int, number of queries
        :return: tuple, a tuple of queries
        """

        assert isinstance(boundary, tuple), 'Tuple expected; found %s.' % str(type(boundary))
        assert isinstance(num, int), 'Int expected; found %s.' % str(type(num))

        length = boundary[2] - boundary[0]
        width = boundary[3] - boundary[1]
        longer_side = length if length > width else width

        # select center positions randomly
        queries = []
        for i in range(num):
            center_x = random() * length + boundary[0]
            center_y = random() * width + boundary[1]
            radius = longer_side / 3.0  # an empirical value, following the 2019 CCS paper
            queries.append(CircularQuery(center=(center_x, center_y), radius=radius))
        return tuple(queries)


class FrequentTravelPattern:
    """
    Frequent travel pattern of mobile users, represented by an ordered sequence of locations (or cells).
    """

    @staticmethod
    def from_dataset(dataset: Dataset, min_len: int, max_len: int, sort_needed: bool = True) -> OrderedDict:
        """
        Mine frequent travel patterns in a dataset.
        :param dataset: Dataset
        :param min_len: int, minimum length of the pattern
        :param max_len: int, maximum length of the pattern
        :param sort_needed: bool, True means sorting patterns by frequencies in descending order.
        :return: OrderedDict, patterns with frequencies
        """
        assert isinstance(dataset, Dataset)
        assert isinstance(min_len, int) and isinstance(max_len, int) and 2 <= min_len <= max_len

        pattern_surpport = {}  # some patterns and their supports
        for i in range(min_len, max_len + 1):
            for user in dataset.users:
                for j in range(len(user.trajectory.checkins) - i + 1):
                    pattern = tuple(checkin.location for checkin in user.trajectory.checkins[j:(j + i)])
                    if pattern not in pattern_surpport.keys():
                        pattern_surpport[pattern] = 0
                    else:
                        pattern_surpport[pattern] += 1
        pattern_surpport = [(k, v) for k, v in pattern_surpport.items()]

        if sort_needed:  # sort patterns by surpport in descending order
            return OrderedDict(sorted(pattern_surpport, key=itemgetter(1), reverse=True))
        else:
            return OrderedDict(pattern_surpport)
