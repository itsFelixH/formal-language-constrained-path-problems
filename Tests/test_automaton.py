import unittest
import random
from graph import GraphGenerator, GraphHelper
from automaton import Automaton
from FAdo.reex import *


class TestAutomaton(unittest.TestCase):

    def test_graph_to_automaton(self):
        G = GraphGenerator.random_weighted_graph(40, 1, 50)
        Sigma = ['a', 'b']
        G = GraphGenerator.random_label(G, Sigma)
        sources = [0]
        targets = [38,39]
        automaton = Automaton.graph_to_automaton(G,sources,targets)

        self.assertEqual(len(automaton.States), G.number_of_nodes())
        self.assertEqual(len(automaton.succintTransitions()), G.number_of_edges())

        self.assertEqual(automaton.Initial, set(sources))
        self.assertEqual(automaton.Final, set(targets))

        transitions = automaton.succintTransitions()
        for u, label, v in transitions:
            self.assertEqual(label, G[int(u)][int(v)]['label'])

        for u, v, d in G.edges(data=True):
            self.assertTrue((str(u), d['label'], str(v)) in transitions)


    def test_graph_to_automaton__other(self):
        sigma = ['a', 'b', 'c', 'd', 'e']
        (G, dic) = GraphGenerator.random_weighted_labeled_grid(20, 20, 50, sigma)
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

        source = random.choice(G.nodes())
        targets = random.sample(G.nodes(), 2)
        automaton = Automaton.graph_to_automaton(G, [source], targets)

        self.assertEqual(len(automaton.States), G.number_of_nodes())
        self.assertEqual(len(automaton.succintTransitions()), G.number_of_edges())

        self.assertEqual(automaton.Initial, {source})
        self.assertEqual(automaton.Final, set(targets))

        transitions = automaton.succintTransitions()
        for u, label, v in transitions:
            self.assertEqual(label, G[int(u)][int(v)]['label'])

        for u, v, d in G.edges(data=True):
            self.assertTrue((str(u), d['label'], str(v)) in transitions)


    def test_automaton_to_graph(self):
        expected_G = GraphGenerator.random_weighted_graph(40, 0.1, 50)
        Sigma = ['a', 'b']
        expected_G = GraphGenerator.random_label(expected_G, Sigma)
        expected_sources = [0]
        expected_targets = [38, 39]
        automaton = Automaton.graph_to_automaton(expected_G, expected_sources, expected_targets)

        (G, sources, targets) = Automaton.automaton_to_graph(automaton)

        self.assertEqual(G.number_of_nodes(), len(automaton.States))
        self.assertEqual(G.number_of_edges(), len(automaton.succintTransitions()))

        self.assertEqual(sources, expected_sources)
        self.assertEqual(targets, expected_targets)

        transitions = automaton.succintTransitions()
        for u, label, v in transitions:
            self.assertEqual(label, G[int(u)][int(v)]['label'])

        for u, v, d in G.edges(data=True):
            self.assertTrue((str(u), d['label'], str(v)) in transitions)


    def test_automaton_to_graph__regex(self):
        string1 = '(a+ba)*'
        string2 = '(b+bab)*+a*'
        string3 = 'a*((b+cd)*+e)'

        automaton1 = Automaton.regex_to_automaton(string1)
        automaton2 = Automaton.regex_to_automaton(string2)
        automaton3 = Automaton.regex_to_automaton(string3)

        (G1, sources1, targets1) = Automaton.automaton_to_graph(automaton1)
        (G2, sources2, targets2) = Automaton.automaton_to_graph(automaton2)
        (G3, sources3, targets3) = Automaton.automaton_to_graph(automaton3)

        self.assertEqual(sources1, automaton1.Initial)
        self.assertEqual(sources2, automaton2.Initial)
        self.assertEqual(sources3, automaton3.Initial)

        self.assertEqual(set(targets1), automaton1.Final)
        self.assertEqual(set(targets2), automaton2.Final)
        self.assertEqual(set(targets3), automaton3.Final)

        self.assertEqual(G1.number_of_nodes(), len(automaton1.States))
        self.assertEqual(G2.number_of_nodes(), len(automaton2.States))
        self.assertEqual(G3.number_of_nodes(), len(automaton3.States))

        self.assertEqual(G1.number_of_edges(), len(automaton1.succintTransitions()))
        self.assertEqual(G2.number_of_edges(), len(automaton2.succintTransitions()))
        self.assertEqual(G3.number_of_edges(), len(automaton3.succintTransitions()))

        transitions1 = automaton1.succintTransitions()
        for u, label, v in transitions1:
            self.assertEqual(label, G1[int(u)][int(v)]['label'])
        transitions2 = automaton2.succintTransitions()
        for u, label, v in transitions2:
            self.assertEqual(label, G2[int(u)][int(v)]['label'])
        transitions3 = automaton3.succintTransitions()
        for u, label, v in transitions3:
            self.assertEqual(label, G3[int(u)][int(v)]['label'])

        for u, v, d in G1.edges(data=True):
            self.assertTrue((str(u), d['label'], str(v)) in transitions1)
        for u, v, d in G2.edges(data=True):
            self.assertTrue((str(u), d['label'], str(v)) in transitions2)
        for u, v, d in G3.edges(data=True):
            self.assertTrue((str(u), d['label'], str(v)) in transitions3)

    def test_automaton_to_graph__regex2(self):
        string1 = '0(0+1)*1'
        string2 = '1*(01*01*)*'
        string3 = '(a+b)*b(a+b)(a+b)'

        automaton1 = Automaton.regex_to_automaton(string1)
        automaton2 = Automaton.regex_to_automaton(string2)
        automaton3 = Automaton.regex_to_automaton(string3)

        (G1, sources1, targets1) = Automaton.automaton_to_graph(automaton1)
        (G2, sources2, targets2) = Automaton.automaton_to_graph(automaton2)
        (G3, sources3, targets3) = Automaton.automaton_to_graph(automaton3)

        self.assertEqual(sources1, automaton1.Initial)
        self.assertEqual(sources2, automaton2.Initial)
        self.assertEqual(sources3, automaton3.Initial)

        self.assertEqual(set(targets1), automaton1.Final)
        self.assertEqual(set(targets2), automaton2.Final)
        self.assertEqual(set(targets3), automaton3.Final)

        self.assertEqual(G1.number_of_nodes(), len(automaton1.States))
        self.assertEqual(G2.number_of_nodes(), len(automaton2.States))
        self.assertEqual(G3.number_of_nodes(), len(automaton3.States))

        self.assertEqual(G1.number_of_edges(), len(automaton1.succintTransitions()))
        self.assertEqual(G2.number_of_edges(), len(automaton2.succintTransitions()))
        self.assertEqual(G3.number_of_edges(), len(automaton3.succintTransitions()))

        transitions1 = automaton1.succintTransitions()
        for u, label, v in transitions1:
            self.assertEqual(label, G1[int(u)][int(v)]['label'])
        transitions2 = automaton2.succintTransitions()
        for u, label, v in transitions2:
            self.assertEqual(label, G2[int(u)][int(v)]['label'])
        transitions3 = automaton3.succintTransitions()
        for u, label, v in transitions3:
            self.assertEqual(label, G3[int(u)][int(v)]['label'])

        for u, v, d in G1.edges(data=True):
            self.assertTrue((str(u), d['label'], str(v)) in transitions1)
        for u, v, d in G2.edges(data=True):
            self.assertTrue((str(u), d['label'], str(v)) in transitions2)
        for u, v, d in G3.edges(data=True):
            self.assertTrue((str(u), d['label'], str(v)) in transitions3)

    def test_regex_to_automaton(self):
        string = '(a+ba)*'
        automaton = Automaton.regex_to_automaton(string)

        word_1 = "aaa"
        word_2 = "baaaaaba"
        word_3 = "ba"
        word_4 = "bababa"
        word_5 = "bbabbaaaa"

        self.assertTrue(automaton.evalWordP(word_1))
        self.assertTrue(automaton.evalWordP(word_2))
        self.assertTrue(automaton.evalWordP(word_3))
        self.assertTrue(automaton.evalWordP(word_4))
        self.assertFalse(automaton.evalWordP(word_5))

        for i in range(0, len(automaton.States)):
            self.assertTrue(i in automaton.States)


    def test_regex_to_automaton__other(self):
        string = 'a*((b+cd)*+e)'
        automaton = Automaton.regex_to_automaton(string)

        word_1 = "aaae"
        word_2 = "bcdcdb"
        word_3 = "e"
        word_4 = "ee"
        word_5 = "acdb"

        self.assertTrue(automaton.evalWordP(word_1))
        self.assertTrue(automaton.evalWordP(word_2))
        self.assertTrue(automaton.evalWordP(word_3))
        self.assertFalse(automaton.evalWordP(word_4))
        self.assertTrue(automaton.evalWordP(word_5))

        for i in range(0, len(automaton.States)):
            self.assertTrue(i in automaton.States)


    def test_product_automaton(self):
        G = GraphGenerator.random_weighted_graph(50, 1, 50)
        Sigma = ['a', 'b']
        G = GraphGenerator.random_label(G, Sigma)
        sourcesG = [0]
        targetsG = [49]
        string = '(a+ba)*'

        M_G = Automaton.graph_to_automaton(G, sourcesG, targetsG)
        M_R = Automaton.regex_to_automaton(string)

        sourceR = M_R.States[M_R.Initial]
        sourceG = M_G.States[list(M_G.Initial)[0]]
        targetsR = [M_R.States[i] for i in M_R.Final]

        source = (sourceG, sourceR)
        targets = [(x, y) for x in targetsG for y in targetsR]

        automaton = Automaton.product_automaton(M_G, M_R)

        self.assertEqual(len(automaton.States), len(M_R.States)*len(M_G.States))
        for state in automaton.States:
            self.assertTrue(state[0] in M_G.States)
            self.assertTrue(state[1] in M_R.States)

        self.assertEqual(automaton.States[list(automaton.Initial)[0]], (source[0], int(source[1])))
        for state_index in automaton.Final:
            self.assertTrue((automaton.States[state_index][0], automaton.States[state_index][1]) in targets)

        for source in automaton.delta:
            transitions = automaton.delta[source]
            for label in transitions:
                targets = transitions[label]
                for target in targets:
                    self.assertEqual(label, G[list(source)[0]][list(target)[0]]['label'])
                    self.assertTrue(M_G.hasTransitionP(source[0], label, target[0]))
                    self.assertTrue((str(source[1]), label, str(target[1])) in M_R.succintTransitions())

        transitions1 = M_G.succintTransitions()
        transitions2 = M_R.succintTransitions()
        for state in automaton.States:
            for to in automaton.States:
                for label in Sigma:
                    if ((str(state[0]), label, str(to[0])) in transitions1) and ((str(state[1]), label, str(to[1])) in transitions2):
                        self.assertTrue(automaton.hasTransitionP(state, label, to))


    def test_product_automaton__other(self):
        sigma = ['a', 'b', 'c', 'd', 'e']
        (G, dic) = GraphGenerator.random_weighted_labeled_grid(10, 10, 50, sigma)
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)
        sourcesG = [0]
        targetsG = [99]
        string1 = '(b+cae)*+d*'
        string2 = 'a*((b+cd)*+e)'

        M_G = Automaton.graph_to_automaton(G, sourcesG, targetsG)
        M_R1 = Automaton.regex_to_automaton(string1)
        M_R2 = Automaton.regex_to_automaton(string2)

        sourceG = M_G.States[list(M_G.Initial)[0]]
        sourceR1 = M_R1.States[M_R1.Initial]
        sourceR2 = M_R2.States[M_R2.Initial]

        targetsR1 = [M_R1.States[i] for i in M_R1.Final]
        targetsR2 = [M_R2.States[i] for i in M_R2.Final]

        source1 = (sourceG, sourceR1)
        source2 = (sourceG, sourceR2)

        targets1 = [(x, y) for x in targetsG for y in targetsR1]
        targets2 = [(x, y) for x in targetsG for y in targetsR2]

        automaton1 = Automaton.product_automaton(M_G, M_R1)
        automaton2 = Automaton.product_automaton(M_G, M_R2)

        self.assertEqual(len(automaton1.States), len(M_R1.States) * len(M_G.States))
        self.assertEqual(len(automaton2.States), len(M_R2.States) * len(M_G.States))

        for state in automaton1.States:
            self.assertTrue(state[0] in M_G.States)
            self.assertTrue(state[1] in M_R1.States)
        for state in automaton2.States:
            self.assertTrue(state[0] in M_G.States)
            self.assertTrue(state[1] in M_R2.States)

        self.assertEqual(automaton1.States[list(automaton1.Initial)[0]], (source1[0], int(source1[1])))
        for state_index in automaton1.Final:
            self.assertTrue((automaton1.States[state_index][0], automaton1.States[state_index][1]) in targets1)
        self.assertEqual(automaton2.States[list(automaton2.Initial)[0]], (source2[0], int(source2[1])))
        for state_index in automaton2.Final:
            self.assertTrue((automaton2.States[state_index][0], automaton2.States[state_index][1]) in targets2)

        for source in automaton1.delta:
            transitions = automaton1.delta[source]
            for label in transitions:
                targets = transitions[label]
                for target in targets:
                    self.assertEqual(label, G[list(source)[0]][list(target)[0]]['label'])
                    self.assertTrue(M_G.hasTransitionP(source[0], label, target[0]))
                    self.assertTrue((str(source[1]), label, str(target[1])) in M_R1.succintTransitions())
        for source in automaton2.delta:
            transitions = automaton2.delta[source]
            for label in transitions:
                targets = transitions[label]
                for target in targets:
                    self.assertEqual(label, G[list(source)[0]][list(target)[0]]['label'])
                    self.assertTrue(M_G.hasTransitionP(source[0], label, target[0]))
                    self.assertTrue((str(source[1]), label, str(target[1])) in M_R2.succintTransitions())

        transitionsG = M_G.succintTransitions()
        transitionsR1 = M_R1.succintTransitions()
        transitionsR2 = M_R2.succintTransitions()
        for state in automaton1.States:
            for to in automaton1.States:
                for label in sigma:
                    if ((str(state[0]), label, str(to[0])) in transitionsG) and (
                        (str(state[1]), label, str(to[1])) in transitionsR1):
                        self.assertTrue(automaton1.hasTransitionP(state, label, to))
        for state in automaton2.States:
            for to in automaton2.States:
                for label in sigma:
                    if ((str(state[0]), label, str(to[0])) in transitionsG) and (
                                (str(state[1]), label, str(to[1])) in transitionsR2):
                        self.assertTrue(automaton2.hasTransitionP(state, label, to))

    def test_product_automaton__other2(self):
        sourcesG = [0]
        targetsG = [99]
        string1 = '0(0+1)*1'
        string2 = '1*(01*01*)*'
        regex1 = str2regexp(string1)
        sigma = list(regex1.setOfSymbols())

        (G, dic) = GraphGenerator.random_weighted_labeled_grid(10, 10, 50, sigma)
        (G, dic) = GraphHelper.convert_node_labels_to_integers(G, dic)

        M_G = Automaton.graph_to_automaton(G, sourcesG, targetsG)
        M_R1 = Automaton.regex_to_automaton(string1)
        M_R2 = Automaton.regex_to_automaton(string2)

        sourceG = M_G.States[list(M_G.Initial)[0]]
        sourceR1 = M_R1.States[M_R1.Initial]
        sourceR2 = M_R2.States[M_R2.Initial]

        targetsR1 = [M_R1.States[i] for i in M_R1.Final]
        targetsR2 = [M_R2.States[i] for i in M_R2.Final]

        source1 = (sourceG, sourceR1)
        source2 = (sourceG, sourceR2)

        targets1 = [(x, y) for x in targetsG for y in targetsR1]
        targets2 = [(x, y) for x in targetsG for y in targetsR2]

        automaton1 = Automaton.product_automaton(M_G, M_R1)
        automaton2 = Automaton.product_automaton(M_G, M_R2)

        self.assertEqual(len(automaton1.States), len(M_R1.States) * len(M_G.States))
        self.assertEqual(len(automaton2.States), len(M_R2.States) * len(M_G.States))

        for state in automaton1.States:
            self.assertTrue(state[0] in M_G.States)
            self.assertTrue(state[1] in M_R1.States)
        for state in automaton2.States:
            self.assertTrue(state[0] in M_G.States)
            self.assertTrue(state[1] in M_R2.States)

        self.assertEqual(automaton1.States[list(automaton1.Initial)[0]], (source1[0], int(source1[1])))
        for state_index in automaton1.Final:
            self.assertTrue((automaton1.States[state_index][0], automaton1.States[state_index][1]) in targets1)
        self.assertEqual(automaton2.States[list(automaton2.Initial)[0]], (source2[0], int(source2[1])))
        for state_index in automaton2.Final:
            self.assertTrue((automaton2.States[state_index][0], automaton2.States[state_index][1]) in targets2)

        for source in automaton1.delta:
            transitions = automaton1.delta[source]
            for label in transitions:
                targets = transitions[label]
                for target in targets:
                    self.assertEqual(label, G[list(source)[0]][list(target)[0]]['label'])
                    self.assertTrue(M_G.hasTransitionP(source[0], label, target[0]))
                    self.assertTrue((str(source[1]), label, str(target[1])) in M_R1.succintTransitions())
        for source in automaton2.delta:
            transitions = automaton2.delta[source]
            for label in transitions:
                targets = transitions[label]
                for target in targets:
                    self.assertEqual(label, G[list(source)[0]][list(target)[0]]['label'])
                    self.assertTrue(M_G.hasTransitionP(source[0], label, target[0]))
                    self.assertTrue((str(source[1]), label, str(target[1])) in M_R2.succintTransitions())

        transitionsG = M_G.succintTransitions()
        transitionsR1 = M_R1.succintTransitions()
        transitionsR2 = M_R2.succintTransitions()
        for state in automaton1.States:
            for to in automaton1.States:
                for label in sigma:
                    if ((str(state[0]), label, str(to[0])) in transitionsG) and (
                                (str(state[1]), label, str(to[1])) in transitionsR1):
                        self.assertTrue(automaton1.hasTransitionP(state, label, to))
        for state in automaton2.States:
            for to in automaton2.States:
                for label in sigma:
                    if ((str(state[0]), label, str(to[0])) in transitionsG) and (
                                (str(state[1]), label, str(to[1])) in transitionsR2):
                        self.assertTrue(automaton2.hasTransitionP(state, label, to))