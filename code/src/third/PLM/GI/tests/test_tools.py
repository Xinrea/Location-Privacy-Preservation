# encoding=utf-8
import unittest

from GI.protections.noise import CoordinatesConverter
from GI.models.tools import DatasetImporter


class TestCoordinatesConverter(unittest.TestCase):
    def test_geographic2cartesian(self):
        lonlat = (0, 0)
        xy = CoordinatesConverter.geographic2cartesian(lonlat)
        self.assertAlmostEqual(xy[0], 0, delta=0.001)
        self.assertAlmostEqual(xy[1], 0, delta=0.001)

        lonlat = (-180, 0)
        xy = CoordinatesConverter.geographic2cartesian(lonlat)
        self.assertAlmostEqual(xy[0], -20037508.342789244, delta=0.001)
        self.assertAlmostEqual(xy[1], 0, delta=0.001)

        lonlat = (180, 0)
        xy = CoordinatesConverter.geographic2cartesian(lonlat)
        self.assertAlmostEqual(xy[0], 20037508.342789244, delta=0.001)
        self.assertAlmostEqual(xy[1], 0, delta=0.001)

        lonlat = (180, 90)
        xy = CoordinatesConverter.geographic2cartesian(lonlat)
        self.assertAlmostEqual(xy[0], 20037508.342789244, delta=0.001)
        self.assertAlmostEqual(xy[1], 238107693.26496765, delta=0.001)

        lonlat = (-122.5153, 37.7084)  # San Francisco
        xy = CoordinatesConverter.geographic2cartesian(lonlat)
        self.assertAlmostEqual(xy[0], -13638340.810385149, delta=0.001)
        self.assertAlmostEqual(xy[1], 4538314.016916643, delta=0.001)

        lonlat = (-122.5153, 37.7084)  # San Francisco
        xy = CoordinatesConverter.geographic2cartesian(lonlat)
        lonlat_expected = CoordinatesConverter.cartesian2geographic(xy)
        self.assertAlmostEqual(lonlat[0], lonlat_expected[0], delta=0.001)
        self.assertAlmostEqual(lonlat[1], lonlat_expected[1], delta=0.001)

    def test_cartesian2geographic(self):
        xy = (-13638340.810385149, 4538314.016916643)  # San Francisco
        lonlat = CoordinatesConverter.cartesian2geographic(xy)
        xy_expected = CoordinatesConverter.geographic2cartesian(lonlat)
        self.assertAlmostEqual(xy[0], xy_expected[0], delta=0.001)
        self.assertAlmostEqual(xy[1], xy_expected[1], delta=0.001)

    def test_to_cartesian_boundary(self):
        geo_boundary = (-180, 0, 180, 90)
        car_boundary = CoordinatesConverter.to_cartesian_boundary(geo_boundary)
        car_boundary_expected = (-20037508.342789244, 0, 20037508.342789244, 238107693.26496765)
        self.assertEqual(len(car_boundary), len(car_boundary_expected))
        for i, j in zip(car_boundary, car_boundary_expected):
            self.assertAlmostEqual(i, j, delta=0.001)


class TestDatasetImporter(unittest.TestCase):
    def test_load_adatrace_dataset(self):
        dataset_directory = 'D:\\Workspace\\IWorkspace\\AdaTrace\\'
        wrong_actual_dataset_filepath = dataset_directory + 'wrong_brinkhoff.dat'
        self.assertRaises(OSError, DatasetImporter.import_from_adatrace, wrong_actual_dataset_filepath)


if __name__ == '__main__':
    unittest.main()
