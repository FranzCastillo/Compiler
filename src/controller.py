from src.regex.dfa import DFA
from src.regex.direct import DirectDFA
from src.regex.min_dfa import MinifiedDFA
from src.regex.nfa import NFA
from src.regex.operators_values import *
from src.regex.shunting_yard import ShuntingYard
from src.view.automaton import ViewAutomaton
from src.view.tree import ViewTree


def replace_postfix(postfix):
    """
    Replaces x? with xε| and x+ with xx*.
    """
    stack = []
    for char in postfix:
        if char in unary_operators:
            right = stack.pop()
            if char == QUESTION_MARK:
                stack.append(f"{right}{EPSILON}{UNION}")
            elif char == KLEENE_PLUS:
                stack.append(f"{right}{right}{KLEENE_STAR}{CONCAT}")
            else:
                stack.append(f"{right}{char}")
        elif char in operators:
            right = stack.pop()
            left = stack.pop()
            stack.append(f"{left}{right}{char}")
        else:
            stack.append(char)
    return stack.pop()


def remove_comments(content):
    result = ""
    in_comment = False
    i = 0
    while i < len(content):
        if content[i:i + 2] == '(*':
            in_comment = True
            i += 2
        elif content[i:i + 2] == '*)':
            in_comment = False
            i += 2
        elif not in_comment:
            result += content[i]
            i += 1
        else:
            i += 1
    return result


class Controller:
    def __init__(self, regex=None):
        self.regex = regex
        self.postfix = None
        self.nfa_grammar = None
        self.dfa_grammar = None
        self.min_dfa_grammar = None
        self.direct_dfa = None
        self.direct_dfa_grammar = None
        self.min_direct_dfa_grammar = None

        # Flag to check if the grammars have been processed.
        # Allowing the grammars to be viewed only after they have been processed. (When they are not None)
        self.grammars_processed = False

        self.declarations = None
        self.rules = None
        self.code = None

        try:
            # Object to create the PDFs of the automata
            self.automaton_viewer = ViewAutomaton()
            self.tree_viewer = ViewTree()
            # self.process_grammars()
        except Exception as e:
            print(e)

    def run_file(self, print_console: callable, content: str):
        content = content.strip()
        if not content:
            raise Exception("Empty file")
        content = remove_comments(content)
        print_console(content)
        d, r, c = content.split("%%")
        self.declarations = d.strip()
        self.rules = r.strip()
        self.code = c.strip()
        #
        # rules = self.rules.split("\n")
        # for rule in rules:
        #     rule.strip()
        #     if not rule:
        #         continue
        #     self.create_rule(rule)

    def view_automatons(self):
        try:
            self.view_nfa("NFA")
            self.view_dfa("DFA")
            self.view_min_dfa("MIN_DFA")
            self.view_direct_dfa("DIRECT_DFA")
            self.view_min_direct_dfa("MIN_DIRECT_DFA")
        except Exception as e:
            print(e)

    def view_syntax_tree(self):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't view syntax tree.")
        self.tree_viewer.set_tree(self.direct_dfa.syntax_tree)
        self.tree_viewer.view("SYNTAX_TREE")

    def set_regex(self, regex):
        self.regex = regex
        self.process_grammars()

    def process_grammars(self):
        try:
            if not self.regex:
                raise Exception("Regex not set")
            # if check_operators_together(self.regex):
            #     raise Exception("Invalid Regex. Operators together")
            sy = ShuntingYard()
            sy.set_regex(self.regex)
            postfix = sy.get_postfix()
            self.postfix = replace_postfix(postfix)

            nfa = NFA(self.postfix)
            self.nfa_grammar = nfa.get_grammar()

            dfa = DFA(self.nfa_grammar)
            self.dfa_grammar = dfa.get_grammar(show_death_state=False)

            min_dfa = MinifiedDFA(self.dfa_grammar)
            self.min_dfa_grammar = min_dfa.get_grammar()

            self.direct_dfa = DirectDFA(self.postfix)
            self.direct_dfa_grammar = self.direct_dfa.get_grammar()

            self.min_direct_dfa_grammar = MinifiedDFA(self.direct_dfa_grammar).get_grammar()

            self.grammars_processed = True
        except Exception as e:
            print(e)

    def chain_accepted_nfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't check if chain is accepted (NFA)")
        return self.nfa_grammar.is_accepted(string)

    def chain_accepted_dfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't check if chain is accepted (DFA)")
        return self.dfa_grammar.is_accepted(string)

    def chain_accepted_min_dfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't check if chain is accepted (Min DFA)")
        return self.min_dfa_grammar.is_accepted(string)

    def chain_accepted_direct_dfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't check if chain is accepted (Direct DFA)")
        return self.direct_dfa_grammar.is_accepted(string)

    def chain_accepted_min_direct_dfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't check if chain is accepted (Min Direct DFA)")
        return self.min_direct_dfa_grammar.is_accepted(string)

    def simulate_nfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't simulate (NFA)")
        return self.nfa_grammar.simulate(string)

    def simulate_dfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't simulate (DFA)")
        return self.dfa_grammar.simulate(string)

    def simulate_min_dfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't simulate (Min DFA)")
        return self.min_dfa_grammar.simulate(string)

    def simulate_direct_dfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't simulate (Direct DFA)")
        return self.direct_dfa_grammar.simulate(string)

    def simulate_min_direct_dfa(self, string):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't simulate (Min Direct DFA)")
        return self.min_direct_dfa_grammar.simulate(string)

    def view_nfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't view NFA.")

        self.automaton_viewer.set_grammar(self.nfa_grammar)
        self.automaton_viewer.view(output_name)

    def view_dfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't view DFA.")

        self.automaton_viewer.set_grammar(self.dfa_grammar)
        self.automaton_viewer.view(output_name)

    def view_min_dfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't view Min DFA.")

        self.automaton_viewer.set_grammar(self.min_dfa_grammar)
        self.automaton_viewer.view(output_name)

    def view_direct_dfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't view Direct DFA.")

        self.automaton_viewer.set_grammar(self.direct_dfa_grammar)
        self.automaton_viewer.view(output_name)

    def view_min_direct_dfa(self, output_name):
        if not self.grammars_processed:
            raise Exception("Grammars not processed. Can't view Min Direct DFA.")

        self.automaton_viewer.set_grammar(self.min_direct_dfa_grammar)
        self.automaton_viewer.view(output_name)
