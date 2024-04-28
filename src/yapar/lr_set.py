from src.yapar.lr_symbol import LrSymbol


class LrSet:
    """
    Defines a Set of Productions used in the LR(0) automaton
    """

    def __init__(self, set_id: int, heart_prods: dict, is_accepting: bool = False):
        self.set_id = set_id
        self.heart_prods = heart_prods
        self.closure_prods = None
        self.is_accepting = is_accepting
        self.transitions = {}

    def add_transition(self, symbol: LrSymbol, lr_set: 'LrSet') -> None:
        """
        Add a transition to the set
        """
        self.transitions[symbol] = lr_set

    def get_dot(self):
        """
        Dot notation for graphviz
        """
        if self.is_accepting:
            dot = '''<
                <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">
                    <TR>
                        <TD COLSPAN="2" BGCOLOR="lightgreen">
                            ACCEPT
                        </TD>
                    </TR>
            '''
            return dot + "</TABLE>>"

        dot = f'''<
                <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">
                    <TR>
                        <TD COLSPAN="2" BGCOLOR="lightblue">
                            I{self.set_id}
                        </TD>
                    </TR>
                '''

        # Remove the heart productions from the closure_prods
        body_prods = {}
        # Add bodies that are not part of the heart productions
        for head, bodies in self.closure_prods.items():
            if head not in self.heart_prods:
                body_prods[head] = bodies

        # Add bodies that are part of the heart productions
        for head, bodies in self.closure_prods.items():
            if head in self.heart_prods:
                body_prods[head] = [body for body in bodies if body not in self.heart_prods[head]]

        for head, body in self.heart_prods.items():
            for prod in body:
                dot += f'''
                    <TR>
                        <TD>
                            {head} → {' '.join([str(symbol) for symbol in prod])}
                        </TD>
                    </TR>
                '''
        for head, body in body_prods.items():
            for prod in body:
                dot += f'''
                    <TR>
                        <TD BGCOLOR="gray">
                            {head} → {' '.join([str(symbol) for symbol in prod])}
                        </TD>
                    </TR>
                '''

        return dot + "</TABLE>>"

    def __str__(self):
        return f"I{self.set_id}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.heart_prods == other.heart_prods

    def __hash__(self):
        return hash(self.set_id)
