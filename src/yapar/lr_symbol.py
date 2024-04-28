class LrSymbol:
    def __init__(self, symbol: str, is_terminal: bool = False, is_dot: bool = False, is_sentinel: bool = False):
        self.symbol = symbol
        self.is_terminal = is_terminal
        self.is_dot = is_dot
        self.is_sentinel = is_sentinel

    def __str__(self):
        return f"{self.symbol}"

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def __repr__(self):
        return str(self)