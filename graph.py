import networkx as nx
import random
import math


class GraphGenerator:

    @staticmethod
    def random_weighted_graph(number_of_nodes, p, max_weight):
        """Generates random weighted directed graph.
        Parameters:
        number_of_nodes: int (number of nodes in the graph)
        p : float (probability for edges in the graph)
        max_weight : int (maximum weight for edges)

        Returns:
        G : NetworkX graph"""

        G = nx.gnp_random_graph(number_of_nodes, p, directed=True)
        for (u,v) in G.edges():
            G[u][v]['weight'] = random.randint(1, max_weight)
        return G


    @staticmethod
    def random_weighted_dag(number_of_nodes, p, max_weight):
        """Generates random weighted directed acyclic graph.
        Parameters:
        number_of_nodes: int (number of nodes in the graph)
        p : float (probability for edges in the graph)
        max_weight : int (maximum weight for edges)

        Returns:
        DAG : NetworkX graph"""

        G = nx.gnp_random_graph(number_of_nodes, p, directed=True)
        DAG = nx.DiGraph([(u, v, {'weight': random.randint(1, max_weight)}) for (u, v) in G.edges() if u < v])
        return DAG


    @staticmethod
    def random_weighted_spg(number_of_edges, max_weight):
        """Generates random weighted directed acyclic graph.
        Parameters:
        number_of_edges: int (number of edges in the graph)
        max_weight : int (maximum weight for edges)

        Returns:
        SPG : NetworkX graph"""

        sp_list = dict()
        source = dict()
        sink = dict()
        for i in range(0, number_of_edges):
            sp_list[i] = nx.MultiDiGraph()
            sp_list[i].add_edge(str(i)+'_1', str(i)+'_2', weight = random.randint(1, max_weight))
            source[i] = str(i)+'_1'
            sink[i] = str(i)+'_2'
        k = 0
        while len(sp_list) > 1:
            key1 = random.choice(list(sp_list.keys()))
            G1 = sp_list[key1]
            del sp_list[key1]
            key2 = random.choice(list(sp_list.keys()))
            G2 = sp_list[key2]
            G = nx.union(G1, G2)
            if random.random() < 0.5:
                combine = [sink[key1], source[key2]]
                G = GraphHelper.merge_nodes(G, combine, 's_' + str(k))
                source[key2] = source[key1]
            else:
                combine1 = [source[key1], source[key2]]
                combine2 = [sink[key1], sink[key2]]
                G = GraphHelper.merge_nodes(G, combine1, 'p1_' + str(k))
                G = GraphHelper.merge_nodes(G, combine2, 'p2_' + str(k))
                source[key2] = 'p1_' + str(k)
                sink[key2] = 'p2_' + str(k)

            sp_list[key2] = G
            del source[key1]
            del sink[key1]
            k += 1
        key = sp_list.keys()[0]
        SPG = sp_list[key]
        SPG = nx.convert_node_labels_to_integers(SPG)
        return SPG


    @staticmethod
    def random_weighted_labeled_grid(m, n, max_weight, sigma=None):
        """Generates random weighted labeled grid graph.
        Parameters:
        m: int (number of rows of the grid)
        n: int (number of columns of the grid)
        max_weight : int (maximum weight for edges)
        sigma : list, optional (alphabet for labels)

        Returns:
        G : NetworkX graph
        dic: dictionary (positions of the nodes)"""

        G = nx.grid_2d_graph(m, n)
        for (u, v) in G.edges():
            G[u][v]['weight'] = random.randint(1, max_weight)
        G = GraphGenerator.random_label(G, sigma)
        G = G.to_directed()
        dic = dict(zip(G, G))
        return G, dic


    @staticmethod
    def random_road_network(m, n, max_weight, sigma):
        """Generates random weighted labeled road network.
        Parameters:
        m: int (number of rows of the grid)
        n: int (number of columns of the grid)
        max_weight : int (maximum weight for edges)
        sigma : list (alphabet for labels)

        Returns:
        G : NetworkX graph
        dic: dictionary (positions of the nodes)"""

        (G, dic) = GraphGenerator.random_weighted_labeled_grid(m, n, max_weight, sigma)
        if n > 3 and m > 3:
            for k in range(random.randint((min(m, n)/2), max(m, n))):
                x = random.randint(2, m-1)
                y = random.randint(2, n-1)
                node = (x, y)
                if random.random() > 0.5:
                    x2 = x + 1
                else:
                    x2 = x - 1
                if random.random() > 0.5:
                    y2 = y + 1
                else:
                    y2 = y - 1
                node2 = (x2, y2)
                G.add_edge(node, node2, {'weight': random.randint(1, max_weight), 'label': random.choice(sigma)})
        for node in G.nodes():
            if random.random() < 0.01:
                G.remove_node(node)
                dic.pop(node)
        for u, v in G.edges():
            if random.random() < 0.03:
                G.remove_edge(u, v)
        return G, dic


    @staticmethod
    def random_label(G, sigma=None):
        """Randomly labels edges on graph.
        Parameters:
        G : NetworkX graph
        sigma : list, optional (alphabet for labels)

        Returns:
        G : NetworkX graph"""

        if sigma:
            for (u, v) in G.edges():
                G[u][v]['label'] = random.choice(sigma)
        return G


class GraphHelper:

    @staticmethod
    def get_all_nodes_in_rectangle(dic, x1, x2, y1, y2):
        """Computes all nodes in specified rectangle.
        Parameters:
        dic: dictionary (positions of the nodes)
        x1, x2, y1, y2 : int (interval borders)

        Returns:
        L : list (list of nodes)"""

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        L = []
        for node in dic:
            if x1 <= dic[node][0] <= x2 and y1 <= dic[node][1] <= y2:
                L.append(node)
        return L

    @staticmethod
    def get_rectangle_around_s_and_t(dic, source, target, path=None):
        """Computes all nodes in rectangle around source and target.
        Parameters:
        dic: dictionary (positions of the nodes)
        source, target : node
        path : list, optional (default = None)

        Returns:
        L : list (list of nodes)"""

        x_source = dic[source][0]
        y_source = dic[source][1]
        x_target = dic[target][0]
        y_target = dic[target][1]
        if path:
            path_contained = 0
            L = []
            while not path_contained:
                path_contained = 1
                L = GraphHelper.get_all_nodes_in_rectangle(dic, x_source, x_target, y_source, y_target)
                for node in path:
                    if node not in L:
                        path_contained = 0
                        x_node = dic[node][0]
                        y_node = dic[node][1]
                        if x_node > x_source and x_node > x_target:
                            if x_source > x_target:
                                x_source = x_node
                            else:
                                x_target = x_node
                        if x_node < x_source and x_node < x_target:
                            if x_source < x_target:
                                x_source = x_node
                            else:
                                x_target = x_node
                        if y_node > y_source and y_node > y_target:
                            if y_source > y_target:
                                y_source = y_node
                            else:
                                y_target = y_node
                        if y_node < y_source and y_node < y_target:
                            if y_source < y_target:
                                y_source = y_node
                            else:
                                y_target = y_node
                        break
        else:
            L = GraphHelper.get_all_nodes_in_rectangle(dic, x_source, x_target, y_source, y_target)
        return L

    @staticmethod
    def make_graph_geometric(G, dic):
        """Computes geometric distance for edge weights.
        Parameters:
        G : NetworkX graph
        dic: dictionary (positions of the nodes)

        Returns:
        G : NetworkX graph"""

        for u, v, d in G.edges(data=True):
            geometric_dist = math.sqrt(((dic[u][0] - dic[v][0]) ** 2) + (dic[u][1] - dic[v][1]) ** 2)
            d['weight'] = int(math.ceil(geometric_dist))

        return G

    @staticmethod
    def merge_nodes(G, selected_nodes, new_node):
        """Merges selected_nodes into new_node.
        Parameters:
        G : NetworkX graph
        selected_nodes : list (nodes to merge)
        new_node : (node to merge to)

        Returns:
        G : NetworkX graph"""

        multigraph = 0
        if G.is_multigraph():
            multigraph = 1

        G.add_node(new_node)
        for u, v, data in G.edges(data=True):
            if multigraph:
                if u in selected_nodes:
                    G.add_edge(new_node, v, key=None, attr_dict=data)
                elif v in selected_nodes:
                    G.add_edge(u, new_node, key=None, attr_dict=data)
            else:
                if u in selected_nodes:
                    if not G.has_edge(new_node, v):
                        G.add_edge(new_node, v, data)
                    else:
                        multigraph = 1
                        H = nx.MultiDiGraph()
                        H.add_nodes_from(G.nodes())
                        H.add_edges_from(G.edges(data=True))
                        G = H
                        G.add_edge(new_node, v, key=None, attr_dict=data)
                elif v in selected_nodes:
                    if not G.has_edge(u, new_node):
                        G.add_edge(u, new_node, data)
                    else:
                        multigraph = 1
                        H = nx.MultiDiGraph()
                        H.add_nodes_from(G.nodes())
                        H.add_edges_from(G.edges(data=True))
                        G = H
                        G.add_edge(u, new_node, key=None, attr_dict=data)
        for node in selected_nodes:
            G.remove_node(node)

        return G


    @staticmethod
    def get_edgelist_from_nodelist(nodelist):
        """Computes edgelist from nodelist.
        Parameters:
        nodelist : list (list of connected nodes)

        Returns:
        edgelist : list (list of edges)"""

        edgelist = []
        for u, v in zip(nodelist[:-1], nodelist[1:]):
            edgelist.append((u, v))

        return edgelist


    @staticmethod
    def get_nodelist_from_edgelist(edgelist):
        """Computes nodelist from edgelist.
        Parameters:
        edgelist : list (list of adjacent edges)

        Returns:
        nodelist : list (list of nodes)"""

        nodelist = [edgelist[0][0]]
        for u, v in edgelist:
            nodelist.append(v)

        return nodelist


    @staticmethod
    def get_lables_from_nodelist(G, nodelist):
        """Computes labels of nodelist.
        Parameters:
        nodelist : list (list of connected nodes)

        Returns:
        word : str (concatenated labels of nodelist)"""

        edgelist = GraphHelper.get_edgelist_from_nodelist(nodelist)

        word = ''
        for u, v in edgelist:
            word += str(G[u][v]['label'])

        return word


    @staticmethod
    def convert_node_labels_to_integers(G, pos):
        """Converts node labels to integers.
        Parameters:
        G : NetworkX graph
        pos: dictionary (positions of the nodes)

        Returns:
        G : NetworkX graph
        new_pos: dictionary (positions of the nodes)"""

        G = nx.convert_node_labels_to_integers(G, label_attribute='old')

        new_pos = {}
        for node, data in G.nodes(data=True):
            new_pos[node] = pos[data['old']]
            del G.node[node]['old']

        return G, new_pos