class LrSet:
    """
    Defines a Set of Productions used in the LR(0) automaton
    """

    def __init__(self, set_id: int, heart_prods: dict):
        self.set_id = set_id
        self.heart_prods = heart_prods
