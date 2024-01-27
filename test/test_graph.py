import networkx as nx
import numpy as np
import unittest
import random
import math
from graph import GraphGenerator, GraphHelper


class TestGraphGenerator(unittest.TestCase):

    def test_random_weighted_graph(self):
        G = GraphGenerator.random_weighted_graph(100, 0.1, 50)

        self.assertEqual(G.number_of_nodes(), 100)
        self.assertIsNotNone(G.nodes())
        self.assertIsNotNone(G.edges())

        for u,v,d in G.edges(data=True):
            self.assertIsNotNone(d['weight'])
            self.assertTrue(isinstance(d['weight'], int))
            self.assertTrue(d['weight'] <= 50)

    def test_random_weighted_dag(self):
        G = GraphGenerator.random_weighted_dag(100, 0.1, 50)

        self.assertTrue(nx.is_directed(G))
        self.assertTrue(nx.is_directed_acyclic_graph(G))

        self.assertEqual(G.number_of_nodes(), 100)
        self.assertIsNotNone(G.nodes())
        self.assertIsNotNone(G.edges())

        for u, v, d in G.edges(data=True):
            self.assertIsNotNone(d['weight'])
            self.assertTrue(isinstance(d['weight'], int))
            self.assertTrue(d['weight'] <= 50)

    def test_random_weighted_spg(self):
        G = GraphGenerator.random_weighted_spg(100, 50)

        self.assertEqual(G.number_of_edges(), 100)
        self.assertIsNotNone(G.nodes())
        self.assertIsNotNone(G.edges())

        self.assertTrue(nx.is_directed(G))
        self.assertTrue(nx.is_directed_acyclic_graph(G))

        for u, v, d in G.edges(data=True):
            self.assertIsNotNone(d['weight'])
            self.assertTrue(isinstance(d['weight'], int))
            self.assertTrue(d['weight'] <= 50)

    def test_random_weighted_grid(self):
        sigma = ['a','b']
        (G, dic) = GraphGenerator.random_weighted_labeled_grid(50, 50, 50, sigma)

        self.assertEqual(G.number_of_nodes(), 2500)
        self.assertEqual(G.number_of_edges(), 9800)
        self.assertIsNotNone(G.nodes())
        self.assertIsNotNone(G.edges())

        self.assertTrue(nx.is_directed(G))

        for u, v, d in G.edges(data=True):
            self.assertIsNotNone(d['weight'])
            self.assertIsNotNone(d['label'])
            self.assertTrue(isinstance(d['weight'], int))
            self.assertTrue(d['weight'] <= 50)
            self.assertTrue(d['label'] in sigma)
            self.assertIsNotNone(G[v][u])
            self.assertEqual(d['weight'], G[v][u]['weight'])
            self.assertEqual(d['label'], G[v][u]['label'])

    def test_random_road_network(self):
        sigma = ['a', 'b']
        (G, dic) = GraphGenerator.random_road_network(50, 50, 50, sigma)

        self.assertIsNotNone(G.nodes())
        self.assertIsNotNone(G.edges())

        self.assertTrue(nx.is_directed(G))

        for u, v, d in G.edges(data=True):
            self.assertIsNotNone(d['weight'])
            self.assertIsNotNone(d['label'])
            self.assertTrue(isinstance(d['weight'], int))
            self.assertTrue(d['weight'] <= 50)
            self.assertTrue(d['label'] in sigma)

    def test_random_label(self):
        G = GraphGenerator.random_weighted_graph(100, 0.1, 50)
        sigma = ['a', 'b']
        GraphGenerator.random_label(G, sigma)

        for u, v, d in G.edges(data=True):
            self.assertIsNotNone(d['label'])
            self.assertTrue(d['label'] in sigma)

    def test_random_label__empty_alphabet(self):
        G = GraphGenerator.random_weighted_graph(100, 0.1, 50)
        sigma = []
        GraphGenerator.random_label(G, sigma)

        for u, v, d in G.edges(data=True):
            self.assertFalse('label' in d)

    def test_random_label__no_alphabet(self):
        G = GraphGenerator.random_weighted_graph(100, 0.1, 50)
        GraphGenerator.random_label(G)

        for u, v, d in G.edges(data=True):
            self.assertFalse('label' in d)

    def test_change_label(self):
        G = GraphGenerator.random_weighted_graph(100, 0.1, 50)
        sigma = ['a', 'b', 'c', 'd']
        GraphGenerator.random_label(G, sigma)

        for u, v, d in G.edges(data=True):
            self.assertIsNotNone(d['label'])
            self.assertTrue(d['label'] in sigma)

        sigma2 = [0, 1]
        GraphGenerator.random_label(G, sigma2)

        for u, v, d in G.edges(data=True):
            self.assertIsNotNone(d['label'])
            self.assertTrue(d['label'] in sigma2)


class TestGraphHelper(unittest.TestCase):

    def test_get_all_nodes_in_rectangle(self):
        sigma = ['a', 'b']
        (G, dic) = GraphGenerator.random_weighted_labeled_grid(30, 30, 50, sigma)

        x1 = 10
        y1 = 5
        x2 = 20
        y2 = 17
        L = GraphHelper.get_all_nodes_in_rectangle(dic, x1, x2, y1, y2)

        for node in G.nodes():
            if node in L:
                self.assertTrue((x1 <= dic[node][0] <= x2))
                self.assertTrue((y1 <= dic[node][1] <= y2))
            else:
                self.assertTrue(
                    (x1 > dic[node][0]) or (dic[node][0] > x2) or (y1 > dic[node][1]) or (dic[node][1] > y2))

    def test_get_all_nodes_in_rectangle__reverse_order(self):
        sigma = ['a', 'b']
        (G, dic) = GraphGenerator.random_weighted_labeled_grid(30, 30, 50, sigma)

        x1 = 22
        y1 = 19
        x2 = 8
        y2 = 13
        L = GraphHelper.get_all_nodes_in_rectangle(dic, x1, x2, y1, y2)

        for node in G.nodes():
            if node in L:
                self.assertTrue((x2 <= dic[node][0] <= x1))
                self.assertTrue((y2 <= dic[node][1] <= y1))
            else:
                self.assertTrue(
                    (x2 > dic[node][0]) or (dic[node][0] > x1) or (y2 > dic[node][1]) or (dic[node][1] > y1))

    def test_get_rectangle_around_s_and_t(self):
        sigma = ['a', 'b']
        (G, dic) = GraphGenerator.random_weighted_labeled_grid(30, 30, 50, sigma)
        source = 0
        target = 0
        path = []
        while True:
            source = random.choice(G.nodes())
            target = random.choice(G.nodes())
            try:
                path = nx.shortest_path(G, source, target, weight='weight')
            except nx.NetworkXNoPath:
                continue
            break

        L = GraphHelper.get_rectangle_around_s_and_t(dic, source, target, path)

        self.assertTrue(source in L)
        self.assertTrue(target in L)
        for node in G.nodes():
            if node in path:
                self.assertTrue(node in L)


    def test_make_graph_geometric(self):
        sigma = ['a', 'b']
        (G, dic) = GraphGenerator.random_weighted_labeled_grid(30, 30, 50, sigma)
        G = GraphHelper.make_graph_geometric(G, dic)

        for u, v, d in G.edges(data=True):
            geometric_dist = math.sqrt(((dic[u][0] - dic[v][0]) ** 2) + (dic[u][1] - dic[v][1]) ** 2)
            self.assertTrue(d['weight'] >= geometric_dist)
            self.assertTrue(d['weight'] <= geometric_dist + 1)

    def test_merge_nodes(self):
        G1 = nx.Graph()
        G1.add_edge(1, 2)

        G2 = nx.Graph()
        G2.add_edge(3, 4)

        G = nx.union(G1, G2)

        self.assertEqual(G.number_of_nodes(), 4)
        self.assertEqual(G.number_of_edges(), 2)

        G = GraphHelper.merge_nodes(G, [2, 3], 'merged')

        self.assertEqual(G.number_of_nodes(), 3)
        self.assertEqual(G.number_of_edges(), 2)
        self.assertTrue(G.has_node('merged'))
        self.assertFalse(G.has_node(2))
        self.assertFalse(G.has_node(3))

    def test_merge_nodes__multigraph(self):
        G = nx.MultiDiGraph()
        G.add_edges_from([(1, 2), (3, 4), (1, 3), (2, 5)])
        G.add_edge(1, 2)

        self.assertEqual(G.number_of_nodes(), 5)
        self.assertEqual(G.number_of_edges(), 5)

        G = GraphHelper.merge_nodes(G, [2, 3], 'merged')

        self.assertEqual(G.number_of_nodes(), 4)
        self.assertEqual(G.number_of_edges(), 5)
        self.assertTrue(G.has_node('merged'))
        self.assertFalse(G.has_node(2))
        self.assertFalse(G.has_node(3))

    def test_merge_nodes__attributes(self):
        sigma = ['a','b']
        (G_old, dic) = GraphGenerator.random_weighted_labeled_grid(50, 50, 50, sigma)
        G = G_old.copy()

        selected_nodes = random.sample(G.nodes(), np.random.randint(2, G.number_of_nodes() / 2))

        G = GraphHelper.merge_nodes(G, selected_nodes, 'merged')

        self.assertEqual(G.number_of_nodes(), 2500 - len(selected_nodes) + 1)
        self.assertTrue(G.has_node('merged'))

        for node in selected_nodes:
            self.assertFalse(G.has_node(node))
            for successor in G_old.successors(node):
                if G.has_node(successor):
                    self.assertTrue(G.has_edge('merged', successor))
                    weights = []
                    for edge in G['merged'][successor]:
                        weights.append(G['merged'][successor][edge]['weight'])
                    self.assertTrue(G_old[node][successor]['weight'] in weights)
            for predecessor in G_old.predecessors(node):
                if G.has_node(predecessor):
                    self.assertTrue(G.has_edge(predecessor, 'merged'))
                    weights = []
                    for edge in G[predecessor]['merged']:
                        weights.append(G[predecessor]['merged'][edge]['weight'])
                    self.assertTrue(G_old[predecessor][node]['weight'] in weights)

    def test_merge_nodes__random(self):
        G_old = GraphGenerator.random_weighted_graph(100, 0.1, 50)
        G = G_old.copy()

        selected_nodes = random.sample(G.nodes(), np.random.randint(2, G.number_of_nodes() / 2))
        successors = dict()
        for node in selected_nodes:
            successors[node] = G.successors(node)
        G = GraphHelper.merge_nodes(G, selected_nodes, 'merged')

        self.assertEqual(G.number_of_nodes(), 100 - len(selected_nodes) + 1)
        self.assertTrue(G.has_node('merged'))

        for node in selected_nodes:
            self.assertFalse(G.has_node(node))
            for successor in G_old.successors(node):
                if G.has_node(successor):
                    self.assertTrue(G.has_edge('merged', successor))
                    weights = []
                    for edge in G['merged'][successor]:
                        weights.append(G['merged'][successor][edge]['weight'])
                    self.assertTrue(G_old[node][successor]['weight'] in weights)
            for predecessor in G_old.predecessors(node):
                if G.has_node(predecessor):
                    self.assertTrue(G.has_edge(predecessor, 'merged'))
                    weights = []
                    for edge in G[predecessor]['merged']:
                        weights.append(G[predecessor]['merged'][edge]['weight'])
                    self.assertTrue(G_old[predecessor][node]['weight'] in weights)

    def test_get_edgelist_from_nodelist(self):
        path = random.sample(xrange(500), random.randint(20,250))

        edgelist = GraphHelper.get_edgelist_from_nodelist(path)

        for u, v in edgelist:
            self.assertTrue(u in path)
            self.assertTrue(v in path)
            self.assertEqual(path[path.index(u) + 1], v)

    def test_get_nodelist_from_edgelist(self):
        path = random.sample(xrange(500), random.randint(20, 250))
        edgelist = GraphHelper.get_edgelist_from_nodelist(path)

        nodelist = GraphHelper.get_nodelist_from_edgelist(edgelist)

        self.assertEqual(nodelist, path)

    def test_get_labels_from_nodelist(self):
        G = nx.Graph()
        G.add_nodes_from(range(1,10))
        G.add_edge(1, 2, {'label': 't'})
        G.add_edge(2, 4, {'label': 'e'})
        G.add_edge(4, 8, {'label': 's'})
        G.add_edge(8, 10, {'label': 't'})

        word1 = GraphHelper.get_lables_from_nodelist(G, [1, 2, 4, 8, 10])
        word2 = GraphHelper.get_lables_from_nodelist(G, [2, 4, 8, 10])
        word3 = GraphHelper.get_lables_from_nodelist(G, [1, 2, 4])

        self.assertEqual(word1, 'test')
        self.assertEqual(word2, 'est')
        self.assertEqual(word3, 'te')

    def test_convert_node_labels_to_integers(self):
        sigma = ['a', 'b']
        (G_old, dic_old) = GraphGenerator.random_weighted_labeled_grid(20, 20, 50, sigma)

        (G, dic) = GraphHelper.convert_node_labels_to_integers(G_old, dic_old)

        self.assertEqual(len(dic), len(dic_old))
        self.assertEqual(G.number_of_nodes(), G_old.number_of_nodes())

        for node, data in G.nodes(data=True):
            self.assertTrue(isinstance(node, int))
            self.assertTrue(dic[node] in dic_old.values())
            self.assertFalse('old' in data)

        for node, data in G_old.nodes(data=True):
            self.assertTrue(dic_old[node] in dic.values())