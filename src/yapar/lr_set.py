from src.yapar.lr_symbol import LrSymbol


class LrSet:
    """
    Defines a Set of Productions used in the LR(0) automaton
    """

    def __init__(self, set_id: int, heart_prods: dict):
        self.set_id = set_id
        self.heart_prods = heart_prods
        self.closure_prods = None
        self.transitions = {}

    def add_transition(self, symbol: LrSymbol, lr_set: 'LrSet') -> None:
        """
        Add a transition to the set
        """
        self.transitions[symbol] = lr_set

    def __str__(self):
        return f"I{self.set_id}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.heart_prods == other.heart_prods

    def __hash__(self):
        return hash(self.id)

