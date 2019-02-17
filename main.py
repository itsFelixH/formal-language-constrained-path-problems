import networkx as nx
import matplotlib.pyplot as plt
import time
import math
import random
import os
import common
from FAdo.reex import *
from FAdo.cfg import *
from FAdo.fa import *
from graph import GraphGenerator, GraphHelper
from constrainedpath import REGLanguage, CFLanguage, KSimilarPath
from reader import Reader
from automaton import Automaton
from shortestpath import Dijkstra, DAGraph, SPGraph


# Variables
max_weight1 = 50
max_weight2 = 1000
sigma1 = ['a','b']
sigma2 = ['a', 'b', 'c', 'd', 'e']
regex1 = '(a+ba)*'
regex2 = '(b+bab)*+a*'
regex3 = 'a*((b+cd)*+e)'
regex4 = '0(0+1)*1' # 0 vorne, 1 hinten
regex5 = '1*(01*01*)*'  # gerade Anzahl an 0en
regex5b = 'b*(ab*ab*)*'  # gerade Anzahl an a's
regex6 = '(a+b)*b(a+b)(a+b)'    # 2te Stelle von hinten = b
size1 = (5, 5)  # n = 25
size2 = (10, 10)  # n = 100
size3 = (15, 15)  # n = 225
size4 = (20, 20)  # n = 400
size5 = (25, 25)  # n = 625
size6 = (30, 30)  # n = 900
size7 = (40, 40)  # n = 1600
size8 = (50, 50)  # n = 2500
size9 = (60, 60)  # n = 3600
size10 = (75, 75)  # n = 5625
size11 = (100, 100)  # n = 10000
n1 = 100
n2 = 1000
n3 = 10000
iterations1 = 100
iterations2 = 1000
choice = 'av_times_cfg'

# Parameters
ask_user_choice = False


if ask_user_choice:
    print('''Formal Language Constrained Path Problems


    Press a button.

    a) Generate random grid with labels and weights.
    b) Calculate single source shortest path on a random DAG.
    c) Calculate single source shortest path on a random SPG.
    d) REG-ShP (without product) on random road network.
    e) REG-ShP (without product) on NY graph.
    f) Compare REG-ShP algorithms + write statistics.
    g) k similar path on NY
    h) CFG-ShP

    ''')

    choice = input('Your choice: ')


if choice == "a":
    # Variables
    sigma = sigma1
    m = size5[0]
    n = size5[1]
    max_weight = max_weight1

    # Parameters
    user_input = True
    show_plot = True

    if user_input:
        while True:
            m = input('Enter the number of rows of the grid: ')
            try:
                m = int(m)
            except ValueError:
                continue
            break
        while True:
            n = input('Enter the number of columns of the grid: ')
            try:
                n = int(n)
            except ValueError:
                continue
            break

    (G, dic) = GraphGenerator.random_weighted_labeled_grid(m, n, max_weight, sigma)

    if show_plot:
        nx.draw_networkx_nodes(G, pos=dic, with_labels=False, node_color='w', node_size=40)
        nx.draw_networkx_edges(G, pos=dic, arrows=False, edge_color='0.75', width=0.75)
        edge_labels = dict(((u, v), str(d['weight']) + ', ' + str(d['label'])) for u, v, d in G.edges(data=True))
        nx.draw_networkx_edge_labels(G, pos=dic, edge_labels=edge_labels, font_size=10)
        plt.show()


elif choice == "b":
    # Variables
    sigma = sigma1
    n = n2
    max_weight = max_weight1

    # Parameters
    user_input = True
    show_plot = True
    print_results = True

    if user_input:
        while True:
            n = input('How many nodes do you want to be generated?: ')
            try:
                n = int(n)
            except ValueError:
                continue
            break

    p = float(10) / (float(n) * 2)

    t1 = time.clock()
    G = GraphGenerator.random_weighted_dag(n, p, max_weight)
    t2 = time.clock()

    source = 0
    target = 0
    expected_dist = 0
    expected_path = []
    while True:
        try:
            source = random.choice(G.nodes())
            target = random.choice(G.nodes())

            expected_dist = nx.shortest_path_length(G, source=source, target=target, weight="weight")
            expected_path = nx.shortest_path(G, source=source, target=target, weight="weight")
        except nx.NetworkXNoPath:
            continue
        break

    t3 = time.clock()
    (dist, pred) = DAGraph.s_shortest_path(G, source)
    t4 = time.clock()

    path = []
    node = target
    while True:
        path[:0] = [node]
        if node == source:
            break
        node = pred[node]

    pathlist = []
    for u, v in zip(path[:-1], path[1:]):
        pathlist.append((u, v))

    if show_plot:
        dic = nx.spring_layout(G)
        t5 = time.clock()
        nx.draw_networkx_nodes(G, pos=dic, with_labels=False, node_color='w', node_size=40)
        nx.draw_networkx_nodes(G, pos=dic, nodelist=[source], with_labels=False, node_color='b', node_size=75)
        nx.draw_networkx_nodes(G, pos=dic, nodelist=[target], with_labels=False, node_color='r', node_size=75)
        nx.draw_networkx_nodes(G, pos=dic, nodelist=path[1:-1], with_labels=False, node_color='g', node_size=50)
        nx.draw_networkx_edges(G, pos=dic, arrows=False, edge_color='0.75', width=0.75)
        nx.draw_networkx_edges(G, pos=dic, edgelist=pathlist, arrows=False, edge_color='g', width=1.5)
        edge_labels = dict(((u, v), str(d['weight'])) for u, v, d in G.edges(data=True))
        nx.draw_networkx_edge_labels(G, pos=dic, edge_labels=edge_labels, font_size=10)
        source_label = {source: 'source'}
        target_label = {target: 'target'}
        nx.draw_networkx_labels(G, pos=dic, labels=source_label, font_size=16, font_color='b')
        nx.draw_networkx_labels(G, pos=dic, labels=target_label, font_size=16, font_color='r')
        t6 = time.clock()
        plt.show()

    if print_results:
        print('ShP on DAG')
        print('')
        print('The graph G has ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges.')
        print('')
        print('The shortest path has cost ' + str(dist[target]))
        if dist[target] == expected_dist and path == expected_path:
            print('The solution is correct')
        else:
            print('The solution is NOT correct')
            print('The right solution is ' + str(expected_dist))
        print('')
        print('Times:')
        print('Time to generate random grid: ' + str(t2-t1) + 's')
        print('Time to calculate shortest path: ' + str(t4-t3) + 's')
        if show_plot:
            print('Time to draw plot: ' + str(t6-t5) + 's')


elif choice == "c":
    # Variables
    n = n1
    max_weight = max_weight1

    # Parameters
    user_input = True
    show_plot = True
    print_results = True

    if user_input:
        while True:
            n = input('How many edges do you want to be generated?: ')
            try:
                n = int(n)
            except ValueError:
                continue
            break

    G = GraphGenerator.random_weighted_spg(n, max_weight)

    source = 0
    target = 0
    expected_dist = 0
    expected_path = []
    while True:
        try:
            source = random.choice(G.nodes())
            target = random.choice(G.nodes())

            expected_dist = nx.shortest_path_length(G, source=source, target=target, weight="weight")
            expected_path = nx.shortest_path(G, source=source, target=target, weight="weight")
        except nx.NetworkXNoPath:
            continue
        break

    t1 = time.clock()
    (dist, path) = SPGraph.st_shortest_path(G, source, target)
    t2 = time.clock()

    pathlist = []
    for u, v in zip(path[:-1], path[1:]):
        pathlist.append((u, v))

    if show_plot:
        dic = nx.spring_layout(G)
        t3 = time.clock()
        nx.draw_networkx_nodes(G, pos=dic, with_labels=False, node_color='w', node_size=40)
        nx.draw_networkx_nodes(G, pos=dic, nodelist=[source], with_labels=False, node_color='b', node_size=75)
        nx.draw_networkx_nodes(G, pos=dic, nodelist=[target], with_labels=False, node_color='r', node_size=75)
        nx.draw_networkx_nodes(G, pos=dic, nodelist=path[1:-1], with_labels=False, node_color='g', node_size=50)
        nx.draw_networkx_edges(G, pos=dic, arrows=True, edge_color='0.75', width=0.75)
        nx.draw_networkx_edges(G, pos=dic, edgelist=pathlist, arrows=True, edge_color='g', width=1.5)
        edge_labels = dict(((u, v), str(d['weight'])) for u, v, d in G.edges(data=True))
        nx.draw_networkx_edge_labels(G, pos=dic, edge_labels=edge_labels, font_size=10)
        source_label = {source: 'source'}
        target_label = {target: 'target'}
        nx.draw_networkx_labels(G, pos=dic, labels=source_label, font_size=16, font_color='b')
        nx.draw_networkx_labels(G, pos=dic, labels=target_label, font_size=16, font_color='r')
        t4 = time.clock()
        plt.show()

    if print_results:
        print('ShP on SPG')
        print('')
        print('The graph G has ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges.')
        print('')
        print('The shortest path has cost ' + str(dist))
        if dist == expected_dist and path == expected_path:
            print('The solution is correct')
        else:
            print('The solution is NOT correct')
            print('The right solution is ' + str(expected_dist))
        print('')
        print('Time to calculate shortest path: ' + str(t2-t1) + 's')
        if show_plot:
            print('Time to draw plot: ' + str(t4 - t3) + 's')


elif choice == "d":
    # Variables
    string = regex5b
    m = size4[0]
    n = size4[1]
    max_weight = max_weight1

    # Parameters
    user_input = False
    show_plot = False
    save_plot = True
    print_results = False

    if user_input:
        while True:
            m = input('Enter the number of rows: ')
            try:
                m = int(m)
            except ValueError:
                continue
            break
        while True:
            n = input('Enter the number of columns: ')
            try:
                n = int(n)
            except ValueError:
                continue
            break

    regex = str2regexp(string)
    sigma = list(regex.setOfSymbols())

    t1 = time.clock()
    (G, dic) = GraphGenerator.random_weighted_labeled_grid(m, n, max_weight, sigma)
    t2 = time.clock()

    (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

    source = random.choice(G.nodes())
    target = random.choice(G.nodes())

    try:
        (dist, path, times) = REGLanguage.st_reg_shortest_path(G, source, target, string, timeit=True)

        t3 = time.clock()
        (dist_sp, path_sp) = Dijkstra.st_shortest_path_heap(G, source, target)
        t4 = time.clock()

        L = GraphHelper.get_rectangle_around_s_and_t(dic, source, target, list(set(path + path_sp)))
        R = nx.subgraph(G, L)

        times['generate_graph'] = t2 - t1
        times['shortest_path'] = t4 - t3

        pathlist = []
        for u, v in zip(path[:-1], path[1:]):
            pathlist.append((u, v))

        word = ''
        for u, v in pathlist:
            word += str(G[u][v]['label'])

        if show_plot or save_plot:
            pathlist_sp = []
            for u, v in zip(path_sp[:-1], path_sp[1:]):
                pathlist_sp.append((u, v))

            t5 = time.clock()

            fig = plt.figure()
            plt.axis('off')

            nx.draw_networkx_nodes(R, pos=dic, with_labels=False, node_color='w', node_size=40)
            nx.draw_networkx_nodes(R, pos=dic, nodelist=[source], with_labels=False, node_color='b', node_size=75)
            nx.draw_networkx_nodes(R, pos=dic, nodelist=[target], with_labels=False, node_color='r', node_size=75)
            nx.draw_networkx_nodes(R, pos=dic, nodelist=path_sp[1:-1], with_labels=False, node_color='g', node_size=50)
            nx.draw_networkx_nodes(R, pos=dic, nodelist=path[1:-1], with_labels=False, node_color='y', node_size=50)
            nx.draw_networkx_edges(R, pos=dic, arrows=False, edge_color='0.75', width=0.75)
            nx.draw_networkx_edges(R, pos=dic, edgelist=pathlist_sp, arrows=False, edge_color='g', width=1.5)
            nx.draw_networkx_edges(R, pos=dic, edgelist=pathlist, arrows=False, edge_color='y', width=1.5)
            edge_labels = dict(((u, v), str(d['weight']) + ', ' + str(d['label'])) for u, v, d in R.edges(data=True))
            nx.draw_networkx_edge_labels(R, pos=dic, edge_labels=edge_labels, font_size=10)
            source_label = {source: 'source'}
            target_label = {target: 'target'}
            nx.draw_networkx_labels(R, pos=dic, labels=source_label, font_size=16, font_color='b')
            nx.draw_networkx_labels(R, pos=dic, labels=target_label, font_size=16, font_color='r')

            fig.tight_layout()
            fig.set_frameon(False)

            t6 = time.clock()
            times['draw_plot'] = t6 - t5

            if save_plot:
                dir = "SavedGridPlots"
                if not os.path.exists(dir):
                    os.makedirs(dir)
                timestr = time.strftime("%Y%m%d-%H%M%S")
                name = 'Figure-' + timestr
                filepath = os.path.join(dir, name)

                plt.savefig(filepath)
            if show_plot:
                plt.show()

        if print_results:
            print('REG-ShP on Grid')
            print('')
            print('The graph G has ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges.')
            print('')
            print('Shortest Path has cost ' + str(dist_sp))
            print('REG-constrained Path has cost ' + str(dist) + ' with label: ' + word)
            print('')
            if regex.evalWordP(word):
                print('The word has been accepted by the regular expression ' + string + '.')
            else:
                print('The word has NOT been accepted by the regular expression ' + string + '.')
            print('')
            print('Times: ')
            print('Time to generate random grid: ' + str(times['generate_graph']) + 's')
            print('Time to convert regular expression to NFA M(R): ' + str(times['regex_to_nfa']) + 's')
            print('Time to setup pointers for outgoing edges: ' + str(times['setup_pointers']) + 's')
            print('Time to calculate REG-constrained path: ' + str(times['calculate_path']) + 's')
            print('Time to calculate shortest path: ' + str(times['shortest_path']) + 's')
            print('Overall: ' + str(sum(times.values())) + 's')
            if show_plot:
                print('Time to draw plot: ' + str(times['draw_plot']) + 's')

    except nx.NetworkXNoPath:
        print('No path between %s and %s.' % (source, target))

elif choice == "e":
    # Variables
    string = regex1

    # Parameters
    full_ny = False
    show_plot = True
    save_plot = True
    print_results = True

    t1 = time.clock()
    [NY, dic] = Reader.convert_to_graph('USA-road-d.NY')
    t2 = time.clock()

    if full_ny:
        G = NY
    else:
        x1 = -7.39765e+07
        y1 = 4.06047e+07
        x2 = -7.39008e+07
        y2 = 4.06888e+07
        L = GraphHelper.get_all_nodes_in_rectangle(dic, x1, x2, y1, y2)

        G = nx.subgraph(NY, L)
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

    regex = str2regexp(string)
    sigma = list(regex.setOfSymbols())
    G = GraphGenerator.random_label(G, sigma)

    source = random.choice(G.nodes())
    target = random.choice(G.nodes())

    try:
        (dist, path, times) = REGLanguage.st_reg_shortest_path(G, source, target, string, timeit=True)

        t3 = time.clock()
        (dist_sp, path_sp) = Dijkstra.st_shortest_path_heap(G, source, target)
        t4 = time.clock()

        times['read_graph'] = t2 - t1
        times['shortest_path'] = t4 - t3

        pathlist = []
        for u, v in zip(path[:-1], path[1:]):
            pathlist.append((u, v))

        word = ''
        for u, v in pathlist:
            word += str(G[u][v]['label'])

        if show_plot or save_plot:
            pathlist_sp = []
            for u, v in zip(path_sp[:-1], path_sp[1:]):
                pathlist_sp.append((u, v))

            t5 = time.clock()

            fig = plt.figure()
            plt.axis('off')

            nx.draw_networkx_nodes(G, pos=dic, with_labels=False, node_color='w', node_size=40)
            nx.draw_networkx_nodes(G, pos=dic, nodelist=[source], with_labels=False, node_color='b', node_size=75)
            nx.draw_networkx_nodes(G, pos=dic, nodelist=[target], with_labels=False, node_color='r', node_size=75)
            nx.draw_networkx_nodes(G, pos=dic, nodelist=path_sp[1:-1], with_labels=False, node_color='g', node_size=50)
            nx.draw_networkx_nodes(G, pos=dic, nodelist=path[1:-1], with_labels=False, node_color='y', node_size=50)
            nx.draw_networkx_edges(G, pos=dic, arrows=False, edge_color='0.75', width=0.75)
            nx.draw_networkx_edges(G, pos=dic, edgelist=pathlist_sp, arrows=False, edge_color='g', width=1.5)
            nx.draw_networkx_edges(G, pos=dic, edgelist=pathlist, arrows=False, edge_color='y', width=1.5)
            edge_labels = dict(((u, v), str(d['weight']) + ', ' + str(d['label'])) for u, v, d in G.edges(data=True))
            nx.draw_networkx_edge_labels(G, pos=dic, edge_labels=edge_labels, font_size=10)
            source_label = {source: 'source'}
            target_label = {target: 'target'}
            nx.draw_networkx_labels(G, pos=dic, labels=source_label, font_size=16, font_color='b')
            nx.draw_networkx_labels(G, pos=dic, labels=target_label, font_size=16, font_color='r')

            fig.tight_layout()
            fig.set_frameon(False)

            t6 = time.clock()
            times['draw_plot'] = t6 - t5

            if save_plot:
                dir = "SavedNYPlots"
                if not os.path.exists(dir):
                    os.makedirs(dir)
                timestr = time.strftime("%Y%m%d-%H%M%S")
                name = 'Figure-' + timestr
                filepath = os.path.join(dir, name)
                plt.savefig(filepath)
            if show_plot:
                plt.show()

        if print_results:
            print('REG-ShP on NY')
            print('')
            print('The graph has ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges.')
            print('')
            print('Shortest Path has cost ' + str(dist_sp))
            print('REG-constrained Path has cost ' + str(dist) + ' with label: ' + word)
            print('')
            if regex.evalWordP(word):
                print('The word has been accepted by the regular expression ' + string + '.')
            else:
                print('The word has NOT been accepted by the regular expression ' + string + '.')
            print('')
            print('Times: ')
            print('Time to read graph of NY from file: ' + str(times['read_graph']) + 's')
            print('Time to convert regular expression to NFA M(R): ' + str(times['regex_to_nfa']) + 's')
            print('Time to setup pointers for outgoing edges: ' + str(times['setup_pointers']) + 's')
            print('Time to calculate REG-constrained path: ' + str(times['calculate_path']) + 's')
            print('Time to calculate shortest path: ' + str(times['shortest_path']) + 's')
            print('Overall: ' + str(sum(times.values())) + 's')
            if show_plot:
                print('Time to draw plot: ' + str(times['draw_plot']) + 's')

    except nx.NetworkXNoPath:
        print('No path between %s and %s.' % (source, target))


elif choice == "f":
    # Variables
    strings = ['0(0+1)*1', '1*(01*01*)*', '(a+b)*b(a+b)(a+b)', 'a*((b+cd)*+e)']
    sizes = [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100]
    i = iterations1
    max_weight = max_weight1

    # Parameters
    user_input = False
    write_statistics = True

    if user_input:
        while True:
            m = input('Enter the number of rows: ')
            try:
                m = int(m)
            except ValueError:
                continue
            break
        while True:
            n = input('Enter the number of columns: ')
            try:
                n = int(n)
            except ValueError:
                continue
            break
        while True:
            i = input('Enter the number of iterations: ')
            try:
                i = int(i)
            except ValueError:
                continue
            break

    for string in strings:

        regex = str2regexp(string)
        sigma = list(regex.setOfSymbols())

        print('Starting ' + string + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

        for size in sizes:
            (G, dic) = GraphGenerator.random_weighted_labeled_grid(size, size, max_weight, sigma)
            (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

            if write_statistics:
                dir = "Statistics"
                if not os.path.exists(dir):
                    os.makedirs(dir)
                timestr = time.strftime("%Y%m%d-%H%M%S")
                name = str(G.number_of_nodes()) + '_' + string + '_' + timestr + '.csv'
                name = re.sub(r'[\\/*?:"<>|]', '', name)
                filepath = os.path.join(dir, name)

                f = open(filepath, 'w')
                f.write('Graph G ' + ';' + str(G.number_of_nodes()) + ' nodes' + ';' + str(G.number_of_edges()) + ' edges\n')
                f.write('Regexp: ' + ';' + string + "\n")
                f.write('\n')
                f.write('Source;Target;Distance;Bee Line;#Nodes REG-ShP;#Nodes ShP;Time REG-ShP;Time NFA;Time PreProcess;'
                        'Time Calc;Time REG-ShP(product);Time NFA;Time Product;Time Calc;Time ShP\n')

            for k in range(i):
                l = 0
                while True:
                    if l >= 25:
                        (G, dic) = GraphGenerator.random_weighted_labeled_grid(size, size, max_weight, sigma)
                        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)
                        l = 0
                    try:
                        source = random.choice(G.nodes())
                        target = random.choice(G.nodes())

                        (dist2, path2, time2) = REGLanguage.st_reg_shortest_path(G, source, target, string, timeit=True)
                        (dist1, path1, time1) = REGLanguage.st_reg_shortest_path__product_nfa(G, source, target, string, timeit=True)
                        t1 = time.clock()
                        (dist_sp, path_sp) = Dijkstra.st_shortest_path_heap(G, source, target)
                        t2 = time.clock()

                        time_sp = t2 - t1
                    except nx.NetworkXNoPath:
                        l += 1
                        continue
                    break

                beeline = int(math.sqrt(((dic[source][0] - dic[target][0]) ** 2) + (dic[source][1] - dic[target][1]) ** 2))

                if write_statistics:
                    f.write(str(source) + ';' + str(target) + ';' + str(dist1) + ';' + str(beeline) + ';' +
                            str(len(path1)) + ';' + str(len(path_sp)) + ';' +
                            "{0:.6f}".format(sum(time2.values())) + ';' +
                            "{0:.6f}".format(time2['regex_to_nfa']) + ';' +
                            "{0:.6f}".format(time2['setup_pointers']) + ';' +
                            "{0:.6f}".format(time2['calculate_path']) + ';' +
                            "{0:.6f}".format(sum(time1.values())) + ';' +
                            "{0:.6f}".format(time1['regex_to_nfa'] + time1['graph_to_nfa']) + ';' +
                            "{0:.6f}".format(time1['product_nfa']) + ';' +
                            "{0:.6f}".format(time1['calculate_path']) + ';' +
                            "{0:.6f}".format(time_sp) + "\n")
            print(string + ' with size ' + str(G.number_of_nodes()) + ' done' + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

            f.close()
        print(string + ' done' + ' at ' + time.strftime("%Y%m%d-%H%M%S"))
        print('----------------')



elif choice == "g":
    # Variables
    k = 20

    # Parameters
    full_ny = False
    show_plot = True
    save_plot = True
    print_results = True

    [NY, dic] = Reader.convert_to_graph('USA-road-d.NY')

    if full_ny:
        G = NY
    else:
        x1 = -7.39765e+07
        y1 = 4.06047e+07
        x2 = -7.39008e+07
        y2 = 4.06888e+07
        L = GraphHelper.get_all_nodes_in_rectangle(dic, x1, x2, y1, y2)

        G = nx.subgraph(NY, L)
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

    source = random.choice(G.nodes())
    target = random.choice(G.nodes())

    try:
        (dist, distk, path, pathk) = KSimilarPath.st_k_similar_path(G, source, target, k)

        if show_plot or save_plot:
            L = GraphHelper.get_rectangle_around_s_and_t(dic, source, target, list(set(path + pathk)))
            R = nx.subgraph(G, L)

            pathlist = GraphHelper.get_edgelist_from_nodelist(path)
            pathlistk = GraphHelper.get_edgelist_from_nodelist(pathk)

            common_edges = 0
            for edge in pathlistk:
                if edge in pathlist:
                    common_edges += 1

            nx.draw_networkx_nodes(R, pos=dic, with_labels=False, node_color='w', node_size=40)
            nx.draw_networkx_nodes(R, pos=dic, nodelist=[source], with_labels=False, node_color='b', node_size=75)
            nx.draw_networkx_nodes(R, pos=dic, nodelist=[target], with_labels=False, node_color='r', node_size=75)
            nx.draw_networkx_nodes(R, pos=dic, nodelist=path[1:-1], with_labels=False, node_color='g', node_size=50)
            nx.draw_networkx_nodes(R, pos=dic, nodelist=pathk[1:-1], with_labels=False, node_color='y', node_size=50)
            nx.draw_networkx_edges(R, pos=dic, arrows=False, edge_color='0.75', width=0.75)
            nx.draw_networkx_edges(R, pos=dic, edgelist=pathlist, arrows=False, edge_color='g', width=1.5)
            nx.draw_networkx_edges(R, pos=dic, edgelist=pathlistk, arrows=False, edge_color='y', width=1.5)
            edge_labels = dict(((u, v), str(d['weight'])) for u, v, d in R.edges(data=True))
            nx.draw_networkx_edge_labels(R, pos=dic, edge_labels=edge_labels, font_size=10)
            source_label = {source: 'source'}
            target_label = {target: 'target'}
            nx.draw_networkx_labels(R, pos=dic, labels=source_label, font_size=16, font_color='b')
            nx.draw_networkx_labels(R, pos=dic, labels=target_label, font_size=16, font_color='r')

            if save_plot:
                dir = "KSimilarPath"
                if not os.path.exists(dir):
                    os.makedirs(dir)
                timestr = time.strftime("%Y%m%d-%H%M%S")
                name = 'Figure-' + timestr
                filepath = os.path.join(dir, name)
                plt.savefig(filepath)
            if show_plot:
                plt.show()

        if print_results:
            print('k Similar Path on NY')
            print('')
            print('The graph has ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges.')
            print('')
            print('Shortest Path has cost ' + str(dist))
            print('k Similar Path has cost ' + str(distk))
            print('They have ' +str(common_edges) + ' edges in common.')

    except nx.NetworkXNoPath:
        print('No path between %s and %s.' % (source, target))


elif choice == "h":
    # Variables
    productions = [('S', ('A')), ('A', ('x', 'A', 'y')), ('A', ('x', 'B', 'y')), ('B', ('z'))]
    m = size1[0]
    n = size1[1]
    max_weight = max_weight1

    # Parameters
    user_input = False
    print_results = True

    if user_input:
        while True:
            m = input('Enter the number of rows: ')
            try:
                m = int(m)
            except ValueError:
                continue
            break
        while True:
            n = input('Enter the number of columns: ')
            try:
                n = int(n)
            except ValueError:
                continue
            break

    grammar = CNF(productions)

    grammar.makenonterminals()
    grammar.maketerminals()
    grammar.terminalrules()

    terminals = grammar.Terminals
    tr = grammar.tr
    rules = grammar.Rules
    start = grammar.Start

    (G, dic) = GraphGenerator.random_weighted_labeled_grid(m, n, max_weight, list(terminals))

    D = CFLanguage.all_pair_cfg_shortest_path(G, grammar)

    while True:
        source = random.choice(G.nodes())
        target = random.choice(G.nodes())

        try:
            (dist_sp, path_sp) = Dijkstra.st_shortest_path_heap(G, source, target)
        except nx.NetworkXNoPath:
            continue

        dist = D[source][target][start]

        if dist < float('inf'):
            break

    if print_results:
        print('CFG-ShP on NY')
        print('')
        print('The graph has ' + str(G.number_of_nodes()) + ' nodes and ' + str(G.number_of_edges()) + ' edges.')
        print('')
        print('Shortest Path has cost ' + str(dist_sp))
        print('CFG-constrained Path has cost ' + str(dist)) #+ ' with label: ' + word)




elif choice == 'regex':
    k = 5
    regex_helper = 'f*'
    regex_str = 'f*'
    for i in range(k):
        regex_helper += 'tf*'
        regex_str += '+' + regex_helper

    R = str2regexp(regex_str)
    M = Automaton.regex_to_automaton(regex_str)

    M.display()

elif choice == 'nfa':
    M = DFA()
    M.setSigma(['a', 'b'])
    M.addState('s1')
    M.addState('s2')
    M.addState('s3')
    M.setInitial(0)
    M.addFinal(2)
    M.addTransition(0, 'a', 0)
    M.addTransition(0, 'b', 1)
    M.addTransition(1, 'a', 1)
    M.addTransition(1, 'b', 2)
    M.addTransition(2, 'a', 2)

    print(M.reCG())

elif choice == 'av_times':
    # Variables
    strings = ['a*((b+cd)*+e)']
    # strings = ['(a+ba)*', '(b+bab)*+a*', 'a*((b+cd)*+e)', '0(0+1)*1', '1*(01*01*)*', '(a+b)*b(a+b)(a+b)']
    sizes = [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100]
    # sizes = [5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100]
    i = iterations1
    max_weight = max_weight1

    for string in strings:
        print('Starting ' + string + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

        regex = str2regexp(string)
        sigma = list(regex.setOfSymbols())

        for n in sizes:
            (G, dic) = GraphGenerator.random_weighted_labeled_grid(n, n, max_weight, sigma)
            (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

            times = dict()
            times2 = dict()

            for k in range(i):

                if (k+1) % 10 == 0:
                    print('Iteration ' + str(k+1))

                l = 0
                while True:
                    if l >= 25:
                        (G, dic) = GraphGenerator.random_weighted_labeled_grid(n, n, max_weight, sigma)
                        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)
                        l = 0
                    try:
                        source = random.choice(G.nodes())
                        target = random.choice(G.nodes())

                        (dist2, path2, time2) = REGLanguage.st_reg_shortest_path(G, source, target, string, timeit=True)

                        (dist1, path1, time1) = REGLanguage.st_reg_shortest_path__product_nfa(G, source, target, string,
                                                                                              timeit=True)
                        for label in time1:
                            if label not in times:
                                times[label] = []
                            times[label].append(time1[label])
                        for label in time2:
                            if label not in times2:
                                times2[label] = []
                            times2[label].append(time2[label])
                    except nx.NetworkXNoPath:
                        l += 1
                        continue
                    break

            av_time = dict()
            for label in times:
                av_time[label] = sum(times[label]) / float(i)
            av_time2 = dict()
            for label in times2:
                av_time2[label] = sum(times2[label]) / float(i)

            dir = "Statistics"
            if not os.path.exists(dir):
                os.makedirs(dir)
            timestr = time.strftime("%Y%m%d-%H%M%S")
            name = 'av_times_' + string + '_' + timestr + '.csv'
            name = re.sub(r'[\\/*?:"<>|]', '', name)
            filepath = os.path.join(dir, name)

            f = open(filepath, 'w')
            f.write('Regexp: ' + ';' + string + "\n")
            f.write('Average' + ';' + 'times' + ';' + 'for' + ';' + str(i) + ';' + 'iterations:' + '\n')
            f.write('\n')
            f.write('N;Time REG-ShP;Time NFA;Time PreProcess;Time Calc;'
                    'Time REG-ShP(product);Time NFA;Time Product;Time Calc\n')

            f.write(str(n) + ';' +
                    "{0:.6f}".format(sum(av_time2.values())) + ';' +
                    "{0:.6f}".format(av_time2['regex_to_nfa']) + ';' +
                    "{0:.6f}".format(av_time2['setup_pointers']) + ';' +
                    "{0:.6f}".format(av_time2['calculate_path']) + ';' +
                    "{0:.6f}".format(sum(av_time.values())) + ';' +
                    "{0:.6f}".format(av_time['regex_to_nfa'] + av_time['graph_to_nfa']) + ';' +
                    "{0:.6f}".format(av_time['product_nfa']) + ';' +
                    "{0:.6f}".format(av_time['calculate_path']) + "\n")

            print(string + ' with size ' + str(G.number_of_nodes()) + ' done' + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

            f.close()

        print(string + ' done' + ' at ' + time.strftime("%Y%m%d-%H%M%S"))
        print('----------------')


elif choice == 'av_times_ny':
    # Variables
    strings = ['0(0+1)*1', '1*(01*01*)*', '(a+b)*b(a+b)(a+b)', '(a+ba)*', '(b+bab)*+a*', 'a*((b+cd)*+e)']
    # strings = ['(a+ba)*', '(b+bab)*+a*', 'a*((b+cd)*+e)', '0(0+1)*1', '1*(01*01*)*', '(a+b)*b(a+b)(a+b)']
    i = iterations1

    # Parameters
    full_ny = True

    [NY, dic] = Reader.convert_to_graph('USA-road-d.NY')

    if full_ny:
        G = NY
    else:
        x1 = -7.39765e+07
        y1 = 4.06047e+07
        x2 = -7.39008e+07
        y2 = 4.06888e+07
        L = GraphHelper.get_all_nodes_in_rectangle(dic, x1, x2, y1, y2)

        G = nx.subgraph(NY, L)
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

    for string in strings:
        print('Starting ' + string + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

        regex = str2regexp(string)
        sigma = list(regex.setOfSymbols())
        G = GraphGenerator.random_label(G, sigma)

        dir = "Statistics"
        if not os.path.exists(dir):
            os.makedirs(dir)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        name = 'NY_av_times_' + string + '_' + timestr + '.csv'
        name = re.sub(r'[\\/*?:"<>|]', '', name)
        filepath = os.path.join(dir, name)

        f = open(filepath, 'w')
        f.write('Regexp: ' + ';' + string + "\n")
        f.write('Average;times;for;' + str(i) + ';iterations:' + '\n')
        f.write('\n')
        f.write('Time REG-ShP;Dist REG-ShP;Nodes REG-ShP;Time ShP;Dist ShP;Nodes ShP' + '\n')

        times = dict()
        times_sp = []
        num_nodes = []
        num_nodes_sp = []
        dists = []
        dists_sp = []

        l = 0
        for k in range(i):
            print('Starting Iteration ' + str(k + 1) + ' at ' + time.strftime("%Y%m%d-%H%M%S"))
            while True:
                if l >= 25:
                    G = GraphGenerator.random_label(G, sigma)
                    l = 0
                try:
                    source = random.choice(G.nodes())
                    target = random.choice(G.nodes())

                    (dist, path, time1) = REGLanguage.st_reg_shortest_path(G, source, target, string, timeit=True)

                    t1 = time.clock()
                    (dist_sp, path_sp) = Dijkstra.st_shortest_path_heap(G, source, target)
                    t2 = time.clock()

                    time_sp = t2 - t1
                    times_sp.append(time_sp)

                    num_nodes.append(len(path))
                    num_nodes_sp.append(len(path_sp))
                    dists.append(dist)
                    dists_sp.append(dist_sp)

                    for label in time1:
                        if label not in times:
                            times[label] = []
                        times[label].append(time1[label])
                except nx.NetworkXNoPath:
                    l += 1
                    continue
                break

        av_time = dict()
        for label in times:
            av_time[label] = sum(times[label]) / float(i)

        f.write("{0:.6f}".format(sum(av_time.values())) + ';' +
                "{0:.6f}".format(sum(dists)/float(i)) + ';' +
                "{0:.6f}".format(sum(num_nodes)/float(i)) + ';' +
                "{0:.6f}".format(sum(times_sp)/float(i)) + ';' +
                "{0:.6f}".format(sum(dists_sp) / float(i)) + ';' +                "{0:.6f}".format(sum(num_nodes_sp) / float(i)) + "\n")
        f.close()

        print(string + ' done' + ' at ' + time.strftime("%Y%m%d-%H%M%S"))
        print('----------------')


elif choice == 'av_times_ny_ksim':
    # Variables
    sizes = [100]
    ks = [0, 1, 2, 5, 10, 20, 30, 40, 50]
    i = iterations1

    # Parameters
    full_ny = True

    [NY, dic] = Reader.convert_to_graph('USA-road-d.NY')

    if full_ny:
        G = NY
    else:
        x1 = -7.39765e+07
        y1 = 4.06047e+07
        x2 = -7.39008e+07
        y2 = 4.06888e+07
        L = GraphHelper.get_all_nodes_in_rectangle(dic, x1, x2, y1, y2)

        G = nx.subgraph(NY, L)
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

    dir = "Statistics"
    if not os.path.exists(dir):
        os.makedirs(dir)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = 'av_ny_ksim_' + str(G.number_of_nodes()) + '_' + timestr + '.csv'
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    filepath = os.path.join(dir, name)

    f = open(filepath, 'w')
    f.write('K-similar Path' + "\n")
    f.write('\n')
    f.write('Average' + ';' + 'values' + ';' + 'for' + ';' + str(i) + ';' + 'iterations:' + '\n')
    f.write('\n')
    f.write('k;Total Time;Time KSimP;Dist KSimP;Nodes KSimP;Time ShP;Dist ShP;Nodes ShP\n')

    for k in ks:
        print('Starting k = ' + str(k) + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

        times = dict()
        num_nodes = []
        num_nodesk = []
        dists = []
        distsk = []

        for l in range(i):
            while True:
                try:
                    source = random.choice(G.nodes())
                    target = random.choice(G.nodes())

                    (dist, distk, path, pathk, time1) = KSimilarPath.st_k_similar_path(G, source, target, k, timeit=True)

                    num_nodes.append(len(path))
                    num_nodesk.append(len(pathk))
                    dists.append(dist)
                    distsk.append(distk)

                    for label in time1:
                        if label not in times:
                            times[label] = []
                        times[label].append(time1[label])
                except nx.NetworkXNoPath:
                    continue
                break

        av_time = dict()
        for label in times:
            av_time[label] = sum(times[label]) / float(i)

        dir = "Statistics"
        if not os.path.exists(dir):
            os.makedirs(dir)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        name = 'av_ny_ksim_' + str(k) + '_' + timestr + '.csv'
        name = re.sub(r'[\\/*?:"<>|]', '', name)
        filepath = os.path.join(dir, name)

        f = open(filepath, 'w')
        f.write('K-similar Path' + "\n")
        f.write('\n')
        f.write('Average' + ';' + 'values' + ';' + 'for' + ';' + str(i) + ';' + 'iterations:' + '\n')
        f.write('\n')
        f.write('k;Total Time;Time KSimP;Dist KSimP;Nodes KSimP;Time ShP;Dist ShP;Nodes ShP\n')

        f.write(str(k) + ';' +
                "{0:.6f}".format(sum(av_time.values())) + ';' +
                "{0:.6f}".format(av_time['KSimP'] + av_time['Labels']) + ';' +
                "{0:.6f}".format(sum(distsk) / float(i)) + ';' +
                "{0:.6f}".format(sum(num_nodesk) / float(i)) + ';' +
                "{0:.6f}".format(av_time['ShP']) + ';' +
                "{0:.6f}".format(sum(dists) / float(i)) + ';' +
                "{0:.6f}".format(sum(num_nodes) / float(i))+ "\n")
        f.close()

        print('k = ' + str(k) + ' done' + ' at ' + time.strftime("%Y%m%d-%H%M%S"))
        print('----------------------')



elif choice == 'av_times_ksim':
    # Variables
    sizes = [100]
    ks = [0, 1, 2, 5, 10, 20, 30, 40, 50]
    i = iterations1
    max_weight = max_weight1

    for n in sizes:
        (G, dic) = GraphGenerator.random_weighted_labeled_grid(n, n, max_weight)
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

        print('Starting size ' + str(G.number_of_nodes()) + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

        dir = "Statistics"
        if not os.path.exists(dir):
            os.makedirs(dir)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        name = 'av_ksim_' + str(G.number_of_nodes()) + '_' + timestr + '.csv'
        name = re.sub(r'[\\/*?:"<>|]', '', name)
        filepath = os.path.join(dir, name)

        f = open(filepath, 'w')
        f.write('K-similar Path' + "\n")
        f.write('Graph G ' + ';' + str(G.number_of_nodes()) + ' nodes' + ';' + str(G.number_of_edges()) + ' edges\n')
        f.write('\n')
        f.write('Average' + ';' + 'values' + ';' + 'for' + ';' + str(i) + ';' + 'iterations:' + '\n')
        f.write('\n')
        f.write('k;Total Time;Time KSimP;Dist KSimP;Nodes KSimP;Time ShP;Dist ShP;Nodes ShP\n')

        for k in ks:
            print('Starting k = ' + str(k) + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

            times = dict()
            num_nodes = []
            num_nodesk = []
            dists = []
            distsk = []

            j = 0
            for l in range(i):
                while True:
                    if j >= 25:
                        (G, dic) = GraphGenerator.random_weighted_labeled_grid(n, n, max_weight)
                        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)
                        j = 0
                    try:
                        source = random.choice(G.nodes())
                        target = random.choice(G.nodes())

                        (dist, distk, path, pathk, time1) = KSimilarPath.st_k_similar_path(G, source, target, k, timeit=True)

                        num_nodes.append(len(path))
                        num_nodesk.append(len(pathk))
                        dists.append(dist)
                        distsk.append(distk)

                        for label in time1:
                            if label not in times:
                                times[label] = []
                            times[label].append(time1[label])
                    except nx.NetworkXNoPath:
                        j += 1
                        continue
                    break

            av_time = dict()
            for label in times:
                av_time[label] = sum(times[label]) / float(i)

            f.write(str(k) + ';' +
                    "{0:.6f}".format(sum(av_time.values())) + ';' +
                    "{0:.6f}".format(av_time['KSimP'] + av_time['Labels']) + ';' +
                    "{0:.6f}".format(sum(distsk) / float(i)) + ';' +
                    "{0:.6f}".format(sum(num_nodesk) / float(i)) + ';' +
                    "{0:.6f}".format(av_time['ShP']) + ';' +
                    "{0:.6f}".format(sum(dists) / float(i)) + ';' +
                    "{0:.6f}".format(sum(num_nodes) / float(i))+ "\n")
        f.close()

        print('Size ' + str(G.number_of_nodes()) + ' done' + ' at ' + time.strftime("%Y%m%d-%H%M%S"))
        print('----------------')


elif choice == 'av_times_cfg':
    # Variables
    # productions = [('S', ('A')), ('A', ('x', 'A', 'y')), ('A', ('x', 'B', 'y')), ('B', ('z'))]
    # productions = [('A', ('a','A')), ('A', ('a', 'b', 'c'))]
    productions = [('S', ('0', '0', 'S')), ('S', ('1', '1', 'F')), ('F', ('0', '0', 'F')), ('F', common.Epsilon)]
    # productions = [('S', ('a', 'S')), ('S', ('S', 'b')), ('S', common.Epsilon)]
    m = 5
    n = 10
    i = iterations1
    max_weight = max_weight1

    grammar = CNF(productions)

    grammar.makenonterminals()
    grammar.maketerminals()
    grammar.terminalrules()

    terminals = grammar.Terminals
    tr = grammar.tr
    rules = grammar.Rules
    start = grammar.Start

    dir = "Statistics"
    if not os.path.exists(dir):
        os.makedirs(dir)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = 'av_times_' + str(m*n) + '_' + timestr + '.csv'
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    filepath = os.path.join(dir, name)

    f = open(filepath, 'w')
    f.write('Graph G ' + ';' + str(m*n) + ' nodes\n')
    f.write('Language: ' + ';' + 'L={x^n z y^n}')
    f.write('\n')
    f.write('Time CFG-ShP\n')

    for k in range(i):
        print('Starting Iteration ' + str(k + 1) + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

        (G, dic) = GraphGenerator.random_weighted_labeled_grid(m, n, max_weight, list(terminals))
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

        t1 = time.clock()
        D = CFLanguage.all_pair_cfg_shortest_path(G, grammar)
        t2 = time.clock()

        f.write("{0:.6f}".format(t2-t1) + "\n")
    f.close()

elif choice == 'av_times_sp':
    # Variables
    m = 5
    n = 15
    i = iterations1
    max_weight = max_weight1

    dir = "Statistics"
    if not os.path.exists(dir):
        os.makedirs(dir)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    name = 'av_times_' + str(m*n) + '_' + timestr + '.csv'
    name = re.sub(r'[\\/*?:"<>|]', '', name)
    filepath = os.path.join(dir, name)

    f = open(filepath, 'w')
    f.write('Graph G ' + ';' + str(m*n) + ' nodes\n')
    f.write('\n')
    f.write('Time ShP\n')

    for k in range(i):
        print('Starting Iteration ' + str(k + 1) + ' at ' + time.strftime("%Y%m%d-%H%M%S"))

        (G, dic) = GraphGenerator.random_weighted_labeled_grid(m, n, max_weight)
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

        nodes = G.nodes()

        t1 = time.clock()
        for s in nodes:
            for t in nodes:
                try:
                    (dist, path) = Dijkstra.st_shortest_path_heap(G, s, t)
                except nx.NetworkXNoPath:
                    continue
        t2 = time.clock()

        f.write("{0:.6f}".format(t2-t1) + "\n")
    f.close()