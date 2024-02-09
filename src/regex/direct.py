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
    next_pos_table = []  # tag, symbol, next_pos
    for char in regex:
        if char not in operators:
            if char == EPSILON:
                stack.append(Node(char, tag=EPSILON))
            else:
                stack.append(Node(char, tag=tag))
                next_pos_table.append({"tag": tag, "symbol": char, "next_pos": set()})
                tag += 1
        else:
            if char in unary_operators:
                left = stack.pop()
                if char == KLEENE_STAR:
                    node = Node(char, left)
                    node.nullable = True
                    node.first_pos = left.first_pos
                    node.last_pos = left.last_pos
                    stack.append(node)

                    # Fill the next_pos_table
                    for pos in left.last_pos:
                        next_pos_table[pos - 1]["next_pos"].update(left.first_pos)
                else:
                    stack.append(Node(char, left, tag=tag))
                    tag += 1
            else:  # Binary operator
                right = stack.pop()
                left = stack.pop()

                node = Node(char, left, right)
                if char == UNION:
                    node.nullable = left.nullable or right.nullable
                    node.first_pos = left.first_pos.union(right.first_pos)
                    node.last_pos = left.last_pos.union(right.last_pos)
                elif char == CONCAT:
                    node.nullable = left.nullable and right.nullable
                    if left.nullable:
                        node.first_pos = left.first_pos.union(right.first_pos)
                    else:
                        node.first_pos = left.first_pos

                    if right.nullable:
                        node.last_pos = left.last_pos.union(right.last_pos)
                    else:
                        node.last_pos = right.last_pos

                    # Fill the next_pos_table
                    for pos in left.last_pos:
                        next_pos_table[pos - 1]["next_pos"].update(right.first_pos)

                stack.append(node)

    return stack.pop(), next_pos_table


class DirectDFA:
    def __init__(self, regex):
        self.regex = regex
        self.postfix_regex = get_postfix(regex)
        self.augmented_regex = self.postfix_regex + Operator.AUGMENTED.symbol + CONCAT
        self.syntax_tree, self.next_pos_table = build_syntax_tree(self.augmented_regex)
