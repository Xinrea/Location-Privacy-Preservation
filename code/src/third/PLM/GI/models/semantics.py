# encoding=utf-8
from multiprocessing import Pool
from pickle import dump, load
from typing import Union, Iterable

from anytree import AnyNode, LevelOrderIter
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
from anytree.search import find
from foursquare import Foursquare, FoursquareException

from GI.models.base import Dataset
from GI.models.tools import Spatial, CoordinatesConverter


class Cache:
    """
    A mapping from positions to categories.
    """

    COORDINATE_DIFFERENCE_THRESHOLD = 0.0001  # coordinate difference threshold for position comparison
    FILEPATH = 'vanue_categories.cache'  # path of the cache of venue catogories

    def __init__(self):
        self.positions_categories = {}  # {tuple: tuple}

    def has(self, position: tuple):
        """
        Check if there is an equivalent of the given position in cache. If exists, return the equivalent, else None.
        :param position: tuple
        :return: tuple or None
        """

        for cached_position in self.positions_categories.keys():
            if Cache.position_equality(cached_position, position):
                return cached_position
        return None

    def set(self, position: tuple, category: tuple) -> None:
        """
        Add a new position with venue category into cache.
        If there is an equivalent position in cache, update its category by given category.
        :param position: tuple
        :param category: tuple
        :return: None
        """

        equivalent_position = self.has(position)
        if equivalent_position:
            self.positions_categories[equivalent_position] = category
        else:
            self.positions_categories[position] = category

    def get(self, position: tuple) -> Union[tuple, None]:
        """
        Return the venue category of a given position. If there is no euivalent position in cache, return None.
        :param position: tuple
        :return: None
        """

        equivalent_position = self.has(position)
        if equivalent_position:
            return self.positions_categories[equivalent_position]
        return None

    def set_without_check(self, position: tuple, category: tuple) -> None:
        """
        Add a new position with venue category into cache.
        This mechod do not check whether there is an equivalent position in cache.
        :param position: tuple
        :param category: tuple
        :return: None
        """

        self.positions_categories[position] = category

    def get_without_check(self, position: tuple) -> Union[tuple, None]:
        """
        Return the venue category of a given position.
        This mechod do not check whether there is an equivalent position in cache.
        :param position: tuple
        :return: None
        """

        return self.positions_categories[position]

    def load(self):
        """
        Read cache from file.
        :return: None
        """
        with open(Cache.FILEPATH, 'rb') as file:
            self.positions_categories = load(file)

    def save(self):
        """
        Write cache to file.
        :return: None
        """

        with open(Cache.FILEPATH, 'wb+') as file:
            dump(self.positions_categories, file)

    @staticmethod
    def position_equality(position1: tuple, position2: tuple) -> bool:
        """
        Checkin whether two positions are equivalent.
        :param position1: tuple
        :param position2: tuple
        :return: bool
        """

        for coordinate1, coordinate2 in zip(position1, position2):
            if abs(coordinate1 - coordinate2) > Cache.COORDINATE_DIFFERENCE_THRESHOLD:
                return False
        return True


class Semantics:
    """
    Operations related to location semantics (a.k.a. Foursquare venue categories).

    Category of positon is defined as a tuple:
    (root category id, 1-st floor category id, ..., 4-th floor category id), e.g.,
    ('0', '4d4b7105d754a06377d81259', '4bf58dd8d48988d165941735', None, None, None).

    The category stored in database is defined as (catid1, catid2, catid3, catid4, catid5),
    where the root category id '0' is ignored.
    """

    TREE_FILEPATH = 'vanue_categories.anytree'  # path of the catetory file
    MAX_SEARCHING_RADIUS1 = 1000  # meters
    MAX_SEARCHING_RADIUS2 = 0.001  # squared degrees, 0.001 ~ 1km^2
    CLIENT_ID = 'NNWECOZ41XSTTBVNMZGSROSM3MDOFWMZZNW0WQMCL5GXVTCF'
    CLIENT_SECRET = 'MIC5VMAQK3CQWMC5ZBD3FRWESZUJCZDV4UCW5O1Q5J210HY5'

    def __init__(self):
        self.client = Foursquare(Semantics.CLIENT_ID, Semantics.CLIENT_SECRET)  # connect to Foursquare
        self.tree = None
        self.cache = Cache()

        # load the venue category tree
        try:
            file = open(Semantics.TREE_FILEPATH, 'r')
            self.tree = JsonImporter().read(file)
        except OSError:
            # download the tree from Foursquare and save it to disk
            print('Failed to load venue categories tree from disk. Download it from Foursquare.')
            self.download_tree()

        # load the venue category cache
        self.cache.load()

    def download_tree(self) -> None:
        """
        Acquire the venue catetories tree from Foursquare.
        :return: anytree, the root node of the venue categories tree
        """

        try:
            source_tree = self.client.venues.categories()  # Foursquare venue categories tree
        except FoursquareException:
            raise
        else:
            # create an empty tree to copy the Foursquare catetories tree
            target_tree = AnyNode(name='root', parent=None, id='0', pluralName='root', shortName='root')

            # define a method of inorder tree traversal
            def traverse(parent1, parent2):
                for child1 in parent1['categories']:
                    child2 = AnyNode(name=child1['name'], parent=parent2, id=child1['id'],
                                     pluralName=child1['pluralName'], shortName=child1['shortName'])
                    traverse(child1, child2)

            # copy the online Foursquare tree
            traverse(source_tree, target_tree)

            # update self.tree and write it to a Json file named by 'self.TREE_FILEPATH'
            self.tree = target_tree
            with open(self.TREE_FILEPATH, 'w') as file:
                JsonExporter(indent=2, sort_keys=True).write(target_tree, file)

    def categories_on_level(self, level: int) -> set:
        """
        Return the category nodes at the specified level, where 1 represents the root level.
        :param level: int
        :return: set, a set of venue category ids.
        """

        category_ids = set()
        for node in LevelOrderIter(self.tree):  # level-order tree traversal
            node_level = node.depth + 1  # level = depth + 1, where the depth of root is 0
            if node_level == level:
                category_ids.add(node.id)
            elif node_level > level:  # found a node at a lower level, break
                break
        return category_ids

    def get_online_category(self, position: tuple) -> tuple:
        """
        Acquire the category of the location with given geographic coordinates using Foursquare APIs.
        :param position: tuple or list, geographic coordinates, (longitude, latitude)
        :return: list, a list of categories of the location
        """

        try:
            # browse venues within a given area specified by a center coordinate 'll' and 'max_searching_radius1'
            # eg, https://api.foursquare.com/v2/venues/search?intent=browse&radius=1000&ll=37.80710935,-122.4456310167
            venues = self.client.venues.search(params={'intent': 'browse',  # 'll' := latitude, longitude
                                                       'll': ''.join([str(position[1]), ',', str(position[0])]),
                                                       'radius': self.MAX_SEARCHING_RADIUS1})
        except FoursquareException as e:  # failed to query category, then return the root category
            print('Failed to search venue category for %s.' % str(position))
            print(e)
            return self.tree.id,  # this is a tuple
        else:  # succeeded to query category
            assert isinstance(venues, dict) and 'venues' in venues.keys(), 'Wrong result set type.'
            assert venues['venues'], 'Empty result set returned.'

            # find the venue which has category and is nearest to 'position' and the distance between thr venue and
            # 'position' is less than max_searching_radius2
            nearest = None
            min_sqeuclidean_distance = self.MAX_SEARCHING_RADIUS2
            for venue in venues['venues']:
                if venue['categories']:
                    sqeuclidean_distance = Spatial.sqeuclidean(position,
                                                               (venue['location']['lng'], venue['location']['lat']))
                    if sqeuclidean_distance < min_sqeuclidean_distance:
                        min_sqeuclidean_distance = sqeuclidean_distance
                        nearest = venue

            print('Succeed to obtain the venue category of (%f, %f).' % position)
            if nearest:  # succeeded to find a valid venue, then return its category
                category_id = nearest['categories'][0]['id']
                category_node = find(self.tree, lambda node: node.id == category_id)  # an anytree node
                # failed to find the node of which the category id is 'category_id'
                assert category_node, 'Found no node in the vanue categories tree for %s.' % category_id
                # found the node, then obtain all parent nodes' category ids as its category,
                # where [0] is the root category id
                category = [category_id, ]
                parent = category_node.parent
                while parent:
                    category.insert(0, parent.id)
                    parent = parent.parent
                # append some 'None's if category were not the leaf node to ensure len(category) == height of the tree
                category += [None, ] * (self.tree.height + 1 - len(category))
                return tuple(category)
            else:  # failed to find a valid venue, then return the root category
                return (self.tree.id,) + (None,) * (self.tree.height - 1)  # this is a tuple

    def get_cached_category(self, position: tuple) -> tuple:
        """
        Acquire the category of the location with cache.
        :param position: tuple or list, geographic coordinates, (longitude, latitude)
        :return: tuple, venue category of the location
        """

        cached_category = self.cache.get(position)
        if cached_category:  # cache hit
            return cached_category
        else:  # cache miss
            print('cache miss.')
            category = self.get_online_category(position)
            self.cache.set(position, category)
            return category

    def categories_of(self, positions: Iterable) -> dict:
        """
        Acquire venue categories for given geographic positions with cache.
        :param positions: list, a list of geographic positions
        :return: dict, a mapping from positions to their categories
        """

        # try to acquire category for all positions, got None for uncached positions
        pool = Pool(processes=8)  # processes should not be larger than the max number of thread of CPU
        positions_categories = dict(zip(positions, pool.map(self.cache.get, positions)))
        pool.close()

        # acquire category for uncached positions using Foursquare APIs
        uncached_positions = tuple(pos for pos, cat in positions_categories.items() if not cat)
        print('%d uncached positions to acquire online categories.' % len(uncached_positions))
        pool = Pool(processes=32)  # processes can be a large value since this operation has a low usage of CPU
        uncachedpositions_categories = dict(zip(uncached_positions,
                                                pool.map(self.get_online_category, uncached_positions)))
        pool.close()

        # save uncached categories to cache
        for pos, cat in uncachedpositions_categories.items():
            self.cache.set(pos, cat)
        self.cache.save()

        # merge cached and uncached categories
        positions_categories = {**positions_categories, **uncachedpositions_categories}

        return positions_categories

    def set_categories(self, dataset: Dataset) -> None:
        """
        Acquire venue categories for actual check-ins and perturbed check-ins using Foursquare APIs.
        Cartesian coordinates in the dateset required!
        :param dataset: Dataset
        :return: None
        """

        # collect unique Catesian positions and create a mapping from Cartesian positions to geographic positions
        cartesians_geographics = {}
        for user in dataset.users:
            for checkin in user.trajectory.checkins:
                coordinates = CoordinatesConverter.cartesian2geographic(checkin.location.coordinates())
                cartesians_geographics[checkin.location.coordinates()] = coordinates

        # acquire venue categories and create a mapping from geographic positions to categories
        geographics_categories = self.categories_of(cartesians_geographics.values())

        # set venue categories for the dataset
        for user in dataset.users:
            for checkin in user.trajectory.checkins:
                checkin.location.category = \
                    geographics_categories[cartesians_geographics[checkin.location.coordinates()]]

    def update_categories(self, database) -> None:
        import sqlite3 as sq
        from GI.models.database import Database

        assert issubclass(database, Database)

        conn = sq.connect(database.dbfilepath)
        cursor = conn.cursor()

        # add columns for categories
        try:
            cursor.executescript(''.join(['ALTER TABLE ', database.Checkin.__tablename__, ' ADD catid1 TEXT;',
                                          'ALTER TABLE ', database.Checkin.__tablename__, ' ADD catid2 TEXT;',
                                          'ALTER TABLE ', database.Checkin.__tablename__, ' ADD catid3 TEXT;',
                                          'ALTER TABLE ', database.Checkin.__tablename__, ' ADD catid4 TEXT;',
                                          'ALTER TABLE ', database.Checkin.__tablename__, ' ADD catid5 TEXT;'
                                          ]))
            conn.commit()
        except sq.OperationalError:
            #  do nothing if the catid columns already exist
            pass

        # collect unique positions
        positions = [(lon, lat) for lon, lat in cursor.execute(''.join(['SELECT DISTINCT clstlon, clstlat ',
                                                                        'FROM ', database.Checkin.__tablename__])
                                                               ).fetchall()]

        # acquire categories for positions
        pos2cat = self.categories_of(positions)

        # update categories of positions in database
        parameters = [(*cat[1:], *pos) for pos, cat in pos2cat.items()]
        cursor.executemany(''.join(['UPDATE ', database.Checkin.__tablename__, ' ',
                                    'SET catid1 = ?, catid2 = ?, catid3 = ?, catid4 = ?, catid5 = ? ',
                                    'WHERE clstlon = ? AND clstlat = ?']),
                           parameters)

        conn.commit()
        conn.close()


if __name__ == '__main__':
    def init_cache() -> None:
        """
        Acquire venue category for positions in the given datasets from Foursquare, and then cache the results to disk.
        :return: None
        """

        import sqlite3 as sq
        import GI.models.database

        dataset_names = [
            'SNAPBrightkite0201',
            # 'Gowalla0201',
            # 'Gowalla0301',
            # 'Gowalla0401',
        ]

        semantics = Semantics()

        # acquire venue category for the first time
        print('Cache venue categories for the following datasets: ')
        for dataset_name in dataset_names:
            dataset = getattr(GI.models.database, dataset_name)

            conn = sq.connect(dataset.dbfilepath)
            cursor = conn.cursor()

            # fetch all unique positions
            positions = [(lon, lat) for lon, lat in cursor.execute(''.join(['SELECT DISTINCT clstlon, clstlat ',
                                                                            'FROM ',
                                                                            dataset.checkins.name,
                                                                            # ' LIMIT 3'
                                                                            ])).fetchall()]

            # cache the results in chunks
            print(dataset.name, 'with', str(len(positions)), 'positions')
            cnt = 1
            chunk_num = 100
            chunk_size = int(len(positions) / chunk_num)
            for position in positions:
                semantics.get_cached_category(position)
                if cnt % chunk_size == 0:  # the processing of a chunk of positions completed, then save the cache
                    print('%-3d%% work complete.' % (int(cnt / len(positions) * 100)))
                    semantics.cache.save()
                cnt += 1

            semantics.cache.save()  # save the results of the last chunk
            conn.close()

        # re-consider those positions that we failed to acquire the categories just now
        # A category is invalid if category[1] == None.
        # A position with invalid category is called an invalid position.
        invalid_positions = []
        for position, category in semantics.cache.positions_categories.items():
            if not category[1]:
                invalid_positions.append(position)

        if invalid_positions:
            print('Re-acquire venue category for', len(invalid_positions), 'positions.')
            map(semantics.get_cached_category, invalid_positions)
            semantics.cache.save()


    from GI.models.database import Gowalla0501 as Database

    print('Update categories for the database: %s.' % Database.name)
    semantics = Semantics()
    semantics.update_categories(Database)
