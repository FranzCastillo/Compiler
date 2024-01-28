from enum import Enum


class Operator(Enum):
    EPSILON = 'ε'
    KLEENE_STAR = '*'
    CONCAT = '.'
    UNION = '|'
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
