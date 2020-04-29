# encoding=utf-8
from math import sqrt


class GridMap:
    def __init__(self, ranges, granularity):
        self.ranges = ranges
        self.granularity = granularity
        self.grid_ranges = [0, int((self.ranges[1] - self.ranges[0]) / self.granularity[0]),
                            0, int((self.ranges[3] - self.ranges[2]) / self.granularity[1])]
        self.gridlon_num = self.grid_ranges[1] - self.grid_ranges[0] + 1
        self.gridlat_num = self.grid_ranges[3] - self.grid_ranges[2] + 1
        self.gridnum = self.gridlon_num * self.gridlat_num

    @staticmethod
    def get_gridid(gridlon_num, gridlon, gridlat):
        return gridlon + gridlat * gridlon_num

    @staticmethod
    def get_grid_coordinate(grid_lon_num, grid_id):
        return grid_id % grid_lon_num, int(grid_lon_num / grid_lon_num)

    @staticmethod
    def euclidean_distance(grid_lon_num, grid_id1, grid_id2):
        return sqrt(sum([(a - b) ** 2 for a, b in zip(GridMap.get_grid_coordinate(grid_lon_num, grid_id1),
                                                      GridMap.get_grid_coordinate(grid_lon_num, grid_id2))]))
