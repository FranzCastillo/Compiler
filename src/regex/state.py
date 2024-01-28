from src.regex.state_id import StateId

id_giver = StateId()


class State:
    """
    A state in a finite automaton. A state has a value, a set of transitions
    to other states, and a set of epsilon transitions to other states.
    """

    def __init__(self, is_accepting=False):
        self.transitions = {}
        self.epsilon_transitions = set()
        self.value = id_giver.get_id()
        self.is_accepting = is_accepting

    def add_transition(self, symbol, state):
        """
        Add a transition to another state.
        add_trabsition('a', state)
        a -> state
        :param symbol:
        :param state:
        :return:
        """
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(state)

    def add_epsilon_transition(self, state):
        """
        Add an epsilon transition to another state.
        :param state:
        :return:
        """
        self.epsilon_transitions.add(state)

    def get_transitions(self, symbol):
        """
        Get the set of states that are transitioned to by the symbol.
        :param symbol:
        :return:
        """
        if symbol in self.transitions:
            return self.transitions[symbol]
        return set()

    def get_epsilon_transitions(self):
        """
        Get the set of states that are transitioned to by epsilon.
        :return:
        """
        return self.epsilon_transitions

    def get_value(self):
        """
        Get the value of the state.
        :return:
        """
        return self.value

    def is_accepting(self):
        """
        Check if the state is an accepting state.
        :return:
        """
        return self.is_accepting

    def set_is_accepting(self, is_accepting):
        self.is_accepting = is_accepting

    def __str__(self):
        return str(self.value)
