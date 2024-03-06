class RegexParser:
    def __init__(self, identifiers: dict):
        self.identifiers = identifiers

    # TODO:Implement a way to handle \n, \t
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
                            string_content += regex[i] if regex[i] != "'" else ''
                            i += 1
                        stack.append(f"[{string_content}]")

                    else:  # Union of chars
                        pass

                elif next_char == '"':  # Chain of characters
                    string_content = '('
                    i += 2  # Skip ["
                    while regex[i] != '"':
                        string_content += regex[i] + '|'
                        i += 1
                    i += 1  # Skip "
                    stack.append(string_content[:-1] + ')')
                elif next_char == '^':  # Any character except the ones in the set
                    i += 1
            elif char == '"':  # Set of chars
                string_content = ''
                i += 1
                while regex[i] != '"':
                    string_content += regex[i] + '.'
                    i += 1
                stack.append(f"({string_content[:-1]})")
            else:
                stack.append(char)
            i += 1

        return_value = ''.join(stack)
        return return_value
