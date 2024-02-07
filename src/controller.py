from src.regex.shunting_yard import ShuntingYard
from src.regex.nfa import NFA
from src.regex.dfa import DFA
from src.regex.min_dfa import MinifiedDFA
from src.view.automaton import ViewAutomaton


class Controller:
    def __init__(self):
        self.regex = None
        self.chain = None
        self.nfa_grammar = None
        self.dfa_grammar = None
        self.min_dfa_grammar = None

        # Flag to check if the grammars have been processed.
        # Allowing the grammars to be viewed only after they have been processed. (When they are not None)
        self.grammars_processed = False

        # Object to create the PDFs of the automata
        self.automaton_viewer = ViewAutomaton()

    def run(self):
        self.process_grammars()
        self.view_nfa("nfa")
        self.view_dfa("dfa")
        self.view_min_dfa("min_dfa")

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

        self.grammars_processed = True

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
