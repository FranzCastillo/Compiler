from enum import Enum


class Operator(Enum):
    EPSILON = ('ε', None, None)
    KLEENE_STAR = ('*', 3, 'right')
    CONCAT = ('.', 2, 'left')
    UNION = ('|', 1, 'left')
    OPEN_PAREN = ('(', 0, None)
    CLOSE_PAREN = (')', 0, None)

    def __init__(self, symbol, precedence, associativity):
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity
