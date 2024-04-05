# This file was generated automatically by the YALex compiler
# Do not modify this file directly
import json


class State:
    """
    A state in a finite automaton. A state has a value, a set of transitions
    to other states, and a set of epsilon transitions to other states.
    """

    def __init__(self, value, is_accepting=False):
        self.transitions = {}
        self.epsilon_transitions = set()
        self.value = value
        self.is_accepting = is_accepting

    def add_transition(self, symbol, state):
        """
        Add a transition to another state.
        add_transition('a', state)
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

    def get_epsilon_closure(self):
        """
        Get the epsilon closure of the state.
        :return:
        """
        closure = set()
        stack = [self]
        while stack:
            current_state = stack.pop()
            closure.add(current_state)
            for next_state in current_state.get_epsilon_transitions():
                if next_state not in closure:
                    stack.append(next_state)

        return closure

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

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other

    def __hash__(self):
        return hash(self.value)


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

class Lexer:
    """
    TODO:
    - Recreate the grammars from the jsons
    """
    def __init__(self):
        pass
