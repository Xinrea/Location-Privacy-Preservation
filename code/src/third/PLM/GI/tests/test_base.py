# encoding=utf-8
import unittest

from GI.models.base import *


class TestLocation(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(AssertionError):
            Location(x=0, y=0.0, category=None)
        with self.assertRaises(AssertionError):
            Location(x=0.0, y=0, category=None)
        with self.assertRaises(AssertionError):
            Location(x=0, y=0, category=None)
        with self.assertRaises(AssertionError):
            Location(x=0.0, y=0.0, category=[])

    def test_eq(self):
        loc1 = Location(x=0.0, y=0.0, category=None)
        loc2 = Location(x=0.0, y=0.0, category=None)
        self.assertEqual(loc1, loc2)

    def test_str(self):
        loc = Location(x=0.0, y=0.0, category=None)
        self.assertEqual(loc.__str__(), '(0.0,0.0)')

    def test_coordinates(self):
        loc = Location(x=0.0, y=0.0, category=None)
        self.assertTupleEqual(loc.coordinates(), (0.0, 0.0))


class TestCell(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(AssertionError):
            Cell(ll=None, ur=Location(0.0, 0.0))
        with self.assertRaises(AssertionError):
            Cell(ll=Location(0.0, 0.0), ur=None)
        with self.assertRaises(AssertionError):
            Cell(ll=None, ur=None)
        with self.assertRaises(AssertionError):
            Cell(ll=Location(0.0, 0.0), ur=Location(0.0, 0.0), coordinates=[])


if __name__ == '__main__':
    unittest.main()
