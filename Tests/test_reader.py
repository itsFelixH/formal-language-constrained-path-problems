import unittest
import os
from reader import Reader


class TestReader(unittest.TestCase):
    def test_get_coordinates(self):
        path = os.path.join("../MapData", "USA-road-d.NY.co")
        dic = Reader.get_coordinates(path)

        self.assertEqual(dic[1][0], -73530767)
        self.assertEqual(dic[1][1], 41085396)
        self.assertEqual(dic[143903][0], -73948250)
        self.assertEqual(dic[143903][1], 40633610)
        self.assertEqual(dic[264346][0], -73917690)
        self.assertEqual(dic[264346][1], 41291980)

    def test_get_graph_data(self):
        path = os.path.join("../MapData", "USA-road-d.NY.gr")
        G = Reader.get_graph_data(path)

        self.assertEqual(G.number_of_nodes(), 264346)
        self.assertEqual(G.number_of_edges(), 730100)
        self.assertIsNotNone(G.nodes())
        self.assertIsNotNone(G.edges())

        for u, v, d in G.edges(data=True):
            self.assertIsNotNone(d['weight'])