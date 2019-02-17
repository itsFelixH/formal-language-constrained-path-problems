import networkx as nx
from FAdo.reex import *
from FAdo.fio import *


class Automaton:

    @staticmethod
    def graph_to_automaton(G, sources, targets):
        """Covert graph G to equivalent NFA.
        Parameters:
        G : NetworkX graph
        sources : list of nodes (Starting nodes)
        targets : list of nodes (Ending nodes)

        Returns:
        automaton : FAdo NFA (NFA representing graph G)"""

        automaton = NFA()

        for node in G.nodes():
            if node in sources:
                i_source = automaton.addState(node)
                automaton.addInitial(i_source)
            elif node in targets:
                i_target = automaton.addState(node)
                automaton.addFinal(i_target)
            else:
                automaton.addState(node)

        for u, v, data in G.edges(data=True):
            automaton.addSigma(G[u][v]['label'])
            automaton.addTransition(int(u), str(G[u][v]['label']), int(v))

        return automaton

    @staticmethod
    def automaton_to_graph(automaton):
        """Covert NFA automaton to equivalent graph G.
        Parameters:
        automaton : FAdo NFA

        Returns:
        G : NetworkX graph (Graph representing NFA automaton)
        sources : list of nodes (Starting nodes)
        targets : list of nodes (Ending nodes)"""

        dfa = 0
        if isinstance(automaton, DFA):
            dfa = 1
        Graph = nx.DiGraph()

        states = automaton.States
        for state in states:
            Graph.add_node(state)

        for u in automaton.delta:
            for symbol in automaton.delta[u]:
                vs = automaton.delta[u][symbol]
                if dfa:
                    Graph.add_edge(u, vs, {'label': symbol})
                else:
                    for v in vs:
                        Graph.add_edge(u, v, {'label': symbol})

        if dfa:
            sources = states[automaton.Initial]
        else:
            sources = []
            for i in automaton.Initial:
                sources.append(states[i])

        targets = []
        for i in automaton.Final:
            targets.append(states[i])

        return Graph, sources, targets

    @staticmethod
    def regex_to_automaton(regex_str):
        """Covert graph G to equivalent NFA.
        Parameters:
        regex_str : string (String representing regular expression)

        Returns:
        automaton : FAdo NFA (NFA for regular expression regex_str)"""

        regex = str2regexp(regex_str)
        automaton = regex.nfaPosition().toDFA().minimal(complete=False)
        automaton.renameStates(range(0, len(automaton.States)))

        return automaton

    @staticmethod
    def product_automaton(weighted_automaton, other_automaton):
        """Compute product of NFA and DFA.
        Parameters:
        weighted_automaton : FAdo NFA
        other_automaton : FAdo DFA

        Returns:
        automaton : FAdo NFA (product NFA of weighted_automaton and other_automaton)"""

        source = (list(weighted_automaton.Initial)[0], other_automaton.Initial)
        targets = [(int(x), int(y)) for x in weighted_automaton.Final for y in other_automaton.Final]

        automaton = NFA()
        states = [(int(x), int(y)) for x in weighted_automaton.States for y in other_automaton.States]
        for state in states:
            if state == source:
                i_source = automaton.addState(state)
                automaton.addInitial(i_source)
            elif state in targets:
                i_target = automaton.addState(state)
                automaton.addFinal(i_target)
            else:
                automaton.addState(state)

        transitions1 = dict()
        for u in weighted_automaton.delta:
            for symbol in weighted_automaton.delta[u]:
                for v in weighted_automaton.delta[u][symbol]:
                    k = (u, v)
                    if k not in transitions1:
                        transitions1[k] = []
                    transitions1[k].append(symbol)

        transitions2 = dict()
        for u in other_automaton.delta:
            for symbol in other_automaton.delta[u]:
                v = other_automaton.delta[u][symbol]
                k = (u, v)
                if k not in transitions2:
                    transitions2[k] = []
                transitions2[k].append(symbol)

        for u1, v1 in transitions1:
            symlist1 = transitions1[(u1, v1)]
            for u2, v2 in transitions2:
                symlist2 = transitions2[(u2, v2)]
                for symbol in symlist1:
                    if symbol in symlist2:
                        automaton.addTransition((u1, u2), symbol, (v1, v2))

        return automaton