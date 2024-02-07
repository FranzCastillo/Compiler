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
        self.grammars_processed = False

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

        view = ViewAutomaton(self.nfa_grammar)
        view.view(output_name)

    def view_dfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed")

        view = ViewAutomaton(self.dfa_grammar)
        view.view(output_name)

    def view_min_dfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed")

        view = ViewAutomaton(self.min_dfa_grammar)
        view.view(output_name)
