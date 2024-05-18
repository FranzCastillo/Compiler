import json
import os

from src.regex.direct import DirectDFA
from src.regex.grammar import Grammar
from src.regex.operators_values import *
from src.regex.shunting_yard import ShuntingYard
from src.regex.sy_tokens import SyToken
from src.yalex.file_parser import FileParser


def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def replace_postfix(postfix: list):
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


def process_regex(regex: str) -> Grammar:
    sy = ShuntingYard()
    sy.set_regex(regex)
    postfix = sy.get_postfix()
    postfix = replace_postfix(postfix)

    direct_dfa = DirectDFA(postfix)
    direct_dfa_grammar = direct_dfa.get_grammar()

    return direct_dfa_grammar


def build_str_automatons(rules: dict) -> str:
    try:
        automatons_str = {}  # {rule: [{grammar: Grammar, return: ""] }
        for rule in rules:
            automatons_str[rule] = []
            for regex in rules[rule]:
                direct_dfa_grammar = process_regex(regex)
                automatons_str[rule].append({"automaton": direct_dfa_grammar.to_json(), "return": rules[rule][regex]})

        return automatons_str
    except Exception as e:
        raise Exception(f"Can't building the string automatons: {e}")


def get_token_types(automatons_str: dict) -> set:
    token_types = set()
    for rule in automatons_str:
        for automaton in automatons_str[rule]:
            token_types.add(automaton["return"])
    return token_types


def create_lex_file(header: str, automatons: dict, footer: str, output_path: str) -> None:
    """
    Create the lexical analyzer with the given automatons.
    :param header: Header of the lexical analyzer
    :param automatons: {rule: [{grammar: Grammar, return: ""] }
    :param footer: Footer of the lexical analyzer
    :param output_path: Path to save the lexical analyzer
    """
    # Create the folder for the lexical analyzer
    try:
        # If the doesn't exist, create it
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Append the automatons to the lexical analyzer
        for rule in automatons:
            with open(f"{output_path}/{rule}_automaton.json", "w") as file:
                json.dump(automatons[rule], file, indent=4)

        with open("templates/yalex_template.py", "r") as file:
            template = file.read()
            with open(f"{output_path}/lexical_analyzer.py", "w") as lex_file:
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
        raise Exception(f"Can't create File: {e}")


class Factory:
    def __init__(self, yalex_file_path: str, output_path: str):
        self.yalex_file_path = yalex_file_path
        self.output_path = output_path

    def create_lex_analyzer(self):
        try:
            header, automatons_str, footer = self.parse_file()
            create_lex_file(header, automatons_str, footer, self.output_path)
            return get_token_types(automatons_str)
        except Exception as e:
            raise Exception(f"Error creating the Lexical Analyzer: {e}")

    def parse_file(self) -> tuple:
        try:
            # Since the parameter asks for the content of the file
            file_parser = FileParser(read_file(self.yalex_file_path))

            header = file_parser.declarations_content
            automatons_str = build_str_automatons(file_parser.rules)
            footer = file_parser.code_content
            return header, automatons_str, footer
        except Exception as e:
            raise Exception(f"Can't parse the file: {e}")
