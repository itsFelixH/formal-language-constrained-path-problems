import os
import networkx as nx


class Reader:

    @staticmethod
    def convert_to_graph(filename):
        """Reads graph from file(s).
        Parameters:
        filename : string (i.e.: "USA-road-d.NY")

        Returns:
        G : NetworkX graph
        dic: dictionary (positions of the nodes)"""

        current_folder_path, current_folder_name = os.path.split(os.getcwd())
        if current_folder_name == 'Tests':
            path = os.path.join("../MapData", filename)
        else:
            path = os.path.join("MapData", filename)
        G = Reader.get_graph_data(path + ".gr")
        dic = Reader.get_coordinates(path + ".co")

        return G, dic
    
    @staticmethod
    def get_graph_data(filename):
        """Reads graph from file.
        Parameters:
        filename : string (filename of gr-file)

        Returns:
        G : NetworkX graph"""

        f = open(filename, 'r')
        G = nx.DiGraph()
        for line in f:
            if line[0] == 'a':
                set = line[2:-1].split()
                G.add_node(int(set[0]))
                G.add_node(int(set[1]))
                G.add_edge(int(set[0]), int(set[1]), weight=int(int(set[2])))

        f.close()
        return G

    @staticmethod
    def get_coordinates(filename):
        """Reads node coordinates from file.
        Parameters:
        filename : string (filename of co-file)

        Returns:
        dic: dictionary (positions of the nodes)"""

        dic = {}
        f = open(filename, 'r')
        for line in f:
            if line[0] == 'v':

                set = line[2:-1].split()
                dic[int(set[0])] = (int(set[1]),int(set[2]))

        f.close()
        return dic