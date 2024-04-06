# This file was generated automatically by the YALex compiler
# Do not modify this file directly unless you know what you are doing
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


def rebuild_automatons() -> dict:
    """
    Rebuild the automatons from the json files on the same directory.
    Each JSON is an automaton for a specific rule.
    """
    jsons_paths = # JSONS PATHS

    rule_names = # RULE NAMES

    automatons = {}
    for i in range(len(jsons_paths)):
        # Load the JSON rule file
        with open(jsons_paths[i], "r") as file:
            automatons[rule_names[i]] = json.load(file)

        # Transform the JSONs of the Automatons
        new_automaton = []
        for automaton in automatons[rule_names[i]]:
            temp = {
                'automaton': json.loads(automaton['automaton']),
                'return': automaton['return']
            }
            new_automaton.append(temp)

        automatons[rule_names[i]] = new_automaton

    return automatons


def rebuild_grammars(automatons: dict) -> dict:
    grammars = {}

    for rule in automatons:
        grammars[rule] = []

        # Build Grammars
        for automaton in automatons[rule]:
            automaton_json = automaton['automaton']

            # Create a state for each state in the automaton
            states = set()
            alphabet = set()
            start = None
            accepting_states = set()
            transitions = {}

            # Add the alphabet
            alphabet.add(char for char in automaton_json['alphabet'])

            # Create the states objects
            for state in automaton_json['states']:
                is_accepting = state in automaton_json['accepting_states']
                new_state = State(state, is_accepting)
                states.add(new_state)
                # Add it to start if it's the start state
                if state == automaton_json['start']:
                    start = new_state

                # Add it to accepting states if it's an accepting state
                if is_accepting:
                    accepting_states.add(new_state)

            # Create the transitions
            for transition in automaton_json['transitions']:
                # Get the state obj in the set of states with the same value
                current_state = None
                for state in states:
                    if state.get_value() == int(transition):
                        current_state = state
                        break

                transitions[current_state] = {}

                # Create the transition char -> state
                for char in automaton_json['transitions'][transition]:
                    next_state = None
                    for state in states:
                        if state.get_value() == int(automaton_json['transitions'][transition][char]):
                            next_state = state
                            break

                    if char not in transitions[current_state]:
                        transitions[current_state][char] = set()
                    transitions[current_state][char].add(next_state)

            temp = {
                "grammar": Grammar(states, alphabet, start, accepting_states, transitions),
                "return": automaton['return']
            }
            grammars[rule].append(temp)

    return grammars

    states = {}
    for rule in automatons:
        states[rule] = []
        for automaton in automatons[rule]:
            states[rule].append(automaton['automaton'])


class Lexer:
    def __init__(self):
        self.grammars = rebuild_grammars(
            rebuild_automatons()
        )


def lex_main():
    lexer = Lexer()


if __name__ == "__main__":
    lex_main()
