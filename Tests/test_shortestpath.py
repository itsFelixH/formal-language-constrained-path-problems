import unittest
import networkx as nx
import random
from graph import GraphGenerator
from reader import Reader
from shortestpath import Dijkstra, DAGraph, SPGraph


class TestDijkstra(unittest.TestCase):

    def test_s_shortest_path(self):
        G = GraphGenerator.random_weighted_graph(100, 0.03, 50)
        nodes = G.nodes()

        source = random.choice(nodes)

        expected_dist = nx.shortest_path_length(G, source=source, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, weight="weight")
        (dist, pred) = Dijkstra.s_shortest_path(G, source)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])

    def test_s_shortest_path__multidigraph(self):
        G = GraphGenerator.random_weighted_spg(100, 50)
        nodes = G.nodes()

        source = random.choice(nodes)

        expected_dist = nx.shortest_path_length(G, source=source, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, weight="weight")
        (dist, pred) = Dijkstra.s_shortest_path(G, source)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])

    def test_s_shortest_path__dag(self):
        G = GraphGenerator.random_weighted_dag(100, 0.03, 50)
        nodes = G.nodes()

        source = random.choice(nodes)

        expected_dist = nx.shortest_path_length(G, source=source, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, weight="weight")
        (dist, pred) = Dijkstra.s_shortest_path(G, source)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])

    def test_s_shortest_path__spg(self):
        G = GraphGenerator.random_weighted_spg(100, 50)
        nodes = G.nodes()

        source = random.choice(nodes)

        expected_dist = nx.shortest_path_length(G, source=source, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, weight="weight")
        (dist, pred) = Dijkstra.s_shortest_path(G, source)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])

    def test_s_shortest_path_heap(self):
        G = GraphGenerator.random_weighted_graph(100, 0.03, 50)
        nodes = G.nodes()

        source = random.choice(nodes)

        expected_dist = nx.shortest_path_length(G, source=source, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, weight="weight")
        (dist, pred) = Dijkstra.s_shortest_path_heap(G, source)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])

    def test_s_shortest_path_heap__multidigraph(self):
        G = GraphGenerator.random_weighted_graph(100, 0.03, 50)
        nodes = G.nodes()

        source = random.choice(nodes)

        expected_dist = nx.shortest_path_length(G, source=source, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, weight="weight")
        (dist, pred) = Dijkstra.s_shortest_path_heap(G, source)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])

    def test_s_shortest_path_heap__dag(self):
        G = GraphGenerator.random_weighted_dag(100, 0.03, 50)
        nodes = G.nodes()

        source = random.choice(nodes)

        expected_dist = nx.shortest_path_length(G, source=source, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, weight="weight")
        (dist, pred) = Dijkstra.s_shortest_path_heap(G, source)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])

    def test_s_shortest_path_heap__spg(self):
        G = GraphGenerator.random_weighted_spg(100, 50)
        nodes = G.nodes()

        source = random.choice(nodes)

        expected_dist = nx.shortest_path_length(G, source=source, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, weight="weight")
        (dist, pred) = Dijkstra.s_shortest_path_heap(G, source)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])

    def test_st_shortest_path_heap(self):
        G = GraphGenerator.random_weighted_graph(100, 0.03, 50)
        nodes = set(nx.nodes(G))
        sources = random.sample(nodes, 5)
        targets = random.sample(nodes, 5)

        pairs = zip(sources, targets)

        for pair in pairs:
            source = pair[0]
            target = pair[1]

            expected_dist = 0
            expected_path = []
            expected_error = 0
            try:
                expected_dist = nx.shortest_path_length(G, source, target, weight="weight")
                expected_path = nx.shortest_path(G, source, target, weight="weight")
            except nx.NetworkXNoPath:
                expected_error = 1

            dist = 0
            path = []
            error = 0
            try:
                (dist, path) = Dijkstra.st_shortest_path_heap(G, source, target)
            except nx.NetworkXNoPath:
                error = 1

            self.assertEqual(dist, expected_dist)
            self.assertEqual(path, expected_path)
            self.assertEqual(error, expected_error)

    def test_st_shortest_path_heap__source_is_target(self):
        G = GraphGenerator.random_weighted_graph(100, 0.03, 50)
        source = random.choice(G.nodes())
        target = source

        expected_dist = 0
        expected_path = [source]

        (dist, path) = Dijkstra.st_shortest_path_heap(G, source, target)

        self.assertEqual(dist, expected_dist)
        self.assertEqual(path, expected_path)

    def test_st_shortest_path_heap__multidigraph(self):
        G = GraphGenerator.random_weighted_spg(100, 50)
        nodes = set(G.nodes())
        sources = random.sample(nodes, 5)
        targets = random.sample(nodes, 5)

        pairs = zip(sources, targets)

        for pair in pairs:
            source = pair[0]
            target = pair[1]

            expected_dist = 0
            expected_path = []
            expected_error = 0
            try:
                expected_dist = nx.shortest_path_length(G, source, target, weight="weight")
                expected_path = nx.shortest_path(G, source, target, weight="weight")
            except nx.NetworkXNoPath:
                expected_error = 1

            dist = 0
            path = []
            error = 0
            try:
                (dist, path) = Dijkstra.st_shortest_path_heap(G, source, target)
            except nx.NetworkXNoPath:
                error = 1

            self.assertEqual(dist, expected_dist)
            self.assertEqual(path, expected_path)
            self.assertEqual(error, expected_error)

    def test_st_shortest_path_heap__dag(self):
        G = GraphGenerator.random_weighted_dag(100, 0.03, 50)
        nodes = set(G.nodes())
        sources = random.sample(nodes, 5)
        targets = random.sample(nodes, 5)

        pairs = zip(sources, targets)

        for pair in pairs:
            source = pair[0]
            target = pair[1]

            expected_dist = 0
            expected_path = []
            expected_error = 0
            try:
                expected_dist = nx.shortest_path_length(G, source, target, weight="weight")
                expected_path = nx.shortest_path(G, source, target, weight="weight")
            except nx.NetworkXNoPath:
                expected_error = 1

            dist = 0
            path = []
            error = 0
            try:
                (dist, path) = Dijkstra.st_shortest_path_heap(G, source, target)
            except nx.NetworkXNoPath:
                error = 1

            self.assertEqual(dist, expected_dist)
            self.assertEqual(path, expected_path)
            self.assertEqual(error, expected_error)

    def test_st_shortest_path_heap__spg(self):
        G = GraphGenerator.random_weighted_spg(100, 50)
        nodes = set(G.nodes())
        sources = random.sample(nodes, 5)
        targets = random.sample(nodes, 5)

        pairs = zip(sources, targets)

        for pair in pairs:
            source = pair[0]
            target = pair[1]

            expected_dist = 0
            expected_path = []
            expected_error = 0
            try:
                expected_dist = nx.shortest_path_length(G, source, target, weight="weight")
                expected_path = nx.shortest_path(G, source, target, weight="weight")
            except nx.NetworkXNoPath:
                expected_error = 1

            dist = 0
            path = []
            error = 0
            try:
                (dist, path) = Dijkstra.st_shortest_path_heap(G, source, target)
            except nx.NetworkXNoPath:
                error = 1

            self.assertEqual(dist, expected_dist)
            self.assertEqual(path, expected_path)
            self.assertEqual(error, expected_error)

    def test_st_shortest_path_heap__NY(self):
        [G, dic] = Reader.convert_to_graph('USA-road-d.NY')

        source = random.choice(G.nodes())
        target = random.choice(G.nodes())

        expected_dist = nx.shortest_path_length(G, source=source, target=target, weight="weight")
        expected_path = nx.shortest_path(G, source=source, target=target, weight="weight")

        (dist, path) = Dijkstra.st_shortest_path_heap(G, source, target)

        self.assertEqual(dist, expected_dist)
        self.assertEqual(path, expected_path)


class TestDAGraph(unittest.TestCase):

    def test_top_sort(self):
        G = GraphGenerator.random_weighted_dag(100, 0.03, 50)
        order = DAGraph.top_sort(G)
        exspected_order = nx.topological_sort(G)

        self.assertEqual(order, exspected_order)

    def test_s_shortest_path(self):
        G = GraphGenerator.random_weighted_dag(100, 0.03, 50)
        nodes = set(nx.nodes(G))

        source = random.choice(nx.nodes(G))

        (dist, pred) = DAGraph.s_shortest_path(G, source)
        expected_dist = nx.shortest_path_length(G, source=source, target=None, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, target=None, weight="weight")

        unmatched_item = set(expected_dist.items()) ^ set(dist.items())
        self.assertEqual(len(unmatched_item), 0)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])

    def test_s_shortest_path__multigraph(self):
        G = GraphGenerator.random_weighted_dag(100, 0.03, 50)
        G = nx.MultiDiGraph(G)
        nodes = set(nx.nodes(G))

        source = random.choice(nx.nodes(G))

        (dist, pred) = DAGraph.s_shortest_path(G, source)
        expected_dist = nx.shortest_path_length(G, source=source, target=None, weight="weight")
        expected_pred = nx.shortest_path(G, source=source, target=None, weight="weight")

        unmatched_item = set(expected_dist.items()) ^ set(dist.items())
        self.assertEqual(len(unmatched_item), 0)

        for node in nodes:
            if node in dist:
                self.assertEqual(dist[node], expected_dist[node])
            if node in pred:
                self.assertEqual(pred[node], expected_pred[node][-2])


class TestSPGraph(unittest.TestCase):

    def test_shortest_path(self):
        G = GraphGenerator.random_weighted_spg(200, 50)
        nodes = set(G.nodes())

        sources = random.sample(nodes, 5)
        targets = random.sample(nodes, 5)

        pairs = zip(sources, targets)

        for pair in pairs:
            source = pair[0]
            target = pair[1]

            expected_dist = 0
            expected_path = []
            expected_error = 0
            try:
                expected_dist = nx.shortest_path_length(G, source, target, weight="weight")
                expected_path = nx.shortest_path(G, source, target, weight="weight")
            except nx.NetworkXNoPath:
                expected_error = 1

            dist = 0
            path = []
            error = 0
            try:
                (dist, path) = (dist, path) = SPGraph.st_shortest_path(G, source, target)
            except nx.NetworkXNoPath:
                error = 1

            self.assertEqual(dist, expected_dist)
            self.assertEqual(path, expected_path)
            self.assertEqual(error, expected_error)

    def test_st_shortest_path__source_is_target(self):
        G = GraphGenerator.random_weighted_spg(100, 50)
        source = random.choice(G.nodes())
        target = source

        expected_dist = 0
        expected_path = [source]

        (dist, path) = SPGraph.st_shortest_path(G, source, target)

        self.assertEqual(dist, expected_dist)
        self.assertEqual(path, expected_path)