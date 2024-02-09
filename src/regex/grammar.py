class Grammar:
    def __init__(self, states, alphabet, start, accepting_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start = start
        self.accepting_states = accepting_states
        self.transitions = transitions

    def is_accepted(self, string):
        current_states = {self.start}
        has_epsilon_transitions = self.transitions is not {}
        for char in string:
            # If it's an NFA should have epsilon transitions and append the epsilon closure. If not, no states will
            # be added
            temp = set()
            for state in current_states:
                if state.epsilon_transitions:
                    temp.update(state.get_epsilon_closure())
                    has_epsilon_transitions = True
            current_states.update(temp)

            if has_epsilon_transitions:
                next_states = set()
                for state in current_states:
                    if char in state.transitions:
                        next_closure = state.transitions[char]
                        for temp_state in next_closure:
                            next_states.update(temp_state.get_epsilon_closure())

                current_states = next_states
            else:
                next_states = set()
                for state in current_states:
                    if state in self.transitions and char in self.transitions[state]:
                        next_states.update(self.transitions[state][char])
                current_states = next_states

        return bool(current_states.intersection(self.accepting_states))

    def simulate(self, string):
        current_states = {self.start}
        has_epsilon_transitions = self.transitions is not {}
        simulation = ""
        for char in string:
            step = ""
            # If it's an NFA should have epsilon transitions and append the epsilon closure. If not, no states will
            # be added
            temp = set()
            for state in current_states:
                if state.epsilon_transitions:
                    temp.update(state.get_epsilon_closure())
                    has_epsilon_transitions = True
            current_states.update(temp)

            step += f"{current_states} -> {char} -> "
            if has_epsilon_transitions:
                next_states = set()
                for state in current_states:
                    if char in state.transitions:
                        next_closure = state.transitions[char]
                        for temp_state in next_closure:
                            next_states.update(temp_state.get_epsilon_closure())

                current_states = next_states
            else:
                next_states = set()
                for state in current_states:
                    if state in self.transitions and char in self.transitions[state]:
                        next_states.update(self.transitions[state][char])
                current_states = next_states

            step += f"{current_states}\n"
            simulation += step
        return simulation
