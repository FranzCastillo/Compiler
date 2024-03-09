from src.regex.operators_values import *

ALL_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def create_set(start, end) -> set:
    return {chr(i) for i in range(ord(start), ord(end) + 1)}


def get_all_chars_set() -> set:
    return {char for char in ALL_CHARS}


class RegexParser:
    def __init__(self, identifiers: dict):
        self.identifiers = identifiers

    def parse(self, regex: str):
        stack = []
        i = 0
        while i < len(regex):
            char = regex[i]
            if char == "[":  # Set of characters
                next_char = regex[i + 1]
                if next_char == "'" or next_char == '"':  # Set of chars or range of chars
                    if next_char == "'" and regex[i + 4] == '-':  # Range of chars ['a'-'z''A'-'Z''0'-'9']
                        i += 2  # Skip ['
                        string_content = ''
                        while regex[i] != ']':
                            string_content += regex[i] if regex[i] != "'" else ''  # Skip '
                            i += 1
                        stack.append(f"[{string_content}]")
                    else:  # Union of chars
                        content_list = []
                        while regex[i] != ']':
                            if regex[i] == "'":
                                i += 1
                                if regex[i] in escape_characters:
                                    content_list.append(f"\\{regex[i]}")
                                elif regex[i] == '\\':
                                    content_list.append(f"\\{regex[i + 1]}")
                                    i += 1
                                else:
                                    content_list.append(regex[i])
                                i += 2  # Skip the last '
                            elif regex[i] == '"':
                                temp = ''
                                i += 1
                                while regex[i] != '"':
                                    temp += regex[i] + CONCAT
                                    i += 1
                                i += 1  # Skip "
                                content_list.append(f"({temp[:-1]})")
                            else:
                                i += 1
                        stack.append(f"({UNION.join(content_list)})")
                elif next_char == '^':  # Any character except the ones in the set
                    i += 2  # Skip ['
                    string_content = ''
                    while regex[i] != ']':
                        string_content += regex[i] if regex[i] != "'" else ''  # Skip ' and -
                        i += 1
                    set_to_remove = set()
                    j = 0
                    while j < len(string_content):
                        if string_content[j] == '-':
                            set_to_remove.update(create_set(string_content[j - 1], string_content[j + 1]))
                        j += 1
                    new_set = get_all_chars_set() - set_to_remove
                    stack.append(f"({UNION.join(new_set)})")
            elif char == '"':  # Set of chars
                string_content = ''
                i += 1
                while regex[i] != '"':
                    current_char = regex[i]
                    if current_char in escape_characters:
                        string_content += f"\\{current_char}" + CONCAT
                    else:
                        string_content += regex[i] + CONCAT
                    i += 1
                stack.append(f"({string_content[:-1]})")
            elif char == "'":  # Simple symbol
                i += 1
                next_char = regex[i]
                if next_char in escape_characters:  # If it finds ., |, etc.
                    stack.append(f"\\{next_char}")
                elif next_char == '\\':  # If it finds \, it will add the next char
                    stack.append(f"\\{regex[i + 1]}")
                    i += 1
                else:
                    stack.append(next_char)
                i += 1
            elif char == '_':  # Any character
                stack.append(f"({UNION.join(ALL_CHARS)})")
            elif char == '#':  # Diff set
                first_set_str = stack.pop()
                if not (first_set_str[0] == '[' and first_set_str[2] == "-"):
                    raise Exception("Syntax Error. Missing first set in #")
                if not (regex[i + 1] == '[' and regex[i + 2] == "'" and regex[i + 5] == '-'):
                    raise Exception("Syntax Error. Missing second set in #")

                # Convert to set
                first_set = set()
                j = 0
                while j < len(first_set_str):
                    if first_set_str[j] == '-':
                        first_set.update(create_set(first_set_str[j - 1], first_set_str[j + 1]))
                    j += 1

                i += 2  # Skip ['
                string_content = ''
                while regex[i] != ']':
                    string_content += regex[i] if regex[i] != "'" else ''  # Skip ' and -
                    i += 1
                second_set = set()
                j = 0
                while j < len(string_content):
                    if string_content[j] == '-':
                        second_set.update(create_set(string_content[j - 1], string_content[j + 1]))
                    j += 1
                new_set = first_set - second_set
                stack.append(f"({UNION.join(new_set)})")
            else:
                stack.append(char)
            i += 1

        return_value = ''.join(stack)
        return return_value
