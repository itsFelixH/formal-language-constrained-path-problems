import unittest
import networkx as nx
from graph import GraphGenerator, GraphHelper
from FAdo.reex import *
from FAdo.cfg import *
from constrainedpath import REGLanguage, CFLanguage, KSimilarPath


class TestREGLanguage(unittest.TestCase):

    def test_st_shortest_path_product_automaton(self):
        while True:
            G = GraphGenerator.random_weighted_graph(40, 0.1, 50)
            sigma = ['a', 'b']
            G = GraphGenerator.random_label(G, sigma)
            string = "(a+ab)*"

            try:
                source = random.choice(G.nodes())
                target = random.choice(G.nodes())

                (dist, path) = REGLanguage.st_reg_shortest_path__product_nfa(G, source, target, string)

                self.assertEqual(path[0], source)
                self.assertEqual(path[-1], target)

                for node in path:
                    self.assertTrue(node in G)

                expected_dist = 0
                word = []
                for u,v in zip(path[:-1],path[1:]):
                    self.assertTrue(G.has_edge(u,v))
                    expected_dist += G[u][v]['weight']
                    word += G[u][v]['label']
                self.assertEqual(dist, expected_dist)
                self.assertTrue(str2regexp(string).evalWordP(word))
                self.assertTrue(dist >= nx.shortest_path_length(G, source, target, weight="weight"))

            except nx.NetworkXNoPath:
                continue
            break


    def test_st_shortest_path_product_automaton__other(self):
        while True:
            sigma = ['a', 'b', 'c', 'd', 'e']
            (G, dic) = GraphGenerator.random_weighted_labeled_grid(50, 50, 50, sigma)
            (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)
            string = 'a*((b+cd)*+e)'

            try:
                source = random.choice(G.nodes())
                target = random.choice(G.nodes())

                (dist, path) = REGLanguage.st_reg_shortest_path__product_nfa(G, source, target, string)

                self.assertEqual(path[0], source)
                self.assertEqual(path[-1], target)

                for node in path:
                    self.assertTrue(node in G)

                expected_dist = 0
                word = []
                for u, v in zip(path[:-1], path[1:]):
                    self.assertTrue(G.has_edge(u, v))
                    expected_dist += G[u][v]['weight']
                    word += G[u][v]['label']
                self.assertEqual(dist, expected_dist)
                self.assertTrue(str2regexp(string).evalWordP(word))
                self.assertTrue(dist >= nx.shortest_path_length(G, source, target, weight="weight"))

            except nx.NetworkXNoPath:
                continue
            break


    def test_st_shortest_path_product_automaton__timeit(self):
        while True:
            G = GraphGenerator.random_weighted_graph(40, 0.1, 50)
            sigma = ['a', 'b']
            G = GraphGenerator.random_label(G, sigma)
            string = "(a+ab)*"

            try:
                source = random.choice(G.nodes())
                target = random.choice(G.nodes())

                (dist, path, times) = REGLanguage.st_reg_shortest_path__product_nfa(G, source, target, string, timeit=True)

                self.assertEqual(path[0], source)
                self.assertEqual(path[-1], target)

                for node in path:
                    self.assertTrue(node in G)

                expected_dist = 0
                word = []
                for u, v in zip(path[:-1], path[1:]):
                    self.assertTrue(G.has_edge(u, v))
                    expected_dist += G[u][v]['weight']
                    word += G[u][v]['label']
                self.assertEqual(dist, expected_dist)
                self.assertTrue(str2regexp(string).evalWordP(word))
                self.assertTrue(dist >= nx.shortest_path_length(G, source, target, weight="weight"))

                self.assertEqual(len(times), 4)
                for key in times:
                    self.assertTrue(isinstance(times[key], float))
                    self.assertTrue(times[key] >= 0)

            except nx.NetworkXNoPath:
                continue
            break

    def test_st_shortest_path(self):
        while True:
            G = GraphGenerator.random_weighted_graph(40, 0.1, 50)
            sigma = ['a', 'b']
            G = GraphGenerator.random_label(G, sigma)
            string = "(a+ab)*"

            try:
                source = random.choice(G.nodes())
                target = random.choice(G.nodes())

                (dist, path) = REGLanguage.st_reg_shortest_path(G, source, target, string)

                self.assertEqual(path[0], source)
                self.assertEqual(path[-1], target)

                for node in path:
                    self.assertTrue(node in G)

                expected_dist = 0
                word = []
                for u, v in zip(path[:-1], path[1:]):
                    self.assertTrue(G.has_edge(u, v))
                    expected_dist += G[u][v]['weight']
                    word += G[u][v]['label']
                self.assertEqual(dist, expected_dist)
                self.assertTrue(str2regexp(string).evalWordP(word))
                self.assertTrue(dist >= nx.shortest_path_length(G, source, target, weight="weight"))

            except nx.NetworkXNoPath:
                continue
            break

    def test_st_shortest_path__timeit(self):
        while True:
            G = GraphGenerator.random_weighted_graph(40, 0.1, 50)
            sigma = ['a', 'b']
            G = GraphGenerator.random_label(G, sigma)
            string = "(a+ab)*"

            try:
                source = random.choice(G.nodes())
                target = random.choice(G.nodes())

                (dist, path, times) = REGLanguage.st_reg_shortest_path(G, source, target, string, timeit=True)

                self.assertEqual(path[0], source)
                self.assertEqual(path[-1], target)

                for node in path:
                    self.assertTrue(node in G)

                expected_dist = 0
                word = []
                for u, v in zip(path[:-1], path[1:]):
                    self.assertTrue(G.has_edge(u, v))
                    expected_dist += G[u][v]['weight']
                    word += G[u][v]['label']
                self.assertEqual(dist, expected_dist)
                self.assertTrue(str2regexp(string).evalWordP(word))
                self.assertTrue(dist >= nx.shortest_path_length(G, source, target, weight="weight"))

                self.assertEqual(len(times), 3)
                for key in times:
                    self.assertTrue(isinstance(times[key], float))
                    self.assertTrue(times[key] >= 0)

            except nx.NetworkXNoPath:
                continue
            break

    def test_compare_algorithms(self):
        while True:
            G = GraphGenerator.random_weighted_graph(100, 0.1, 50)
            sigma = ['a', 'b']
            G = GraphGenerator.random_label(G, sigma)
            string = "(a+ab)*"

            try:
                source = random.choice(G.nodes())
                target = random.choice(G.nodes())

                (dist, path) = REGLanguage.st_reg_shortest_path__product_nfa(G, source, target, string)
                (dist2, path2) = REGLanguage.st_reg_shortest_path(G, source, target, string)

                word = ''
                for u, v in zip(path[:-1], path[1:]):
                    word += str(G[u][v]['label'])

                word2 = ''
                for u, v in zip(path2[:-1], path2[1:]):
                    word2 += str(G[u][v]['label'])

                self.assertEqual(dist, dist2)
                self.assertEqual(path, path2)
                self.assertEqual(word, word2)

            except nx.NetworkXNoPath:
                continue
            break


class TestCFLanguage(unittest.TestCase):

    def test_initialize_matrix(self):
        productions2 = [('S', ('S', 'S')), ('S', ('a', 'S', 'b')), ('S', ('c'))]
        grammar = CNF(productions2)

        grammar.makenonterminals()
        nonterminals = grammar.Nonterminals
        grammar.maketerminals()
        terminals = grammar.Terminals
        grammar.terminalrules()
        tr = grammar.tr
        rules = grammar.Rules

        (G, dic) = GraphGenerator.random_weighted_labeled_grid(20, 20, 50, list(terminals))

        D = CFLanguage.initialize_matrix(G, grammar)

        for u in D:
            for v in D[u]:
                for A in D[u][v]:
                    self.assertTrue(A in nonterminals)
                    if D[u][v][A] < float('inf'):
                        self.assertEqual(D[u][v][A], G[u][v]['weight'])
                        a = G[u][v]['label']
                        R = []
                        for i in tr[a]:
                            R.append(rules[i][0])
                        self.assertTrue(A in R)


    def test_all_pair_shortest_path(self):
        productions = [('S', ('S', 'S')), ('S', ('a', 'S', 'b')), ('S', ('c'))]
        grammar = CNF(productions)

        grammar.makenonterminals()
        grammar.maketerminals()
        terminals = grammar.Terminals
        grammar.terminalrules()

        (G, dic) = GraphGenerator.random_weighted_labeled_grid(5, 5, 50, list(terminals))

        D = CFLanguage.all_pair_cfg_shortest_path(G, grammar)

        for u in D:
            for v in D[u]:
                for A in D[u][v]:
                    if D[u][v][A] < float('inf'):
                        self.assertTrue(nx.has_path(G,u,v))

    def test_all_pair_shortest_path___reg_grammar(self):
        productions = [('S', ('a', 'S')), ('S', ('S', 'b')), ('S', common.Epsilon)]
        grammar = CNF(productions)

        grammar.makenonterminals()
        grammar.maketerminals()
        terminals = grammar.Terminals
        grammar.terminalrules()

        (G, dic) = GraphGenerator.random_weighted_labeled_grid(5, 5, 50, list(terminals))

        D = CFLanguage.all_pair_cfg_shortest_path(G, grammar)

        for u in D:
            for v in D[u]:
                for A in D[u][v]:
                    if D[u][v][A] < float('inf'):
                        self.assertTrue(nx.has_path(G, u, v))


class TestKSimilarPath(unittest.TestCase):

    def test_st_k_similar_path(self):
        G = GraphGenerator.random_weighted_graph(100, 0.03, 50)
        nodes = nx.nodes(G)

        dist = 0
        distk = 0
        path = []
        pathk = []
        while True:
            source = random.choice(nodes)
            target = random.choice(nodes)
            k = random.randint(2, 12)
            try:
                (dist, distk, path, pathk) =  KSimilarPath.st_k_similar_path(G, source, target, k)
            except nx.NetworkXNoPath:
                continue
            break

        pathlist = GraphHelper.get_edgelist_from_nodelist(path)
        pathlistk = GraphHelper.get_edgelist_from_nodelist(pathk)
        word = GraphHelper.get_lables_from_nodelist(G, path)
        wordk = GraphHelper.get_lables_from_nodelist(G, pathk)

        common_edges = 0
        taken_edges = 0
        for edge in pathlistk:
            if edge in pathlist:
                common_edges += 1

        self.assertTrue(common_edges <= k)
        self.assertTrue(dist <= distk)

        for c in word:
            self.assertEqual(c, 't')
        for c in wordk:
            self.assertTrue(c in {'f', 't'})
            if c == 't':
                taken_edges += 1

        self.assertTrue(taken_edges <= k)
        self.assertEqual(taken_edges, common_edges)


