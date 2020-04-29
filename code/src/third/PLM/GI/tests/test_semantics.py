# encoding=utf-8
import unittest

from anytree.node import AnyNode
from anytree.exporter import DotExporter
from GI.models.semantics import Semantics


class TestSemantics(unittest.TestCase):
    def setUp(self):
        self.semantics = Semantics()

    def test_init(self):
        self.assertIsInstance(self.semantics.tree, AnyNode)
        self.assertIsInstance(self.semantics.cache, dict)
        DotExporter(self.semantics.tree).to_dotfile("venue_categories.dot")
        # Render the tree in https://edotor.net/ by copying the content in dot file and downloading the svg image

    def test_category_of(self):
        # an example in: https://foursquare.com/developers/explore#req=venues%2Fsearch%3Fll%3D40.7484%2C-73.9857
        lonlat = (-73.9857, 40.7484)
        expected_category = ('0', '4d4b7105d754a06372d81259', '4bf58dd8d48988d198941735', None, None, None)
        found_category = self.semantics.get_cached_category(lonlat)
        self.assertTupleEqual(expected_category, found_category)

    def test_init_cache(self):
        Semantics.init_cache()


if __name__ == '__main__':
    unittest.main()
