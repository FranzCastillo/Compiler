def augment_productions(productions: dict):
    """
    Augment the productions with the start symbol
    """
    old_start_symbol = list(productions.keys())[0]
    new_start_symbol = old_start_symbol + "'"
    productions[new_start_symbol] = [old_start_symbol]
    return new_start_symbol, productions


class SLR:
    def __init__(self, tokens, ignored_tokens, productions):
        self.tokens = tokens
        self.ignored_tokens = ignored_tokens
        self.start_symbol, self.productions = augment_productions(productions)
