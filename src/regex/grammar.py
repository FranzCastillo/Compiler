class Grammar:
    def __init__(self, states, alphabet, start, accepting_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.accepting_states = accepting_states
        self.transitions = transitions
