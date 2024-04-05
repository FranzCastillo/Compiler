from src.regex.direct import DirectDFA
from src.regex.operators_values import *
from src.regex.shunting_yard import ShuntingYard
from src.regex.sy_tokens import SyToken
from src.view.automaton import ViewAutomaton
from src.view.tree import ViewTree
from src.view.yalex_result import YalexResult
from src.yalex.file_parser import FileParser


def replace_postfix(postfix):
    """
    Replaces x? with xε| and x+ with xx*.
    """
    try:
        stack = []
        for token in postfix:
            if token.value in unary_operators:
                right = stack.pop()
                if token.value == QUESTION_MARK:
                    temp = []
                    for inside_token in right:
                        temp.append(inside_token)
                    temp.append(SyToken('CHAR', EPSILON))
                    temp.append(SyToken('OP', UNION))
                    stack.append(temp)
                elif token.value == KLEENE_PLUS:
                    # stack.append([right, right, KLEENE_STAR, CONCAT])
                    temp = []
                    for inside_token in right:
                        temp.append(inside_token)
                    for inside_token in right:
                        temp.append(inside_token)
                    temp.append(SyToken('OP', KLEENE_STAR))
                    temp.append(SyToken('OP', CONCAT))
                    stack.append(temp)
                else:
                    # stack.append([right, token.value])
                    temp = []
                    for inside_token in right:
                        temp.append(inside_token)
                    temp.append(token)
                    stack.append(temp)
            elif token.value in operators:
                right = stack.pop()
                left = stack.pop()
                # stack.append([left, right, token])
                temp = []
                for inside_token in left:
                    temp.append(inside_token)
                for inside_token in right:
                    temp.append(inside_token)
                temp.append(token)
                stack.append(temp)
            else:
                stack.append([token])
        return stack[0]
    except Exception:
        raise Exception(f"Syntax Error. Can't parse: {postfix}")


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

        # Object to create the PDFs of the automata
        self.automaton_viewer = ViewAutomaton()
        self.tree_viewer = ViewTree()

    def run_file(self, print_console: callable, content: str):
        try:
            file_parser = FileParser(content)
            rules = file_parser.rules
            grammars = {}  # {rule: [{grammar: Grammar, return: ""] }
            for rule in rules:
                grammars[rule] = []
                for regex in rules[rule]:
                    self.set_regex(regex)
                    grammars[rule].append({
                        "grammar": self.direct_dfa_grammar,
                        "return": rules[rule][regex]
                    })

            yalex_result = YalexResult(grammars, print_console)
            yalex_result.view()

        except Exception as e:
            print_console(f"Error: {e}")

    def set_regex(self, regex):
        self.regex = regex
        self.process_grammars()

    def process_grammars(self):
        if not self.regex:
            raise Exception("Regex not set")
        sy = ShuntingYard()
        sy.set_regex(self.regex)
        postfix = sy.get_postfix()
        self.postfix = replace_postfix(postfix)

        direct_dfa = DirectDFA(self.postfix)
        self.direct_dfa_grammar = direct_dfa.get_grammar()

        self.grammars_processed = True
