class LrSet:
    """
    Defines a Set of Productions used in the LR(0) automaton
    """

    def __init__(self, heart_prods: dict):
        self.heart_prods = heart_prods
