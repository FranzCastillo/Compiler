from src.regex.operators_values import *
from src.regex.shunting_yard import ShuntingYard
from src.structures.node import Node


def get_postfix(regex):
    """
    Get the postfix notation of the regular expression.
    :param regex:
    :return:
    """
    sy = ShuntingYard()
    sy.set_regex(regex)
    return sy.get_postfix()


def build_syntax_tree(regex):
    """
    Build the syntax tree of the regular expression.
    :param regex:
    :return:
    """
    stack = []

    for char in regex:
        if char not in operators:
            stack.append(Node(char))
        else:
            if char in unary_operators:
                right = stack.pop()
                stack.append(Node(char, right))
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(Node(char, left, right))

    return stack.pop()


class DirectDFA:
    def __init__(self, regex):
        self.regex = regex
        self.postfix_regex = get_postfix(regex)
        self.augmented_regex = self.postfix_regex + Operator.AUGMENTED.symbol + CONCAT
        self.syntax_tree = build_syntax_tree(self.augmented_regex)
