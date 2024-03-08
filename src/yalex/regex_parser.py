from src.regex.operators_values import *


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
                if next_char == "'":  # Simple symbol
                    i += 1
                    string_content = ''
                    is_range = regex[i + 3] == '-'
                    if is_range:  # ['a'-'z''A'-'Z''0'-'9']
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

                elif next_char == '"':  # Chain of characters
                    string_content = '('
                    i += 2  # Skip ["
                    while regex[i] != '"':
                        current_char = regex[i]
                        if current_char in escape_characters:
                            string_content += f"\\{current_char}" + CONCAT
                        else:
                            string_content += regex[i] + UNION
                        i += 1
                    i += 1  # Skip "
                    stack.append(string_content[:-1] + ')')
                elif next_char == '^':  # Any character except the ones in the set
                    i += 1
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
                if next_char in escape_characters:
                    stack.append(f"\\{next_char}")
                else:
                    stack.append(next_char)
                i += 1
            else:
                stack.append(char)
            i += 1

        return_value = ''.join(stack)
        return return_value
