from src.regex.grammar import Grammar
from src.regex.state import State


def get_reachable_states(dfa_grammar):
    """
    Get the reachable states of a DFA.
    :param dfa_grammar:
    :return:
    """
    start_state = dfa_grammar.start
    reachable_states = set()
    stack = [start_state]
    while stack:
        current_state = stack.pop()
        reachable_states.add(current_state)
        for transition in current_state.transitions:
            next_state = list(current_state.transitions[transition])[0]  # Only one state per transition
            if next_state not in reachable_states and next_state not in stack:
                stack.append(next_state)
    return reachable_states


def get_state_of_partition(partitions_dict, target_state):
    for key, states_set in partitions_dict.items():
        for state in states_set:
            if state == target_state:
                return key
    return None

def minimize_dfa(dfa_grammar):
    """
    Function to minimize a DFA. Using Hopcroft's algorithm.
    https://pfafner.github.io/tc2023/lecturas/Lectura03.pdf
    :return: Minimized DFA.
    """
    states = get_reachable_states(dfa_grammar)
    symbols = dfa_grammar.alphabet
    accept_states = dfa_grammar.accepting_states

    # Create P and W
    difference = states - accept_states
    if difference:
        P = [accept_states, difference]
        W = [accept_states, difference]
    else:
        P = [accept_states]
        W = [accept_states]
    # while (W is not empty) do
    while W:
        # choose and remove a set A from W
        A = W.pop()
        # for each c in Σ do
        for c in symbols:
            # let X be the set of states for which a transition on c leads to a state in A
            X = set()
            for state in states:
                transition = state.transitions.get(c)
                if transition and list(transition)[0] in A:
                    X.add(state)

            # for each set Y in P for which X ∩ Y is nonempty and Y \ X is nonempty do
            for Y in P:
                intersection = X.intersection(Y)
                difference = Y - X
                if intersection and difference:
                    # replace Y in P by the two sets X ∩ Y and Y \ X
                    P.remove(Y)
                    P.append(intersection)
                    P.append(difference)
                    if Y in W:
                        # replace Y in W by the same two sets
                        W.remove(Y)
                        W.append(intersection)
                        W.append(difference)
                    else:
                        if len(intersection) <= len(difference):
                            W.append(intersection)
                        else:
                            W.append(difference)

    states = set()
    alphabet = dfa_grammar.alphabet
    start = None
    accepting_states = set()

    # Create the new states and map the partitions
    partition_dict = {}
    for state_set in P:
        new_state = State()
        for state in state_set:
            if state in accept_states:
                new_state.is_accepting = True
                accepting_states.add(new_state)
            if state == dfa_grammar.start:
                start = new_state
        states.add(new_state)
        partition_dict[new_state] = state_set

    # Create the transitions
    transitions = {}

    for state in states:
        state.transitions = {}
        transitions[state] = {}
        # Since all the states of the same partition transitions to the same partition, we can use any state
        try_state = list(partition_dict[state])[0]  # Contains a state from the partition
        for symbol in alphabet:
            # If the state has no transition for the symbol, continue
            if not try_state.transitions.get(symbol):
                continue

            # Start the set for the transitions dictionary
            if symbol not in transitions[state]:
                transitions[state][symbol] = set()

            next_state = list(try_state.transitions.get(symbol))[0]
            state_to_transition = get_state_of_partition(partition_dict, next_state)

            # Add the transition to the state
            state.transitions[symbol] = {state_to_transition}
            # Add the transition to the transitions dictionary
            transitions[state][symbol].add(state_to_transition)

    return Grammar(states, alphabet, start, accepting_states, transitions)


class MinifiedDFA:
    def __init__(self, dfa_grammar):
        self.dfa_grammar = dfa_grammar
        self.minified_dfa_grammar = minimize_dfa(dfa_grammar)

    def get_grammar(self):
        return self.minified_dfa_grammar
