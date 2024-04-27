from src.yapar.lr_symbol import LrSymbol


def find_pending_symbols(prod_body: list) -> set:
    """
    Find the pending symbols in the body of a production
    A pending symbol are the non-terminal symbols that are after the dot
    """
    pending_symbols = set()
    for i, symbol in enumerate(prod_body):
        if not symbol.is_terminal and not symbol.is_dot:
            pending_symbols.add(symbol)
    return pending_symbols


class LrSet:
    """
    Defines a Set of Productions used in the LR(0) automaton
    """

    def __init__(self, heart_prods: dict, all_prods: dict):
        self.heart_prods = heart_prods
        self.all_prods = all_prods
        self.set_prods = self._closure()

    def _closure(self) -> dict:
        """
        Compute the closure of the heart productions
        """
        set_prods = {}

        # Add the heart productions to the set_prods
        for head, body in self.heart_prods.items():
            set_prods[head] = body

        pending_symbols = set()
        for head, body in self.heart_prods.items():
            pending_symbols |= find_pending_symbols(body)

        checked_symbols = set()

        while pending_symbols:
            symbol = pending_symbols.pop()
            if symbol in checked_symbols:
                continue
            checked_symbols.add(symbol)

            if symbol not in set_prods:
                set_prods[symbol] = []

            for prod in self.all_prods[symbol]:
                temp_prod = [LrSymbol('.', is_dot=True)]
                for prod_symbol in prod:
                    temp_prod.append(prod_symbol)
                set_prods[symbol].append(temp_prod)
                pending_symbols |= find_pending_symbols(temp_prod)

        return set_prods
