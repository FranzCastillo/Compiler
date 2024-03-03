from enum import Enum


class Operator(Enum):
    AUGMENTED = ('#', None, None)
    EPSILON = ('ε', None, None)
    KLEENE_STAR = ('*', 3, 'left')
    KLEENE_PLUS = ('+', 3, 'left')
    QUESTION_MARK = ('?', 3, 'left')
    CONCAT = ('.', 2, 'left')
    UNION = ('|', 1, 'left')
    OPEN_PAREN = ('(', 0, None)
    CLOSE_PAREN = (')', 0, None)
    OPEN_BRACKET = ('[', 0, None)
    CLOSE_BRACKET = (']', 0, None)

    def __init__(self, symbol, precedence, associativity):
        self.symbol = symbol
        self.precedence = precedence
        self.associativity = associativity
