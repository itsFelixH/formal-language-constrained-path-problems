import networkx as nx
from binheap import BinHeap
from math import isinf


class Dijkstra:

    @staticmethod
    def s_shortest_path(G, source):
        """Compute shortest path from source to all nodes in the graph G.
        Parameters:
        G : NetworkX graph
        source : node (Starting node for path)

        Returns:
        dist: dict (dictionary of shortest path distances for each node)
        pred: dict (dictionary of predecessors for each node)"""

        multigraph = 0
        if G.is_multigraph():
            multigraph = 1

        dist = {source: 0}
        pred = {}
        nodes = set(nx.nodes(G))

        while nodes: 
            min_node = None
            for node in nodes:
                if node in dist:
                    if min_node is None:
                        min_node = node
                    elif dist[node] < dist[min_node]:
                        min_node = node

            if min_node is None:
                return dist, pred


            nodes.remove(min_node)
            current_weight = dist[min_node]

            if not multigraph:
                for node in G.successors(min_node):
                    weight = current_weight + G[min_node][node]['weight']
                    if node not in dist or weight < dist[node]:
                        dist[node] = weight
                        pred[node] = min_node
            else:
                for node in G.successors(min_node):
                    for edge in G[min_node][node]:
                        weight = current_weight + G[min_node][node][edge]['weight']
                        if node not in dist or weight < dist[node]:
                            dist[node] = weight
                            pred[node] = min_node
        return dist, pred
    
    @staticmethod
    def s_shortest_path_heap(G, source):
        """Compute shortest path from source to all nodes in the graph G using a heap as priority list.
        Parameters:
        G : NetworkX graph
        source : node (Starting node for path)

        Returns:
        dist: dict (dictionary of shortest path distances for each node)
        pred: dict (dictionary of predecessors for each node)"""

        multigraph = 0
        if G.is_multigraph():
            multigraph = 1

        heap = BinHeap()
        heap.insert(source,0)
        pred = {}
        nodes = set(nx.nodes(G))

        while heap.currentSize > 0: 
            min_node = heap.extractMin()

            nodes.remove(min_node)
            current_weight = heap.key[min_node]

            if not multigraph:
                for node in G.successors(min_node):
                    weight = current_weight + G[min_node][node]['weight']
                    if node not in heap.key:
                        heap.insert(node, weight)
                        pred[node] = min_node
                    elif weight < heap.key[node]:
                        heap.decreaseKey(node, weight)
                        pred[node] = min_node
            else:
                for node in G.successors(min_node):
                    for edge in G[min_node][node]:
                        weight = current_weight + G[min_node][node][edge]['weight']
                        if node not in heap.key:
                            heap.insert(node, weight)
                            pred[node] = min_node
                        elif weight < heap.key[node]:
                            heap.decreaseKey(node, weight)
                            pred[node] = min_node
        dist = heap.key
        return dist, pred

    @staticmethod
    def st_shortest_path_heap(G, source, target):
        """Compute shortest path from source to target in the graph G using a heap as priority list.
        Raises NetworkXNoPath exception when no path exists.
        Parameters:
        G : NetworkX graph
        source : node (Starting node for path)
        target : node (Ending node for path)

        Returns:
        dist: int (The length of the shortest path from the source to the target)
        path: list (A single list of nodes in a shortest path from the source to the target)"""

        if source == target:
            return 0, [source]

        multigraph = 0
        if G.is_multigraph():
            multigraph = 1

        heap = BinHeap()
        heap.insert(source, 0)
        pred = {}
        nodes = set(nx.nodes(G))

        while heap.currentSize > 0:
            min_node = heap.extractMin()
            if min_node == target:
                dist = heap.key[target]
                path = []
                node = target
                while True:
                    path[:0] = [node]
                    if node == source:
                        break
                    node = pred[node]
                return dist, path

            nodes.remove(min_node)
            current_weight = heap.key[min_node]

            if not multigraph:
                for node in G.successors(min_node):
                    weight = current_weight + G[min_node][node]['weight']
                    if node not in heap.key:
                        heap.insert(node, weight)
                        pred[node] = min_node
                    elif weight < heap.key[node]:
                        heap.decreaseKey(node, weight)
                        pred[node] = min_node
            else:
                for node in G.successors(min_node):
                    for edge in G[min_node][node]:
                        weight = current_weight + G[min_node][node][edge]['weight']
                        if node not in heap.key:
                            heap.insert(node, weight)
                            pred[node] = min_node
                        elif weight < heap.key[node]:
                            heap.decreaseKey(node, weight)
                            pred[node] = min_node

        raise nx.NetworkXNoPath("No path between %s and %s." % (source, target))


class DAGraph:

    @staticmethod
    def top_sort(G):
        """Compute topological sorting of DAG G.
        Parameters:
        G : NetworkX graph

        Returns:
        graph_sorted: list of nodes (list of nodes in topological sort order)"""

        graph_sorted = nx.topological_sort(G)
        return graph_sorted


    @staticmethod
    def s_shortest_path(G, source):
        """Compute shortest path from source to target in the DAG G.
        Parameters:
        G : NetworkX graph
        source : node (Starting node for path)

        Returns:
        dist: dict (dictionary of shortest path distances for each node)
        pred: dict (dictionary of predecessors for each node)"""

        multigraph = 0
        if G.is_multigraph():
            multigraph = 1

        top_sorted_nodes = DAGraph.top_sort(G)

        dist = {}
        for node in top_sorted_nodes:
            dist[node] = float('inf')

        dist[source] = 0
        pred = {}

        if not multigraph:
            for node in top_sorted_nodes:
                for successor in G.successors(node):
                    weight = dist[node] + G[node][successor]['weight']
                    if successor not in dist or weight < dist[successor]:
                        dist[successor] = weight
                        pred[successor] = node
        else:
            for node in top_sorted_nodes:
                for successor in G.successors(node):
                    for edge in G[node][successor]:
                        weight = dist[node] + G[node][successor][edge]['weight']
                        if successor not in dist or weight < dist[successor]:
                            dist[successor] = weight
                            pred[successor] = node

        dist = {node: weight for node, weight in dist.items() if not isinf(weight)}

        return dist, pred


class SPGraph:

    @staticmethod
    def st_shortest_path(G, source, target):
        """Compute shortest path from source to target in the SPG G recursively.
        Parameters:
        G : NetworkX graph
        source : node (Starting node for path)
        target : node (Ending node for path)

        Returns:
        dist: int (The length of the shortest path from the source to the target)
        path: list (A single list of nodes in a shortest path from the source to the target)"""

        successors = G.successors(source)
        num_edges = G.out_degree(source)

        if source == target:
            return 0, [source]
        elif num_edges == 0:
            raise nx.NetworkXNoPath("No path between %s and %s." % (source, target))
        elif num_edges == 1:
            node = successors[0]
            current_weight = G[source][node][0]['weight']
            G.remove_node(source)
            try:
                (weight, path) = SPGraph.st_shortest_path(G, node, target)
                new_weight = current_weight + weight
                path.insert(0, source)
                return new_weight, path
            except nx.NetworkXNoPath:
                raise nx.NetworkXNoPath("No path between %s and %s." % (source, target))
        else:
            weights = list()
            paths = list()
            for node in successors:
                for edge in G[source][node]:
                    H = G.copy()
                    current_weight = H[source][node][edge]['weight']
                    H.remove_node(source)
                    try:
                        (old_weight, old_path) = SPGraph.st_shortest_path(H, node, target)
                        weights.append(current_weight + old_weight)
                        paths.append(old_path)
                    except nx.NetworkXNoPath:
                        continue
            if len(weights) > 0:
                weight = min(weights)
                index = weights.index(weight)
                path = paths[index]
                path.insert(0, source)
                return weight, path
            else:
                raise nx.NetworkXNoPath("No path between %s and %s." % (source, target))