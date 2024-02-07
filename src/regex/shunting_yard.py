from src.regex.operators import Operator

EPSILON = Operator.EPSILON.symbol
KLEENE_STAR = Operator.KLEENE_STAR.symbol
KLEENE_PLUS = Operator.KLEENE_PLUS.symbol
QUESTION_MARK = Operator.QUESTION_MARK.symbol
CONCAT = Operator.CONCAT.symbol
UNION = Operator.UNION.symbol
OPEN_PAREN = Operator.OPEN_PAREN.symbol
CLOSE_PAREN = Operator.CLOSE_PAREN.symbol

operators = [KLEENE_STAR, CONCAT, UNION, KLEENE_PLUS ]

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


def get_alphabet(regex):
    """
    Get the alphabet of a regular expression. With an initial epsilon character.
    :param regex:
    :return:
    """
    alphabet = set()
    operators = precedence.keys()
    for char in regex:
        if char not in operators:
            alphabet.add(char)
    alphabet.add(EPSILON)
    return alphabet


def insert_concat_operator(regex):
    """
    Insert the concatenation operator '.' into the regular expression.
    :param regex:
    :return:
    """
    operators = precedence.keys()
    new_regex = ''
    length = len(regex)
    for i in range(length):
        new_regex += regex[i]
        if i < length - 1:
            should_concat = False
            current_char = regex[i]
            next_char = regex[i + 1]
            if current_char not in operators and next_char not in operators:
                should_concat = True
            elif current_char == CLOSE_PAREN and next_char not in operators:
                should_concat = True
            elif current_char not in operators and next_char == OPEN_PAREN:
                should_concat = True
            elif (current_char == KLEENE_STAR or current_char == KLEENE_PLUS or current_char == QUESTION_MARK) and (next_char not in operators or next_char == OPEN_PAREN):
                should_concat = True

            if should_concat:
                new_regex += CONCAT

    return new_regex


class ShuntingYard:
    """
    The Shunting Yard algorithm for converting infix regular expressions to postfix regular expressions.
    https://aquarchitect.github.io/swift-algorithm-club/Shunting%20Yard/#:~:text=The%20shunting%20yard%20algorithm%20was,being%20entered%20to%20postfix%20form.&text=The%20following%20table%20describes%20the%20precedence%20and%20the%20associativity%20for%20each%20operator./
    """

    def __init__(self):
        self.alphabet = None
        self.regex = None

    def set_regex(self, regex):
        self.alphabet = get_alphabet(regex)
        self.regex = insert_concat_operator(regex)

    def get_postfix(self):
        output = ''
        stack = []
        for char in self.regex:
            if char in operators and char != CLOSE_PAREN and char != OPEN_PAREN:
                while (
                        stack and
                        stack[-1] in operators and
                        ((associativity[char] == 'left' and precedence[char] <= precedence[stack[-1]]) or
                         (associativity[char] == 'right' and precedence[char] < precedence[stack[-1]]))
                ):
                    output += stack.pop()
                stack.append(char)
            elif char == OPEN_PAREN:
                stack.append(char)
            elif char == CLOSE_PAREN:
                while stack and stack[-1] != OPEN_PAREN:
                    output += stack.pop()

                if not stack:
                    raise Exception("Invalid regular expression. Mismatched parentheses.")

                stack.pop()
            else:
                output += char

        while stack:
            if stack[-1] in (OPEN_PAREN, CLOSE_PAREN):
                raise Exception("Invalid regular expression. Mismatched parentheses.")
            output += stack.pop()
        return output
