from src.regex.operators_values import *


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
            elif (current_char == KLEENE_STAR or current_char == KLEENE_PLUS or current_char == QUESTION_MARK) and (
                    next_char not in operators or next_char == OPEN_PAREN):
                should_concat = True
            elif current_char == CLOSE_PAREN and next_char == OPEN_PAREN:
                should_concat = True

            if should_concat:
                new_regex += CONCAT

    return new_regex


def expand_ranges(regex):
    """
    Expand the ranges in the regular expression.
    :param regex:
    :return:
    """
    stack = []
    for char in regex:
        if char == OPEN_BRACKET:
            stack.append(char)
        elif char == CLOSE_BRACKET:
            if len(stack) == 0:
                raise Exception("Invalid regular expression. Mismatched brackets.")
            if len(stack) == 1:  # no range
                stack.pop()
            else:
                temp = []
                while stack[-1] != OPEN_BRACKET:
                    temp.append(stack.pop())

                if len(temp) < 2:
                    raise Exception("Invalid regular expression. Invalid range.")

                stack.pop()
                temp.reverse()
                stack.append(temp)
        elif char != '-':
            stack.append(char)

    new_regex = ''
    for char_range in stack:
        if isinstance(char_range, list):
            if len(char_range) % 2 != 0:
                raise Exception("Invalid regular expression. Invalid range.")

            new_regex += OPEN_PAREN

            for i in range(0, len(char_range), 2):
                lower = char_range[i]
                upper = char_range[i + 1]
                lower_ascii = ord(char_range[i])
                upper_ascii = ord(char_range[i + 1])
                if 65 <= lower_ascii <= 90 and 97 <= upper_ascii <= 122:
                    raise Exception(
                        "Invalid regular expression. Invalid range. Lower bound is an upper case letter and upper "
                        "bound is a lower case letter.")

                if lower_ascii > upper_ascii:  # If both are lower case letters or both are upper case letters
                    raise Exception(
                        "Invalid regular expression. Invalid range. Lower bound is greater than upper bound (in ASCII).")

                for j in range(lower_ascii, upper_ascii + 1):
                    new_regex += chr(j) + UNION

            new_regex = new_regex[:-1]  # remove the last '|'
            new_regex += CLOSE_PAREN
        else:
            new_regex += char_range
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
        new_regex = expand_ranges(regex)
        # new_regex = replace_symbols(new_regex)
        self.alphabet = get_alphabet(new_regex)
        self.regex = insert_concat_operator(new_regex)

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
