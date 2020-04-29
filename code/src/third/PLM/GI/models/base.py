# encoding=utf-8
import sqlite3 as sq
from datetime import datetime
from typing import Type
from typing import Union
from pickle import dump, load

from math import sqrt

from GI.models.database import Database
from GI.models.tools import CoordinatesConverter, Spatial


class Location:
    """
    A point in a planar space.
    """

    def __init__(self, x, y, category: tuple = None):
        """
        Initiate a location with given coordinates.
        Note that the coordinates could be geographic coordiantes, Cartesian coordinates or of any other type.
        :param x: float, abscissa of the location
        :param y: float, ordinate of the location
        :param category: tuple, a tuple of venue categories of the location, the length = height of categories tree + 1
        """

        assert (category is None or isinstance(category, tuple))

        self.x, self.y = x, y
        self.category = category  # tuple, https://developer.foursquare.com/docs/resources/categories

    def __eq__(self, other) -> bool:
        """
        Check whether current location is same as the other location. This method returns True if 'other' is a
        location and its coordinates are the same as that of current location.
        :param other: Location, the other location
        :return: bool
        """

        return isinstance(other, Location) and other.x == self.x and other.y == self.y

    def __str__(self) -> str:

        return str(self.x) + ',' + str(self.y)

    def clone(self):
        """
        Return a deep copy of the location.
        :return: Location
        """

        return Location(self.x, self.y, self.category)

    def coordinates(self) -> tuple:
        """
        Return coordinates of the location.
        :return: tuple
        """

        return self.x, self.y

    @staticmethod
    def boundary(locations: list) -> tuple:
        """
        Given a set of locations, this method returns the lower left location and the upper right location.
        :param locations: list, locations
        :return: tuple, a tuple of two locations, (the lower left location, the upper right location)
        """

        assert isinstance(locations, (list, tuple, set)) and len(locations) == 2

        lower_left = locations[0]
        upper_right = locations[0]
        for location in locations:
            if location.x < lower_left.x and location.y < lower_left.y:
                lower_left = location
        for location in locations:
            if location.x > upper_right.x and location.y > upper_right.y:
                upper_right = location
        return lower_left, upper_right


class Cell(Location):
    """
    A cell is a rectangular area and represented by two vertices.
    """

    def __init__(self, ll: Location, ur: Location, coordinates: tuple = None, id_: int = None):
        """
        Initiation of a cell.
        :param ll: Location, the lower left vertice
        :param ur: Location, the upper right vertice
        :param coordinates: tuple, grid cooridnates
        :param id_: int, cell id in a grid
        """

        assert isinstance(ll, Location) and isinstance(ur, Location) and ll.x <= ur.x and ll.y <= ur.y
        assert coordinates is None or isinstance(coordinates, tuple)

        self.ll = ll
        self.ur = ur
        self.id_ = id_

        Location.__init__(self, x=coordinates[0], y=coordinates[1], category=None)

    def __eq__(self, other) -> bool:
        """
        Checkin whether the other cell is same as current cell. This method returns True if vertices of the other cell
        are same as that of current cell.
        :param other: Cell
        :return: bool
        """

        return isinstance(other, Cell) and other.ll == self.ll and other.ur == self.ur

    def __hash__(self) -> int:
        """
        Make the class hashable.
        :return: int
        """

        return hash((self.ll.x, self.ll.y, self.ur.x, self.ur.y))

    def clone(self):
        return Cell(ll=self.ll.clone(), ur=self.ur.clone(), coordinates=self.coordinates(), id_=self.id_)

    def contains_location(self, location: Location) -> bool:
        """
        Check whether a given location falls in the cell.
        :param location: Location
        :return: bool
        """

        assert isinstance(location, Location)

        return self.ll.x <= location.x <= self.ur.x and self.ll.y <= location.y <= self.ur.y

    def contains_cell(self, cell) -> bool:
        """
        Check whether the given cell falls in the cell.
        :param cell: Cell
        """

        assert isinstance(cell, Cell)

        return cell.ll.x >= self.ll.x and cell.ll.y >= self.ll.y and cell.ur.x <= self.ur.x and cell.ur.y <= self.ur.y

    def contains(self, location) -> bool:
        """
        Check whether a given location falls in the cell. The location can be an instance of Location or Cell.
        :param location: Union[Location, Cell]
        :return: bool, return True if location is a Location and falls in the cell or the location is a Cell and
        equals to this cell; return False otherwise
        """

        assert isinstance(location, (Location, Cell))

        return self.contains_location(location) if type(location) == Location else self.contains_cell(location)


class Checkin:
    """
    Check-in, a record representing that people announce their arrival at a location.
    """

    def __init__(self, location: Union[Location, Cell], time: datetime = None):
        """
        Initiation of a check-in with time and location.
        :param location: Location or Cell
        :param time: None or datetime, optianal
        """

        assert isinstance(location, (Location, Cell)) and (time is None or isinstance(time, datetime))

        self.location = location
        self.time = time

    def clone(self):
        return Checkin(location=self.location.clone(), time=self.time)

    def __str__(self) -> str:
        return str(self.time) + ',' + str(self.location)


class Trajectory:
    """
    A trajectory is the path that a moving user follows.
    """

    def __init__(self, checkins: list):
        """
        Initiation of a trajectory
        :param checkins: list, a list of check-ins
        """

        self.checkins = checkins

    def clone(self):
        """
        Return a deep copy of the trajectory.
        :return: Trajectory
        """

        return Trajectory([checkin.clone() for checkin in self.checkins])

    def coordinates(self) -> tuple:
        """
        Transform the trajectory to a series of coordinates.
        :return: tuple, a tuple of tuples, each tuple contains the coordiantes of a check-in
        """

        return tuple(checkin.location.coordinates() for checkin in self.checkins)

    def diameter(self) -> float:
        """
        Calculate the diameter of the trajectory, where the diameter refers to the largest distance of pairwise
        check-ins in the trajectory.
        :return: float
        """

        diameter = 0
        for i in range(len(self.checkins)):
            for j in range(i + 1, len(self.checkins)):
                # squared Euclidean distance
                dist = Spatial.sqeuclidean(self.checkins[i].location.coordinates(),
                                           self.checkins[j].location.coordinates())
                if dist > diameter:
                    diameter = dist
        return sqrt(diameter)

    def length(self) -> float:
        """
        Calculate the sum of travel distances of all of pairwise consecutive check-ins in the trajectory.
        :return: float
        """

        sum_dist = 0.0
        for i in range(len(self.checkins) - 1):
            sum_dist += Spatial.euclidean(self.checkins[i].location.coordinates(),
                                          self.checkins[i + 1].location.coordinates())
        return sum_dist


class Grid:
    """
    A set of cells used to discretize the location space.
    """

    def __init__(self, cells: set):
        """
        Create a grid from given cells.
        :param cells: set, a set of cells
        """

        self.cells = cells

    def __eq__(self, other) -> bool:
        """
        Check whether the grid is same as the other.
        :param other: UniformGrid
        :return: bool
        """

        return isinstance(other, Grid) and self.cells == other.cells

    def clone(self):
        return Grid(cells=set([cell.clone() for cell in self.cells]))

    def contains(self, cell: Cell) -> bool:
        """
        Checkin whether a given cell in the grid.
        :param cell: Cell
        :return: bool
        """

        assert isinstance(cell, Cell)

        return True if cell in self.cells else False

    def find(self, location: Location) -> Union[bool, None]:
        """
        Return the cell that the location falls in.
        :param location: Location
        :return: bool or None
        """

        assert isinstance(location, Location)

        for cell in self.cells:
            if cell.contains(location):
                return cell


class UniformGrid(Grid):
    """
    A grid composed of rectangular cells of the same size.
    """

    def __init__(self, boundary: tuple, shape: tuple):
        """
        Initiation of a uniform grid with a given the geographic location space and a resolution.
        :param boundary: tuple, bounrdary of a rectangular geographic location space,
                         (x-coordinate of lower left corner, y-..., x-coordinate of upper right corner, y-...)
        :param shape: tuple, (the number of cells in a row, the number of cells in a column)
        """

        assert isinstance(boundary, tuple) and isinstance(shape, tuple)

        self.boundary = boundary
        self.shape = shape
        self.num_cells = shape[0] * shape[1]
        self.cell_length = (boundary[2] - boundary[0]) / shape[0]
        self.cell_width = (boundary[3] - boundary[1]) / shape[1]

        # initiate self.cells (super.cells)
        cells = set()
        for i in range(self.shape[0] - 1):  # [0, self.shape[0] - 1]-th rows, [0, self.shape[1] - 2]-th columns
            for j in range(self.shape[1] - 1):  # [0, self.shape[0] - 2]-th rows, [0, self.shape[1] - 2]-th columns
                llx = i * self.cell_length + self.boundary[0]  # the lower left corner of the cell
                lly = j * self.cell_width + self.boundary[1]
                urx = llx + self.cell_length  # the upper right corner of the cell
                ury = lly + self.cell_width
                cells.add(Cell(Location(llx, lly), Location(urx, ury), coordinates=(i, j)))
            llx = i * self.cell_length + self.boundary[0]  # [self.shape[1] - 1]-th row, [0, self.shape[1] - 2] columns
            lly = (self.shape[1] - 1) * self.cell_width + self.boundary[1]
            urx = llx + self.cell_length
            ury = self.boundary[3]  # deal with cells in top row
            cells.add(Cell(Location(llx, lly), Location(urx, ury), coordinates=(i, self.shape[1] - 1)))
        for j in range(self.shape[1] - 1):  # [0, self.shape[0] - 2]-th rows, [self.shape[1] - 1]-th column
            llx = (self.shape[0] - 1) * self.cell_length + self.boundary[0]
            lly = j * self.cell_width + self.boundary[1]
            urx = self.boundary[2]  # deal with cells in right column
            ury = lly + self.cell_width
            cells.add(Cell(Location(llx, lly), Location(urx, ury), coordinates=(self.shape[0] - 1, j)))
        llx = (self.shape[0] - 1) * self.cell_length + self.boundary[0]  # deal with the upper right cell
        lly = (self.shape[1] - 1) * self.cell_width + self.boundary[1]
        urx = self.boundary[2]
        ury = self.boundary[3]
        cells.add(Cell(Location(llx, lly), Location(urx, ury), coordinates=(self.shape[0] - 1, self.shape[1] - 1)))
        # set cell id
        for cell in cells:
            cell.id_ = cell.x + cell.y * self.shape[0]
        Grid.__init__(self, cells)

        # initiate self.coordinate_cell, a mapping from grid coordinates to cells
        self.coordinate_cell = {cell.coordinates(): cell for cell in self.cells}

    def __eq__(self, other) -> bool:
        """
        Check whether the grid is same as the other.
        :param other: UniformGrid
        :return: bool
        """

        return isinstance(other, UniformGrid) and self.boundary == other.boundary and self.shape == other.shape

    def clone(self):
        uniformgrid = UniformGrid(boundary=self.boundary, shape=self.shape)
        uniformgrid.cells = set([cell.clone() for cell in self.cells])
        uniformgrid.coordinate_cell = {cell.coordinates(): cell for cell in uniformgrid.cells}
        return uniformgrid

    def contains_location(self, location: Location) -> bool:
        """
        Check whether the location falls in the grid.
        :param location: Location
        :return: bool
        """

        assert isinstance(location, Location)

        return self.boundary[0] <= location.x <= self.boundary[2] and self.boundary[1] <= location.y <= self.boundary[3]

    def contains(self, location: Union[Location, Cell]) -> bool:
        """
        Check whether a given location falls in the grid.
        :param location: Location or Cell
        :return: bool
        """

        assert isinstance(location, (Location, Cell))

        return self.contains_location(location) if type(location) == Location else Grid.contains(self, location)

    def find(self, location: Union[Location, tuple]) -> Union[bool, None]:
        """
        Return the cell that the location falls in.
        :param location: Location or tuple, a location or a pair of coordinates
        :return: bool or None
        """

        assert isinstance(location, (Location, tuple))

        return self.find_by_location(location) if type(location) == Location else self.find_by_coordinates(location)

    def find_by_coordinates(self, coordinates: tuple):
        """
        Return the cell with specified grid coordinates.
        :param coordinates: tuple, grid coordinates, (x-coordinate, y-coordinate)
        :return: Cell
        """

        assert isinstance(coordinates, tuple)
        assert 0 <= coordinates[0 < self.shape[0]] and 0 <= coordinates[1] < self.shape[1]

        return self.coordinate_cell[coordinates]

    def find_by_location(self, location: Location):
        """
        Return the cell that the location falls in. If the location fell outside the grid, return None.
        :param location: Location
        :return: Cell or None
        """

        assert isinstance(location, Location)

        if not self.contains(location):
            return None

        grid_coordinates = (min(self.shape[0] - 1, int(location.x / self.cell_length)),
                            min(self.shape[1] - 1, int(location.y / self.cell_width)))

        return self.find_by_coordinates(grid_coordinates)

    def shortest_path_between(self, start: Cell, end: Cell) -> list:
        """
        Return a shortest path between the starting cell (exclusive) and the ending cell (exclusive).
        :param start: Cell
        :param end: Cell
        :return: list, an ordered sequence of cells
        """

        assert isinstance(start, Cell) and isinstance(end, Cell) and start in self.cells and end in self.cells

        cells = []
        current_coordinates = list(start.coordinates())
        while True:
            cells.append(self.find_by_coordinates(tuple(current_coordinates)))  # 'start' is inclusive
            if end.x > current_coordinates[0]:
                current_coordinates[0] += 1
            elif end.x < current_coordinates[0]:
                current_coordinates[0] -= 1
            if end.y > current_coordinates[1]:
                current_coordinates[1] += 1
            elif end.y < current_coordinates[1]:
                current_coordinates[1] -= 1
            if list(end.coordinates()) == current_coordinates:
                break
        return cells[1:]  # ignore 'start'

    @staticmethod
    def are_adjecent(cell1: Cell, cell2: Cell) -> bool:
        """
        Check whether cell1 (cell2) is adjecent to cell2 (cell1).
        :param cell1: Cell
        :param cell2: Cell
        :return: bool
        """

        assert isinstance(cell1, Cell) and isinstance(cell2, Cell)

        # cell2 (cell1) is either one of the eight cells around cell1 (cell2) or equal to cell1 (cell2)
        return True if abs(cell1.x - cell2.x) <= 1 and abs(cell1.y - cell2.y) <= 1 else False


class UniformGridTrajectory(Trajectory):
    """
    A trajectory composed of an ordered sequence of uniform cells.
    """

    def __init__(self, checkins: list, grid: UniformGrid):
        Trajectory.__init__(self, checkins)
        self.grid = grid

    def clone(self):
        return UniformGridTrajectory(checkins=[checkin.clone() for checkin in self.checkins], grid=self.grid.clone())

    def deduplicate(self) -> None:
        """
        Remove consecutively check-ins with same cells.
        :return: None
        """

        deduplicated_checkins = [self.checkins[0]]
        for checkin in self.checkins:
            if checkin.location != deduplicated_checkins[-1].location:
                deduplicated_checkins.append(checkin)
        self.checkins = deduplicated_checkins

    def interpolate(self) -> None:
        """
        Insert some check-ins between consecutive check-ins to make the trajectory continuous.
        :return: None
        """

        interpolated_checkins = [self.checkins[0]]
        for checkin in self.checkins[1:]:
            if self.grid.are_adjecent(checkin.location, interpolated_checkins[-1].location):
                interpolated_checkins.append(checkin)
                continue
            # interpolate some check-ins between two check-ins with taken place in discontinuous cells recpectively
            for cell in self.grid.shortest_path_between(checkin.location, interpolated_checkins[-1].location):
                interpolated_checkins.append(Checkin(location=cell, time=None))
        self.checkins = interpolated_checkins

    @staticmethod
    def as_gridtrajectory(traj: Trajectory, grid: UniformGrid, deduplication_needed: bool, interpolation_needed: bool):
        """
        Convert a trajectory to grid trajectory using a specified grid.
        :param traj: Trajectory
        :param grid: UniformGrid
        :param deduplication_needed: bool, True represets removing consecutive duplicate cells
        :param interpolation_needed: bool, True represets interpolating some cells while False not
        :return: UniformGridTrajectory
        """

        assert isinstance(traj, Trajectory) and isinstance(grid, UniformGrid) and isinstance(interpolation_needed, bool)

        # convert each check-in's location to the cell that it falls in
        grid_checkins = []
        for checkin in traj.checkins:
            cell = grid.find(checkin.location)
            if not cell:
                continue
            grid_checkin = checkin.clone()
            grid_checkin.location = cell
            grid_checkins.append(grid_checkin)

        gridtrajectory = UniformGridTrajectory(grid=grid, checkins=grid_checkins)

        # remove duplicate consecutive check-ins
        if deduplication_needed:
            gridtrajectory.deduplicate()

        # interpolate some cells if needed
        if interpolation_needed:
            gridtrajectory.interpolate()

        return gridtrajectory


class User:
    """
    A user in location based service.
    """

    def __init__(self, userid: int, trajectory: Trajectory):
        """
        Initiation of a user with original (actual) trajectory and perturbed trajectory.
        :param userid: int, id of the user
        :param trajectory: Trajectory, a trajectory
        """

        self.userid = userid
        self.trajectory = trajectory

    def clone(self):
        return User(userid=self.userid, trajectory=self.trajectory.clone())


class Dataset:
    """
    A dataset composed of some users.
    """

    def __init__(self, users: list):
        self.users = users

    def clone(self):
        return Dataset(users=[user.clone() for user in self.users])

    def boundary(self) -> tuple:
        """
        Return the boundary of the dataset.
        :return: tuple, (x-coordinate of the lower left corner, y-..., x-coordiante of the upper right corner, y-...)
        """

        boundary = [float('inf'), float('inf'), -float('inf'), -float('inf')]
        for user in self.users:
            for checkin in user.trajectory.checkins:
                if checkin.location.x < boundary[0]:
                    boundary[0] = checkin.location.x
                elif checkin.location.x > boundary[2]:
                    boundary[2] = checkin.location.x
                if checkin.location.y < boundary[1]:
                    boundary[1] = checkin.location.y
                elif checkin.location.y > boundary[3]:
                    boundary[3] = checkin.location.y
        return tuple(boundary)

    @staticmethod
    def import_from_binary(filepath: str):
        """
        Import a dataset from binary file using pickle.
        :param filepath: str, path of the binary file.
        :return: Dataset
        """

        with open(filepath, 'rb') as file:
            return load(file)

    @staticmethod
    def import_from_database(database: Type[Database], tablename: str):
        """
        Import a dataset from database.
        :param database: Database, a mobility database class
        :param tablename: str, the name of the table of the dataset
        :return: Dataset, a dataset
        """

        assert issubclass(database, Database)

        conn = sq.connect(database.dbfilepath)
        cursor = conn.cursor()

        userids = [userid for userid, in cursor.execute(''.join(['SELECT DISTINCT userid',
                                                                 ' FROM ', tablename,
                                                                 ' ORDER BY userid ASC',
                                                                 # ' LIMIT 10'  # load part of users
                                                                 ])).fetchall()]

        users = []
        for userid in userids:
            records = cursor.execute(''.join(['SELECT locdatetime, clstlon, clstlat'] +
                                             # [(', catid' + str(i)) for i in range(1, database.tree_height)] +
                                             [' FROM ', tablename, ' WHERE userid = ? ORDER BY locdatetime ASC']),
                                     (userid,)).fetchall()
            # traj = Trajectory([Checkin(time=datetime.strptime(record[0], database.locdatetime_format),
            #                            location=Location(*CoordinatesConverter.geographic2cartesian(record[1:3]),
            #                                              category=('0',) + record[3:]))
            #                    for record in records])
            traj = Trajectory([Checkin(time=datetime.strptime(record[0], database.locdatetime_format),
                                       location=Location(x=record[1], y=record[2]
                                                         # , category=('0',) + record[3:]
                                                         ))
                               for record in records])
            users.append(User(userid, traj))

        conn.close()

        return Dataset(users)

    @staticmethod
    def import_from_adatrace(filepath: str):
        """
        Import an AdaTrace dataset.
        :param filepath: str, path of the AdaTrace dataset file
        :return: Database, a dataset
        """

        try:
            file1 = open(filepath, 'r')
            file2 = open(filepath, 'r')
        except OSError:
            raise
        else:
            default_cat = ('root',) + (None,) * (Database.tree_height - 1)

            users = []
            file2.readline()  # let file1 pointspoint to the 0-th line and file2 to the 1-th line
            while True:
                line1 = file1.readline()
                line2 = file2.readline()
                if not line1 or not line2:
                    break
                elif line1[0] == '#' and line2[0] == '>':  # found a new user
                    userid = int(line1[1:-2])  # e.g., '#0:\n'
                    checkins = []
                    for positions_str in line2[3:-2].split(sep=';'):  # e.g., '>0:11026.0,4693.0;11096.0,4669.2;\n'
                        coordinates = positions_str.split(sep=',')
                        checkins.append(Checkin(time=None, location=Location(*coordinates, category=default_cat)))
                    users.append(User(userid=userid, trajectory=Trajectory(checkins)))

            file1.close()
            file2.close()

        return Dataset(users)

    def export_to_database(self, database: Type[Database], tablename: str) -> None:
        """
        Export a dataset to database.
        :param database: Database, target database
        :param tablename: str, name of the target table
        :return: None
        """

        assert issubclass(database, Database)

        conn = sq.connect(database.dbfilepath)
        cursor = conn.cursor()

        # create a table in the database to store the perturbed trajectories
        cursor.execute(''.join(['DROP TABLE IF EXISTS ', tablename]))
        cursor.execute(''.join(['CREATE TABLE ', tablename,
                                '(id INTEGER PRIMARY KEY, userid INTEGER, locdatetime DATETIME, lon REAL, lat REAL'] +
                               [(', catid' + str(i) + ' TEXT') for i in range(1, database.tree_height)] + [')', ]))

        # transform users' perturbed trajectories to a list of tuples (check-ins)
        records = []
        for user in self.users:
            for checkin in user.trajectory.checkins:
                record = (user.userid, checkin.time)
                # record += CoordinatesConverter.cartesian2geographic(checkin.location.coordinates())
                record += checkin.location.coordinates()
                record += checkin.location.category[1:]  # skip the root category at category[0]
                records.append(record)

        cursor.executemany(''.join(['INSERT INTO ', tablename, '(userid, locdatetime, clstlon, clstlat'] +
                                   [(', catid' + str(i)) for i in range(1, database.tree_height)] +
                                   [') VALUES (?, ?, ?, ?'] +
                                   [', ?' * (database.tree_height - 1), ')']),
                           records)  # bulk insert

        conn.commit()
        conn.close()

    def export_to_adatrace(self, filename: str) -> None:
        """
        Export a dataset to disk following the AdaTrace format.
        :param filename: str
        :return: None
        """

        assert isinstance(filename, str)

        with open(filename, 'w+') as file:
            for user in self.users:
                line = ''.join(['#', str(user.userid), ':\n>0:',
                                ';'.join([str(checkin.location) for checkin in user.trajectory.checkins]),
                                ';\n'])
                file.write(line)

    def export_to_binary(self, filepath: str) -> None:
        """
        Export current dataset to binary file using pickle.
        :param filepath: path of the binary file.
        :return: None
        """

        with open(filepath, mode='wb') as file:
            dump(self, file)


class UniformGridDataset(Dataset):
    """
    A dataset with some uniform-grid trajectories.
    """

    def __init__(self, users: list, grid: UniformGrid, deduplication_needed: bool, interpolation_needed: bool):
        # confirm that all trajectories share the same uniform grid
        for user in users:
            assert user.trajectory.grid == grid

        Dataset.__init__(self, users)
        self.grid = grid
        self.deduplication_needed = deduplication_needed
        self.interpolation_needed = interpolation_needed

    def clone(self):
        return UniformGridDataset(users=[user.clone() for user in self.users],
                                  grid=self.grid.clone(),
                                  deduplication_needed=self.deduplication_needed,
                                  interpolation_needed=self.interpolation_needed)

    @staticmethod
    def as_griddataset(dataset: Dataset, grid: UniformGrid, deduplication_needed: bool, interpolation_needed: bool):
        """
        Generate a uniform-grid dataset by converting each trajecroty in the dataset to grid trajectory.
        :param dataset: Dataset
        :param grid: UniformGrid
        :param deduplication_needed: bool, True represets removing consecutive duplicate cells
        :param interpolation_needed: bool, True represets interpolating some cells while False not
        :return: GridDataset
        """

        assert isinstance(dataset, Dataset) and isinstance(grid, UniformGrid)

        grid_dataset = dataset.clone()  # too slow when the dataset is large
        for user in grid_dataset.users:
            user.trajectory = UniformGridTrajectory.as_gridtrajectory(traj=user.trajectory,
                                                                      grid=grid,
                                                                      deduplication_needed=deduplication_needed,
                                                                      interpolation_needed=interpolation_needed)
        return UniformGridDataset(users=grid_dataset.users,
                                  grid=grid,
                                  deduplication_needed=deduplication_needed,
                                  interpolation_needed=interpolation_needed)
