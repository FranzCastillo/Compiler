EPSILON = 'ε'
KLEENE_STAR = '*'
CONCAT = '.'
UNION = '|'
OPEN_PAREN = '('
CLOSE_PAREN = ')'

precedence = {
    KLEENE_STAR: 3,
    CONCAT: 2,
    UNION: 1,
    OPEN_PAREN: 0,
    CLOSE_PAREN: 0
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

            if regex[i] not in operators and regex[i + 1] not in operators:
                should_concat = True
            elif regex[i] == CLOSE_PAREN and regex[i + 1] not in operators:
                should_concat = True
            elif regex[i] not in operators and regex[i + 1] == OPEN_PAREN:
                should_concat = True
            elif regex[i] == KLEENE_STAR and regex[i + 1] not in operators:
                should_concat = True

            if should_concat:
                new_regex += CONCAT

    return new_regex


class ShuntingYard:
    """
    The Shunting Yard algorithm for converting infix regular expressions to postfix regular expressions.
    https://blog.cernera.me/converting-regular-expressions-to-postfix-notation-with-the-shunting-yard-algorithm/
    """

    def __init__(self):
        self.alphabet = None
        self.regex = None

    def set_regex(self, regex):
        self.alphabet = get_alphabet(regex)
        self.regex = insert_concat_operator(regex)
        print(self.regex)
