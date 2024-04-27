from src.yapar.lr_set import LrSet
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


def find_pending_symbols(prod_body: list[LrSymbol]) -> set:
    """
    Find the pending symbols in the body of a production
    A pending symbol are the non-terminal symbols that are after the dot
    """
    pending_symbols = set()
    for i, symbol in enumerate(prod_body):
        if not symbol.is_terminal and not symbol.is_dot:
            pending_symbols.add(symbol)
    return pending_symbols


class SLR:
    def __init__(self, tokens, ignored_tokens, productions):
        self.tokens = tokens
        self.ignored_tokens = ignored_tokens
        temp_productions = parse_productions(self.tokens, productions)
        self.start_symbol, self.productions = augment_productions(temp_productions)
        self.productions[self.start_symbol].insert(0, LrSymbol(".", is_dot=True))
        self.initial_set = LrSet(
            heart_prods={self.start_symbol: self.productions[self.start_symbol]},
        )

    def closure(self, lr_set: LrSet) -> dict:
        """
        Compute the closure of the heart productions
        """
        set_prods = {}

        # Add the heart productions to the set_prods
        for head, body in lr_set.heart_prods.items():
            set_prods[head] = body

        pending_symbols = set()
        for head, body in lr_set.heart_prods.items():
            pending_symbols |= find_pending_symbols(body)

        checked_symbols = set()

        while pending_symbols:
            symbol = pending_symbols.pop()
            if symbol in checked_symbols:
                continue
            checked_symbols.add(symbol)

            if symbol not in set_prods:
                set_prods[symbol] = []

            for prod in self.productions[symbol]:
                temp_prod = [LrSymbol('.', is_dot=True)]
                for prod_symbol in prod:
                    temp_prod.append(prod_symbol)
                set_prods[symbol].append(temp_prod)
                pending_symbols |= find_pending_symbols(temp_prod)

        return set_prods
