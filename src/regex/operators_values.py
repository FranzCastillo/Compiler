from src.regex.operators import Operator

AUGMENTED = Operator.AUGMENTED.symbol
EPSILON = Operator.EPSILON.symbol
KLEENE_STAR = Operator.KLEENE_STAR.symbol
KLEENE_PLUS = Operator.KLEENE_PLUS.symbol
QUESTION_MARK = Operator.QUESTION_MARK.symbol
CONCAT = Operator.CONCAT.symbol
UNION = Operator.UNION.symbol
OPEN_PAREN = Operator.OPEN_PAREN.symbol
CLOSE_PAREN = Operator.CLOSE_PAREN.symbol
OPEN_BRACKET = Operator.OPEN_BRACKET.symbol
CLOSE_BRACKET = Operator.CLOSE_BRACKET.symbol

operators = [KLEENE_STAR, CONCAT, UNION, KLEENE_PLUS, QUESTION_MARK, KLEENE_PLUS]
unary_operators = [KLEENE_STAR, QUESTION_MARK, KLEENE_PLUS]
escape_characters = [
    AUGMENTED, EPSILON, KLEENE_STAR,
    KLEENE_PLUS, QUESTION_MARK, CONCAT,
    UNION, OPEN_PAREN, CLOSE_PAREN,
    OPEN_BRACKET, CLOSE_BRACKET,
]

precedence = {
    QUESTION_MARK: Operator.QUESTION_MARK.precedence,
    KLEENE_PLUS: Operator.KLEENE_PLUS.precedence,
    KLEENE_STAR: Operator.KLEENE_STAR.precedence,
    CONCAT: Operator.CONCAT.precedence,
    UNION: Operator.UNION.precedence,
    OPEN_PAREN: Operator.OPEN_PAREN.precedence,
    CLOSE_PAREN: Operator.CLOSE_PAREN.precedence
}

associativity = {
    QUESTION_MARK: Operator.QUESTION_MARK.associativity,
    KLEENE_PLUS: Operator.KLEENE_PLUS.associativity,
    KLEENE_STAR: Operator.KLEENE_STAR.associativity,
    CONCAT: Operator.CONCAT.associativity,
    UNION: Operator.UNION.associativity,
    OPEN_PAREN: Operator.OPEN_PAREN.associativity,
    CLOSE_PAREN: Operator.CLOSE_PAREN.associativity
}
