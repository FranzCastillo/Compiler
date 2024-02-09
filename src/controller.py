from src.regex.shunting_yard import ShuntingYard
from src.regex.nfa import NFA
from src.regex.dfa import DFA
from src.regex.min_dfa import MinifiedDFA
from src.view.automaton import ViewAutomaton
from src.view.tree import ViewTree
from src.regex.direct import DirectDFA


class Controller:
    def __init__(self, regex=None):
        self.regex = regex
        self.nfa_grammar = None
        self.dfa_grammar = None
        self.min_dfa_grammar = None
        self.direct_dfa = None

        # Flag to check if the grammars have been processed.
        # Allowing the grammars to be viewed only after they have been processed. (When they are not None)
        self.grammars_processed = False

        # Object to create the PDFs of the automata
        self.automaton_viewer = ViewAutomaton()
        self.tree_viewer = ViewTree()

        self.process_grammars()

    def view_automatons(self):
        self.view_nfa("nfa")
        self.view_dfa("dfa")
        self.view_min_dfa("min_dfa")
        self.view_direct_dfa("direct_syntax_tree")

    def set_regex(self, regex):
        self.regex = regex
        self.process_grammars()

    def process_grammars(self):
        if not self.regex:
            raise Exception("Regex not set")

        sy = ShuntingYard()
        sy.set_regex(self.regex)
        postfix = sy.get_postfix()

        nfa = NFA(postfix)
        self.nfa_grammar = nfa.get_grammar()

        dfa = DFA(self.nfa_grammar)
        self.dfa_grammar = dfa.get_grammar(show_death_state=False)

        min_dfa = MinifiedDFA(self.dfa_grammar)
        self.min_dfa_grammar = min_dfa.get_grammar()

        direct_dfa = DirectDFA(self.regex)
        self.direct_dfa = direct_dfa.syntax_tree

        self.grammars_processed = True

    def chain_accepted_nfa(self, string):
        return self.nfa_grammar.is_accepted(string)

    def chain_accepted_dfa(self, string):
        return self.dfa_grammar.is_accepted(string)

    def chain_accepted_min_dfa(self, string):
        return self.min_dfa_grammar.is_accepted(string)

    def simulate_nfa(self, string):
        return self.nfa_grammar.simulate(string)

    def simulate_dfa(self, string):
        return self.dfa_grammar.simulate(string)

    def simulate_min_dfa(self, string):
        return self.min_dfa_grammar.simulate(string)

    def view_nfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed")

        self.automaton_viewer.set_grammar(self.nfa_grammar)
        self.automaton_viewer.view(output_name)

    def view_dfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed")

        self.automaton_viewer.set_grammar(self.dfa_grammar)
        self.automaton_viewer.view(output_name)

    def view_min_dfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed")

        self.automaton_viewer.set_grammar(self.min_dfa_grammar)
        self.automaton_viewer.view(output_name)

    def view_direct_dfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed")

        self.tree_viewer.set_tree(self.direct_dfa)
        self.tree_viewer.view(output_name)
