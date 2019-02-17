import networkx as nx
import time
from automaton import Automaton
from shortestpath import Dijkstra
from FAdo.cfg import *
from binheap import BinHeap
from grammarhelper import GrammarHelper
from graph import GraphHelper


class REGLanguage:

    @staticmethod
    def st_reg_shortest_path__product_nfa(G, source, target, regex_str, timeit=False):
        """Compute regular language constrained shortest path from source to target in the graph.
        Parameters:
        G : NetworkX graph
        source : node (Starting node for path)
        target : node (Ending node for path)
        regex_str : string (String that specifies regular expression/language)
        timeit : bool, optional (default = False; If True running time is returned)

        Returns:
        dist : int (The length of the shortest path)
        path : list (A list of nodes in the shortest path)
        times : dictionary (A dictionary where running times are stored)"""

        if source == target:
            if not timeit:
                return 0, [source]
            else:
                times = dict()
                times['graph_to_nfa'] = 0.0
                times['regex_to_nfa'] = 0.0
                times['product_nfa'] = 0.0
                times['calculate_path'] = 0.0
                return 0, [source], times

        t1 = time.clock()
        MG = Automaton.graph_to_automaton(G, [source], [target])
        t2 = time.clock()
        MR = Automaton.regex_to_automaton(regex_str)
        t3 = time.clock()
        MP = Automaton.product_automaton(MG, MR)
        t4 = time.clock()

        (GP, sourcesP, targetsP) = Automaton.automaton_to_graph(MP)

        GP = nx.convert_node_labels_to_integers(GP, label_attribute='old')
        sourcesP = [node for node in GP if GP.node[node]['old'] in sourcesP]
        targetsP = [node for node in GP if GP.node[node]['old'] in targetsP]

        for u, v, d in GP.edges(data=True):
            u0 = GP.node[u]['old'][0]
            v0 = GP.node[v]['old'][0]
            if G.has_edge(u0, v0):
                GP.add_edge(u, v, {'weight': G[u0][v0]['weight'], 'label': d['label']})

        path_found = 0
        path = []
        dist = float('inf')

        t5 = time.clock()
        sourceP = sourcesP[0]
        for targetP in targetsP:
            try:
                (current_dist, current_path) = Dijkstra.st_shortest_path_heap(GP, sourceP, targetP)
                path_found = 1
                if current_dist < dist:
                    dist = current_dist
                    path = current_path[:]
            except nx.NetworkXNoPath:
                pass
        t6 = time.clock()

        if path_found:
            times = dict()
            times['graph_to_nfa'] = t2 - t1
            times['regex_to_nfa'] = t3 - t2
            times['product_nfa'] = t4 - t3
            times['calculate_path'] = t6- t5
            path = [GP.node[node]['old'][0] for node in path]
            if not timeit:
                return dist, path
            else:
                return dist, path, times
        else:
            raise nx.NetworkXNoPath("No path between %s and %s." % (source, target))

    @staticmethod
    def st_reg_shortest_path(G, source, target, regex_str, timeit=False):
        """Compute regular language constrained shortest path from source to target in the graph.
        Parameters:
        G : NetworkX graph
        source : node (Starting node for path)
        target : node (Ending node for path)
        regex_str : string (String that specifies regular expression/language)
        timeit : bool, optional (default = False; If True running time is returned)

        Returns:
        dist : int (The length of the shortest path)
        path : list (A list of nodes in the shortest path)
        times : dictionary (A dictionary where running times are stored)"""

        if source == target:
            if not timeit:
                return 0, [source]
            else:
                times = dict()
                times['regex_to_nfa'] = 0.0
                times['setup_pointers'] = 0.0
                times['calculate_path'] = 0.0
                return 0, [source], times

        t1 = time.clock()
        MR = Automaton.regex_to_automaton(regex_str)
        (R, sourceR, targetsR) = Automaton.automaton_to_graph(MR)
        t2 = time.clock()

        nodesG = set(nx.nodes(G))
        nodesR = set(nx.nodes(R))

        sourceP = (source, sourceR)
        targetsP = [(target, targetR) for targetR in targetsR]

        pairs = set([(x, y) for x in nodesG for y in nodesR])

        t3 = time.clock()
        outgoing_edgesG = dict()
        for node in G.nodes():
            outgoing_edgesG[node] = dict()
            for successor in G.successors(node):
                symbol = G[node][successor]['label']
                if symbol not in outgoing_edgesG[node]:
                    outgoing_edgesG[node][symbol] = set()
                outgoing_edgesG[node][symbol].add(successor)

        outgoing_edgesR = dict()
        for node in R.nodes():
            outgoing_edgesR[node] = dict()
            for successor in R.successors(node):
                symbol = R[node][successor]['label']
                if symbol not in outgoing_edgesR[node]:
                    outgoing_edgesR[node][symbol] = set()
                outgoing_edgesR[node][symbol].add(successor)
        t4 = time.clock()

        path_found = 0
        path = []
        dist = float('inf')
        for targetP in targetsP:
            nodes = set(pairs)
            heap = BinHeap()
            heap.insert(sourceP, 0)
            pred = dict()

            while heap.currentSize > 0:
                min_node = heap.extractMin()
                if min_node == targetP:
                    path_found = 1
                    way = []
                    node = targetP
                    while True:
                        way[:0] = [node[0]]
                        if node == sourceP:
                            break
                        node = pred[node]
                    current_dist = heap.key[targetP]
                    current_path = way[:]
                    break

                nodes.remove(min_node)
                current_weight = heap.key[min_node]

                labelsG = outgoing_edgesG[min_node[0]]
                labelsR = outgoing_edgesR[min_node[1]]
                labels_of_interest = filter((lambda x: x in labelsG), labelsR.keys())

                for symbol in labels_of_interest:
                    successors = [(x, y) for x in labelsG[symbol] for y in labelsR[symbol]]
                    for node in successors:
                        weight = current_weight + G[min_node[0]][node[0]]['weight']
                        if node not in heap.key:
                            heap.insert(node, weight)
                            pred[node] = min_node
                        elif weight < heap.key[node]:
                            heap.decreaseKey(node, weight)
                            pred[node] = min_node

            if path_found and current_dist < dist:
                dist = current_dist
                path = current_path[:]
        t5 = time.clock()

        if path_found:
            if not timeit:
                return dist, path
            else:
                times = dict()
                times['regex_to_nfa'] = t2 - t1
                times['setup_pointers'] = t4 - t3
                times['calculate_path'] = t5 - t4
                return dist, path, times
        else:
            raise nx.NetworkXNoPath("No path between %s and %s." % (source, target))


class CFLanguage:

    @staticmethod
    def initialize_matrix(G, grammar):
        """Initializes table D for cfl-constrained all-pair shortest path algorithm.
        Parameters:
        G : NetworkX graph
        grammar: FAdo CNF (grammar in Chomskey Normal From)

        Returns:
        D : dictionary (Table with initial distance values)"""

        nodes = set(G.nodes())

        grammar.makenonterminals()
        nonterminals = grammar.Nonterminals
        grammar.nonterminalrules()

        D = dict()
        for u in nodes:
            D[u] = dict()
            for v in nodes:
                D[u][v] = dict()
                for A in nonterminals:
                    D[u][v][A] = float('inf')

        start = grammar.Start
        epsilon = common.Epsilon
        if (start, [epsilon]) in grammar.Rules or (start, epsilon) in grammar.Rules:
            for v in nodes:
                D[v][v][start] = 0

        derivatives = dict()
        for A in nonterminals:
            derivatives[A] = GrammarHelper.get_derivatives_of(grammar, A)

        for u, v, data in G.edges(data=True):
            a = data['label']
            for A in nonterminals:
                if a in derivatives[A]:
                    D[u][v][A] = data['weight']

        return D

    @staticmethod
    def all_pair_cfg_shortest_path(G, grammar):
        """Compute context-free language constrained all-pair shortest paths in the graph.
        Parameters:
        G : NetworkX graph
        grammar: FAdo CNF (grammar in Chomskey Normal From)

        Returns:
        D : dictionary (Table with all-pair shortest-path distances)"""

        D = CFLanguage.initialize_matrix(G, grammar)

        nonterminals = grammar.Nonterminals

        n_nonterminals = len(nonterminals)
        n_nodes = G.number_of_nodes()

        nodes = set(G.nodes())

        derivatives = dict()
        for A in nonterminals:
            derivatives[A] = GrammarHelper.get_derivatives_of(grammar, A)

        for i in range(n_nodes*n_nodes*n_nonterminals):
            for u in nodes:
                for v in nodes:
                    for A in nonterminals:
                        values = set()
                        if D[u][v][A] < float('inf'):
                            values.add(D[u][v][A])
                        value_found = 0

                        for derivative in derivatives[A]:
                            if len(derivative) == 2:
                                B = derivative[0]
                                C = derivative[1]

                                for k in nodes:
                                    if D[u][k][B] < float('inf') and D[k][v][C] < float('inf'):
                                        value_found = 1
                                        values.add(D[u][k][B] + D[k][v][C])
                        if value_found:
                            D[u][v][A] = min(values)

        return D


class KSimilarPath:

    @staticmethod
    def st_k_similar_path(G, source, target, k, timeit=False):
        """Compute k-similar path from source to target in the graph.
        Parameters:
        G : NetworkX graph
        source : node (Starting node for paths)
        target : node (Ending node for paths)
        k : int (number of common edges allowed)

        Returns:
        dist : int (The length of the shortest path)
        distk : int (The length of the k-similar path)
        path : list (A list of nodes in the shortest path)
        pathk : list (A list of nodes in the k-similar path)"""

        try:
            t1 = time.clock()
            (dist, path) = Dijkstra.st_shortest_path_heap(G, source, target)
            t2 = time.clock()
            time_sp = t2-t1
        except nx.NetworkXNoPath:
            raise nx.NetworkXNoPath("No path between %s and %s." % (source, target))

        t3 = time.clock()
        pathlist = set(GraphHelper.get_edgelist_from_nodelist(path))

        for u, v, data in G.edges(data=True):
            if (u, v) in pathlist:
                G[u][v]['label'] = 't'
            else:
                G[u][v]['label'] = 'f'

        regex_helper = 'f*'
        regex_str = 'f*'
        for i in range(k):
            regex_helper += 'tf*'
            regex_str += '+' + regex_helper
        t4 = time.clock()

        try:
            t5 = time.clock()
            (distk, pathk) = REGLanguage.st_reg_shortest_path(G, source, target, regex_str)
            t6 = time.clock()
        except nx.NetworkXNoPath:
            raise nx.NetworkXNoPath("No k similar path between %s and %s." % (source, target))

        if timeit:
            times = dict()
            times['ShP'] = time_sp
            times['Labels'] = t4 - t3
            times['KSimP'] = t6 - t5
            return dist, distk, path, pathk, times
        else:
            return dist, distk, path, pathk
