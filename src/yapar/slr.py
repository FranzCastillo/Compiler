from src.yapar.lr_symbol import LrSymbol


def parse_productions(tokens: list[str], productions: dict) -> dict:
    """
    Parse the productions to use LrSymbol
    """
    parsed_productions = {}
    for key, value in productions.items():
        key = LrSymbol(key, is_terminal=False)  # The head of a productions is never a terminal
        parsed_productions[key] = [
            [LrSymbol(symbol, symbol in tokens) for symbol in production]
            for production in value
        ]

    return parsed_productions


def augment_productions(productions: dict) -> tuple[LrSymbol, dict]:
    """
    Augment the productions with the start symbol
    """
    old_start_symbol = list(productions.keys())[0]
    new_start_symbol = LrSymbol(
        f"{old_start_symbol.symbol}'",
        is_terminal=False,
    )
    productions[new_start_symbol] = [old_start_symbol]
    return new_start_symbol, productions


class SLR:
    def __init__(self, tokens, ignored_tokens, productions):
        self.tokens = tokens
        self.ignored_tokens = ignored_tokens
        temp_productions = parse_productions(self.tokens, productions)
        self.start_symbol, self.productions = augment_productions(temp_productions)
        print("END")
