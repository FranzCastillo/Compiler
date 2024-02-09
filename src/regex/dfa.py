from src.regex.grammar import Grammar
from src.regex.state import State



def move(states, symbol):
    """
    Get the set of states that are transitioned to by the symbol.
    :param states:
    :param symbol:
    :return:
    """
    next_states = set()
    for state in states:
        # Union the set of states that are transitioned to by the symbol.
        next_states |= state.get_transitions(symbol)
    return next_states


def get_unmarked_states(states):
    """
    Get all the unmarked states.
    :param states:
    :return:
    """
    unmarked_states = set()
    for state in states:
        if not states[state]['marked']:
            unmarked_states.add(state)
    return unmarked_states


def get_transitions(states):
    """
    Get the transitions of the states.
    :param states:
    :return:
    """
    transitions = {}
    for state in states:
        temp = states[state]['transitions']
        transitions[state] = temp
    return transitions


def get_accepting_states(states):
    accepting_states = set()
    for state in states:
        for nfa_state in states[state]['closure']:
            if nfa_state.is_accepting:
                accepting_states.add(states[state]['state'])

    for state in accepting_states:
        state.is_accepting = True
    return accepting_states


class DFA:
    def __init__(self, nfa_grammar):
        self.nfa_grammar = nfa_grammar
        self.grammar = self.get_grammar()

    def get_grammar(self, show_death_state=False):
        return self.build_dfa(show_death_state)

    def build_dfa(self, show_death_state):
        alphabet = self.nfa_grammar.alphabet
        # Create the start state by getting its epsilon closure.
        start_state = State()
        start_closure = self.nfa_grammar.start.get_epsilon_closure()
        states = {
            start_state.value: {
                'state': start_state,
                'closure': start_closure,
                'transitions': {},
                'marked': False
            }
        }

        # Create a "dead" state to transition to if there is no transition for a symbol.
        dead_state = State()
        dead_state.value = -1
        states[dead_state.value] = {
            'state': dead_state,
            'closure': set(),
            'transitions': {},
            'marked': False
        }
        for symbol in alphabet:
            states[dead_state.value]['transitions'][symbol] = {dead_state}
            states[dead_state.value]['state'].add_transition(symbol, dead_state)

        # Create a map to keep track of the closure of each state.
        closure_map = {start_state.value: start_closure}

        while unmarked_states := get_unmarked_states(states):
            current_state = unmarked_states.pop()
            states[current_state]['marked'] = True
            for symbol in alphabet:
                next_states = move(states[current_state]['closure'], symbol)
                next_closure = set()
                for state in next_states:
                    next_closure |= state.get_epsilon_closure()
                if next_closure:
                    if next_closure not in closure_map.values():
                        new_state = State()
                        states[new_state.value] = {
                            'state': new_state,
                            'closure': next_closure,
                            'transitions': {},
                            'marked': False
                        }
                        states[current_state]['transitions'][symbol] = {new_state}
                        states[current_state]['state'].add_transition(symbol, new_state)
                        closure_map[new_state.value] = next_closure
                    else:
                        for state in states:
                            if states[state]['closure'] == next_closure:
                                states[current_state]['transitions'][symbol] = {states[state]['state']}
                                states[current_state]['state'].add_transition(symbol, states[state]['state'])
                                break
                elif show_death_state:
                    states[current_state]['transitions'][symbol] = dead_state
                    states[current_state]['state'].add_transition(symbol, dead_state)

        accepting_states = get_accepting_states(states)
        states_obj = set()
        for state in states:
            states_obj.add(states[state]['state'])
        transitions = get_transitions(states)

        return Grammar(states_obj, alphabet, start_state, accepting_states, transitions)
