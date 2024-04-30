from src.regex.state_id import StateId
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
            [
                LrSymbol(
                    symbol,
                    is_terminal=symbol in tokens,
                    is_epsilon=symbol == "ε"
                )
                for symbol in production
            ]
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
    productions[new_start_symbol] = [[LrSymbol('•', is_dot=True), old_start_symbol]]
    return new_start_symbol, productions


def find_pending_symbols(prod_body: list[LrSymbol]) -> LrSymbol:
    """
    Find the pending symbols in the body of a production
    A pending symbol are the non-terminal symbols that are after the dot
    """
    for i, symbol in enumerate(prod_body):
        if symbol.is_dot:
            if i + 1 < len(prod_body):
                return prod_body[i + 1]
            else:
                return None


class SLR:
    def __init__(self, tokens, ignored_tokens, productions):
        self.all_sets = None
        self.id_giver = StateId()
        self.tokens = tokens
        self.ignored_tokens = ignored_tokens
        temp_productions = parse_productions(self.tokens, productions)
        self.start_symbol, self.productions = augment_productions(temp_productions)
        self.initial_set = LrSet(
            set_id=self.id_giver.get_id(),
            heart_prods={self.start_symbol: self.productions[self.start_symbol]},
        )
        self.symbols = self._get_symbols()
        self.ignored_symbols = [LrSymbol(symbol) for symbol in ignored_tokens]
        self.build_lr0_automaton()

    def _get_symbols(self) -> set[LrSymbol]:
        """
        Get the symbols from the tokens
        """
        symbols = {LrSymbol(symbol) for symbol in self.tokens}

        for head, body in self.productions.items():
            symbols.add(head)
            for prod in body:
                for symbol in prod:
                    if symbol not in symbols:
                        symbols.add(symbol)

        symbols.add(LrSymbol("$", is_sentinel=True))

        return symbols

    def closure(self, lr_set: LrSet) -> LrSet:
        """
        Compute the closure of the heart productions
        """
        set_prods = {}

        # Add the heart productions to the set_prods
        for head, body in lr_set.heart_prods.items():
            set_prods[head] = body.copy()

        pending_symbols = set()
        for head, body in lr_set.heart_prods.items():
            for prod in body:
                pending_symbols.add(find_pending_symbols(prod))

        checked_symbols = set()

        while pending_symbols:
            symbol = pending_symbols.pop()
            if symbol in checked_symbols:
                continue
            checked_symbols.add(symbol)

            if symbol not in set_prods:
                set_prods[symbol] = []

            if symbol not in self.productions:
                continue

            for prod in self.productions[symbol]:
                temp_prod = [LrSymbol('•', is_dot=True)]
                for prod_symbol in prod:
                    temp_prod.append(prod_symbol)
                set_prods[symbol].append(temp_prod)
                pending_symbols.add(find_pending_symbols(temp_prod))

        lr_set.closure_prods = set_prods

        return lr_set

    def goto(self, lr_set: LrSet, lr_symbol: LrSymbol) -> LrSet:
        """
        Compute the go-to set of a symbol
        """
        new_set_prods = {}

        current_set_prods = self.closure(lr_set)
        for head, body in current_set_prods.closure_prods.items():
            for prod in body:
                dot_pos = -1
                for i, symbol in enumerate(prod):
                    if symbol.is_dot:
                        dot_pos = i
                        break

                # If the dot is at the end of the list
                if dot_pos == len(prod) - 1:
                    # If the head is the start symbol
                    if head == self.start_symbol and lr_symbol.is_sentinel:
                        temp = LrSet(
                            set_id=self.id_giver.get_id(),
                            heart_prods={},
                            is_accepting=True,
                        )
                        lr_set.add_transition(lr_symbol, temp)
                        return temp

                    continue

                if prod[dot_pos + 1] == lr_symbol:
                    temp_prod = prod.copy()
                    temp_prod[dot_pos] = lr_symbol
                    temp_prod[dot_pos + 1] = LrSymbol("•", is_dot=True)

                    if head not in new_set_prods:
                        new_set_prods[head] = []

                    new_set_prods[head].append(temp_prod)

        return LrSet(
            set_id=self.id_giver.get_id(),
            heart_prods=new_set_prods,
        )

    def build_lr0_automaton(self):
        """
        Build the LR(0) automaton
        """
        pending_sets = [self.closure(self.initial_set)]
        self.all_sets = [self.initial_set]
        while pending_sets:
            current_set = pending_sets.pop(0)
            for symbol in self.symbols:
                new_set = self.goto(current_set, symbol)
                # Check if the new set already exists
                if new_set.heart_prods or new_set.is_accepting:
                    if new_set in self.all_sets:
                        new_set = self.all_sets[self.all_sets.index(new_set)]
                    else:
                        pending_sets.append(new_set)
                        self.all_sets.append(new_set)
                        self.closure(new_set)

                    current_set.add_transition(symbol, new_set)
