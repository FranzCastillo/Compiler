class RegexParser:
    def __init__(self, identifiers: dict):
        self.identifiers = identifiers

    def parse(self, regex: str):
        new_regex = regex
        initial_char = regex[0]
        if initial_char == "'":  # 'regular-char | escape-sequence'
            pass
        elif initial_char == '_':
            pass
        elif initial_char == '[':  # [ character-set ]
            next_char = regex[1]
            if next_char == '^':  # Denota cualquier símbolo que no pertenece al character-set
                pass
            else:  # Denota un conjunto de símbolos.
                pass
        elif initial_char == '(':  # ( regex )
            pass
        else:  # Identificadores
            pass
        return new_regex