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
    tag = 1
    for char in regex:
        if char not in operators:
            if char == EPSILON:
                stack.append(Node(char, tag=EPSILON))
            else:
                stack.append(Node(char, tag=tag))
                tag += 1
        else:
            if char in unary_operators:
                left = stack.pop()
                if char == KLEENE_STAR:
                    node = Node(char, left)
                    node.nullable = True
                    stack.append(node)
                else:
                    stack.append(Node(char, left, tag=tag))
                    tag += 1
            else:  # Binary operator
                right = stack.pop()
                left = stack.pop()

                node = Node(char, left, right)
                if char == UNION:
                    node.nullable = left.nullable or right.nullable
                elif char == CONCAT:
                    node.nullable = left.nullable and right.nullable

                stack.append(node)

    return stack.pop()


class DirectDFA:
    def __init__(self, regex):
        self.regex = regex
        self.postfix_regex = get_postfix(regex)
        self.augmented_regex = self.postfix_regex + Operator.AUGMENTED.symbol + CONCAT
        self.syntax_tree = build_syntax_tree(self.augmented_regex)

