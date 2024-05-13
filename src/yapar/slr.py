from src.regex.state_id import StateId
from src.yapar.lr_set import LrSet
from src.yapar.lr_symbol import LrSymbol


def parse_productions(tokens: list[LrSymbol], productions: dict) -> dict:
    """
    Parse the productions to use LrSymbol
    """
    parsed_productions = {}
    for key, value in productions.items():
        key = LrSymbol(key, is_terminal=False)  # The head of a productions is never a terminal
        parsed_productions[key] = [
            [LrSymbol(symbol, is_terminal=symbol in tokens, is_epsilon=symbol == "ε") for symbol in production] for
            production in value]

    return parsed_productions


def augment_productions(productions: dict) -> tuple[LrSymbol, dict]:
    """
    Augment the productions with the start symbol
    """
    old_start_symbol = list(productions.keys())[0]
    new_start_symbol = LrSymbol(f"{old_start_symbol.symbol}'", is_terminal=False, )
    productions[new_start_symbol] = [[LrSymbol('•', is_dot=True), old_start_symbol]]
    return new_start_symbol, productions


def find_pending_symbols(prod_body: list[LrSymbol]) -> LrSymbol | None:
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
    return None


def has_epsilon_production(symbol: LrSymbol, productions: dict) -> bool:
    """
    Check if a symbol has an epsilon production
    """
    if symbol not in productions:
        return False

    for prod in productions[symbol]:
        if len(prod) == 1 and prod[0].is_epsilon:
            return True

    return False


class SLR:
    def __init__(self, tokens, ignored_tokens, productions):
        self.all_sets = None
        self.id_giver = StateId()
        self.tokens = tokens
        self.ignored_tokens = ignored_tokens
        self.productions = parse_productions(self.tokens, productions)
        self.start_symbol = list(self.productions.keys())[0]
        self.augmented_start_symbol, self.augmented_productions = augment_productions(self.productions.copy())
        self.initial_set = LrSet(set_id=self.id_giver.get_id(), heart_prods={
            self.augmented_start_symbol: self.augmented_productions[self.augmented_start_symbol]}, )
        self.symbols = self._get_symbols()
        self.ignored_symbols = [LrSymbol(symbol) for symbol in ignored_tokens]
        self.build_lr0_automaton()

    def _get_symbols(self) -> set[LrSymbol]:
        """
        Get the symbols from the tokens
        """
        symbols = {LrSymbol(symbol) for symbol in self.tokens}

        for head, body in self.augmented_productions.items():
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

            if symbol not in self.augmented_productions:
                continue

            for prod in self.augmented_productions[symbol]:
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
                    if head == self.augmented_start_symbol and lr_symbol.is_sentinel:
                        temp = LrSet(set_id=self.id_giver.get_id(), heart_prods={}, is_accepting=True, )
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

        return LrSet(set_id=self.id_giver.get_id(), heart_prods=new_set_prods, )

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

    def first(self):
        first_sets = {}
        for head in self.productions.keys():
            first_sets[head] = self._first(head, {})
        return first_sets

    def _first(self, symbol: LrSymbol, first_sets: dict) -> set[LrSymbol]:
        if symbol.is_terminal:
            return {symbol}

        if symbol in first_sets:
            return first_sets[symbol]

        first_set = set()
        first_sets[symbol] = first_set

        epsilon = LrSymbol("ε", is_epsilon=True)

        for production_head, productions in self.productions.items():
            if production_head == symbol:
                for production in productions:
                    for prod_symbol in production:
                        if prod_symbol == epsilon:
                            first_set.add(epsilon)
                            break

                        if prod_symbol.is_terminal:
                            first_set.add(prod_symbol)
                            break

                        prod_symbol_first = self._first(prod_symbol, first_sets)
                        first_set.update(prod_symbol_first - {epsilon})
                        if epsilon not in prod_symbol_first:
                            break
                    else:
                        first_set.add(epsilon)

        first_sets[symbol] = first_set
        return first_set

    def follow(self):
        follow_sets = {}
        for head in self.productions.keys():
            follow_sets[head] = self._follow(head, {})
        return follow_sets

    def _follow(self, symbol: LrSymbol, follow_sets: dict) -> set[LrSymbol]:
        if symbol in follow_sets:
            return follow_sets[symbol]

        follow_set = set()
        if symbol == self.start_symbol:
            follow_set.add(LrSymbol("$", is_sentinel=True))

        epsilon = LrSymbol("ε", is_epsilon=True)
        for production_head, productions in self.productions.items():
            for production_body in productions:
                for i, prod_symbol in enumerate(production_body):
                    if symbol == prod_symbol:
                        if i + 1 < len(production_body):
                            next_symbol = production_body[i + 1]
                            next_symbol_first = self._first(next_symbol, follow_sets)
                            follow_set.update(next_symbol_first - {epsilon})

                        if i + 1 == len(production_body) or epsilon in self._first(production_body[i + 1], follow_sets):
                            if production_head != symbol:
                                follow_set.update(self._follow(production_head, follow_sets))

        follow_sets[symbol] = follow_set
        return follow_set

    def build_parsing_table(self):
        """
        Build the LR(0) parsing table
        """
        # Set the table up
        table = {}
        for lr_set in self.all_sets:
            table[lr_set.set_id] = {
                "actions": {},
                "gotos": {}
            }
            for symbol in self.symbols:
                if symbol.is_terminal:
                    table[lr_set.set_id]["actions"][symbol] = None
                elif not symbol.is_dot:
                    table[lr_set.set_id]["gotos"][symbol] = None

        # Fill the table
        sentinel = LrSymbol("$", is_sentinel=True)
        dot = LrSymbol("•", is_dot=True)
        for lr_set in self.all_sets:
            for production_head, productions in lr_set.closure_prods.items():
                for production_body in productions:
                    # Accept
                    if production_head == self.augmented_start_symbol and production_body[-1] == dot:
                        table[lr_set.set_id]["actions"][sentinel] = ("ACCEPT", None)