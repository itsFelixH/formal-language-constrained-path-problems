import unittest
from FAdo.cfg import *
from grammarhelper import GrammarHelper


class GrammarHelperTest(unittest.TestCase):

    def test_is_derivable(self):
        productions = [('S', ('A')), ('A', ('x', 'A', 'y')), ('A', ('x', 'B', 'y')), ('B', ('z'))]
        G = CFGrammar(productions)

        productions2 = [('S', ('S', 'S')), ('S', ('a', 'S', 'b')), ('S', ('c'))]
        G2 = CFGrammar(productions2)

        word1 = ('x', 'z', 'y')
        word2 = ('x', 'x', 'x', 'z', 'y', 'y', 'y')
        word3 = ('x', 'x', 'z', 'y')
        word4 = ('x', 'y')
        word5 = 'z'

        word6 = 'c'
        word7 = ('a', 'c', 'b')
        word8 = ('a', 'c', 'b', 'a', 'c', 'b')
        word9 = ('a', 'b')
        word10 = ('a', 'a', 'b')


        self.assertTrue(GrammarHelper.is_derivable(G, word1))
        self.assertTrue(GrammarHelper.is_derivable(G, word2))
        self.assertFalse(GrammarHelper.is_derivable(G, word3))
        self.assertFalse(GrammarHelper.is_derivable(G, word4))
        self.assertFalse(GrammarHelper.is_derivable(G, word5))

        self.assertTrue(GrammarHelper.is_derivable(G2, word6))
        self.assertTrue(GrammarHelper.is_derivable(G2, word7))
        self.assertTrue(GrammarHelper.is_derivable(G2, word8))
        self.assertFalse(GrammarHelper.is_derivable(G2, word9))
        self.assertFalse(GrammarHelper.is_derivable(G2, word10))

    def test_is_derivable__cnf(self):
        productions = [('S', ('A')), ('A', ('x', 'A', 'y')), ('A', ('x', 'B', 'y')), ('B', ('z'))]
        G = CNF(productions)

        G.makenonterminals()
        G.maketerminals()
        G.nonterminalrules()

        word1 = ('x', 'z', 'y')
        word2 = ('x', 'x', 'x', 'z', 'y', 'y', 'y')
        word3 = ('x', 'x', 'z', 'y')
        word4 = ('x', 'y')
        word5 = 'z'

        self.assertTrue(GrammarHelper.is_derivable(G, word1))
        self.assertTrue(GrammarHelper.is_derivable(G, word2))
        self.assertFalse(GrammarHelper.is_derivable(G, word3))
        self.assertFalse(GrammarHelper.is_derivable(G, word4))
        self.assertFalse(GrammarHelper.is_derivable(G, word5))

    def test_get_derivatives_of(self):
        productions = [('S', ('A')), ('A', ('x', 'A', 'y')), ('A', ('x', 'B', 'y')), ('B', ('z'))]
        G = CFGrammar(productions)

        nonterminals = G.Nonterminals
        terminals = G.Terminals

        derivatives_of_S = GrammarHelper.get_derivatives_of(G, 'S')
        derivatives_of_A = GrammarHelper.get_derivatives_of(G, 'A')
        derivatives_of_B = GrammarHelper.get_derivatives_of(G, 'B')

        self.assertEqual(derivatives_of_S, {'A'})
        self.assertEqual(derivatives_of_A, {('x', 'A', 'y'), ('x', 'B', 'y')})
        self.assertEqual(derivatives_of_B, {'z'})

        for derivative in derivatives_of_S | derivatives_of_A | derivatives_of_B:
            if isinstance(derivative, str):
                self.assertTrue(derivative in nonterminals or derivative in terminals)
            elif isinstance(derivative, tuple):
                for symbol in derivative:
                    self.assertTrue(symbol in nonterminals or symbol in terminals)

    def test_get_derivatives_of__cnf(self):
        productions = [('S', ('S', 'S')), ('S', ('a', 'S', 'b')), ('S', ('c'))]
        G = CNF(productions)

        G.makenonterminals()
        nonterminals = G.Nonterminals
        G.maketerminals()
        terminals = G.Terminals
        G.nonterminalrules()

        derivatives_of_S = GrammarHelper.get_derivatives_of(G, 'S')
        derivatives_of_A0 = GrammarHelper.get_derivatives_of(G, 'A@_0')
        derivatives_of_Aa = GrammarHelper.get_derivatives_of(G, 'A@a')
        derivatives_of_Ab = GrammarHelper.get_derivatives_of(G, 'A@b')

        self.assertEqual(derivatives_of_S, {('S', 'S'), ('A@a', 'A@_0'), 'c'})
        self.assertEqual(derivatives_of_A0, {('S', 'A@b')})
        self.assertEqual(derivatives_of_Aa, {'a'})
        self.assertEqual(derivatives_of_Ab, {'b'})

        for derivative in derivatives_of_S:
            if isinstance(derivative, str):
                self.assertTrue(derivative in nonterminals or derivative in terminals)
            elif isinstance(derivative, tuple):
                for symbol in derivative:
                    self.assertTrue(symbol in nonterminals or symbol in terminals)