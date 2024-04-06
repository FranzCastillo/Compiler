from src.regex.direct import DirectDFA
from src.regex.operators_values import *
from src.regex.shunting_yard import ShuntingYard
from src.regex.sy_tokens import SyToken
from src.view.automaton import ViewAutomaton
from src.view.tree import ViewTree
from src.view.yalex_result import YalexResult
from src.yalex.file_parser import FileParser

import json
import os


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


def create_lexical_analyzer(header: str = "", automatons: dict = None, footer: str = "") -> None:
    """
    Create the lexical analyzer with the given automatons.
    :param automatons: {rule: [{grammar: Grammar, return: ""] }
    """
    # Create the folder for the lexical analyzer
    try:
        # If the doesn't exist, create it
        lex_path = "output/lex_analyzer"
        os.makedirs(lex_path, exist_ok=True)

        # Append the automatons to the lexical analyzer
        for rule in automatons:
            with open(f"{lex_path}/{rule}_automaton.json", "w") as file:
                json.dump(automatons[rule], file, indent=4)

        # Create the lexical analyzer (lex_main.py)
        with open("yalex/lex_analyzer_template.py", "r") as file:
            template = file.read()
            with open(f"{lex_path}/lex_main.py", "w") as lex_file:
                # Replace header and footer
                template = template.replace("# YALEX HEADER", header)
                template = template.replace("# YALEX FOOTER", footer)
                # Import the automatons JSONs
                rule_names = "["
                jsons = "["
                for rule in automatons:
                    rule_names += f"'{rule}', "
                    jsons += f"'{rule}_automaton.json', "
                rule_names = rule_names[:-2] + "]"
                jsons = jsons[:-2] + "]"
                template = template.replace("# RULE NAMES", rule_names)
                template = template.replace("# JSONS PATHS", jsons)
                lex_file.write(template)

    except Exception as e:
        raise Exception(f"Error creating the lexical analyzer: {e}")


class Controller:
    def __init__(self, regex=None):
        self.regex = regex
        self.direct_dfa = None
        self.direct_dfa_grammar = None

    def run_file(self, print_console: callable, content: str):
        try:
            file_parser = FileParser(content)
            rules = file_parser.rules
            automatons_str = {}  # {rule: [{grammar: Grammar, return: ""] }
            automatons_obj = {}
            for rule in rules:
                automatons_str[rule] = []
                automatons_obj[rule] = []
                for regex in rules[rule]:
                    self.set_regex(regex)
                    automatons_str[rule].append({
                        "automaton": self.direct_dfa_grammar.to_json(),
                        "return": rules[rule][regex]
                    })

                    self.set_regex(regex)
                    automatons_obj[rule].append({
                        "grammar": self.direct_dfa_grammar,
                        "return": rules[rule][regex]
                    })

            yalex_result = YalexResult(automatons_obj, print_console)
            yalex_result.view('output/lex_analyzer')

            header = file_parser.declarations_content
            footer = file_parser.code_content
            create_lexical_analyzer(header, automatons_str, footer)

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
