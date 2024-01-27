class GrammarHelper:

    @staticmethod
    def is_derivable(grammar, word):
        """Tests if word is accepted by grammar.
        Parameters:
        grammar: FAdo CNF (grammar in Chomskey Normal From)
        word : list (list of terminal symbols)

        Returns:
        bool (whether word is derivable)"""

        length = len(word)

        start = grammar.Start
        nonterminals = grammar.Nonterminals

        T = {start}
        while True:
            T1 = set(T)
            for w in T1:
                for i, A in enumerate(w):
                    if A in nonterminals:
                        derivatives = GrammarHelper.get_derivatives_of(grammar, A)
                        for derivative in derivatives:
                            new_word = tuple(w[:i]) + tuple(derivative) + tuple(w[i + 1:])
                            l = len(new_word)
                            if l <= length:
                                if l == 1:
                                    T.add(new_word[0])
                                else:
                                    T.add(new_word)

            if word in T or T == T1:
                break

        if word in T:
            return True
        else:
            return False


    @staticmethod
    def get_derivatives_of(grammar, nonterminal):
        """Computes derivatives of nonterminal.
        Parameters:
        grammar: FAdo CNF (grammar in Chomskey Normal From)
        nonterminal : string (nonterminal symbol of grammar)

        Returns:
        derivatives : set"""

        ntr = grammar.ntr
        rules = grammar.Rules

        derivatives = set()
        for j in ntr[nonterminal]:
            derivative = rules[j][1]
            derivatives.add(derivative)

        return derivatives