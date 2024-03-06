class RegexParser:
    def __init__(self, identifiers: dict):
        self.identifiers = identifiers

    def parse(self, regex: str):
        stack = []
        for i in range(len(regex)):
            char = regex[i]
            if char == "'":  # Constant or scape character
                pass
            elif char == "_":  # Any character
                pass
            elif char == '"':  # Chain of characters may contain scape characters
                pass
            elif char == "[":  # Set of characters
                next_char = regex[i + 1]
                if next_char == "'":  # Simple symbol
                    pass
                elif next_char == '"':  # Chain of characters
                    pass
                elif next_char == '^':  # Any character except the ones in the set
                    pass
            elif char == '#':  # Difference set of two regex
                pass
            elif char == '*':  # Kleene Closure
                pass
            elif char == '+':  # Positive Closure
                pass
            elif char == '?':  # Optional
                pass
            elif char == '|':  # Union
                pass


        return new_regex
