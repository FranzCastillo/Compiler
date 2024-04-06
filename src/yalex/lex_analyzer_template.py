# This file was generated automatically by the YALex compiler
# Do not modify this file directly unless you know what you are doing

# YALEX HEADER

import json
import argparse


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
        for char in string:
            next_states = set()
            for state in current_states:
                in_transitions = state in self.transitions
                char_creates_transition = char in self.transitions[state]
                if in_transitions and char_creates_transition:
                    next_states.update(self.transitions[state][char])

            # There's no next states, string not accepted
            if not next_states:
                break

            current_states = next_states

        return bool(current_states.intersection(self.accepting_states))

    def print_simulation(self, string):
        current_states = {self.start}
        simulation = ""
        for char in string:
            step = f"{current_states} -> {char} -> "
            next_states = set()
            for state in current_states:
                in_transitions = state in self.transitions
                char_creates_transition = char in self.transitions[state]
                if in_transitions and char_creates_transition:
                    next_states.update(self.transitions[state][char])
            current_states = next_states

            step += f"{current_states}\n"
            simulation += step
            if not current_states:
                break

        return simulation

    def is_runnable_accepted(self, string: str) -> tuple:
        is_runnable = True
        current_states = {self.start}
        for char in string:
            next_states = set()
            for state in current_states:
                in_transitions = state in self.transitions
                char_creates_transition = char in self.transitions[state]
                if in_transitions and char_creates_transition:
                    next_states.update(self.transitions[state][char])
            current_states = next_states

            if not current_states:
                is_runnable = False
                break

        return is_runnable, bool(current_states.intersection(self.accepting_states))


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
            for char in automaton_json['alphabet']:
                alphabet.add(char)

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

                    # Remove the \ before the escaped characters
                    if char[0] == "\\" and char[1] not in ['\\', 'n', 't']:
                        char = char[1]

                    if char not in transitions[current_state]:
                        transitions[current_state][char] = set()

                    transitions[current_state][char].add(next_state)

            temp = {
                "grammar": Grammar(states, alphabet, start, accepting_states, transitions),
                "return": automaton['return']
            }
            grammars[rule].append(temp)

    return grammars


class Token:
    def __init__(self, token_type: str, value: str):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"{self.token_type}: {self.value}"


class SymbolTable:
    def __init__(self):
        self.table = {}


class Lexer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.grammars = rebuild_grammars(
            rebuild_automatons()
        )
        self.tokens = self.tokenize()
        self.symbol_table = SymbolTable()

    def tokenize(self) -> list:
        """
        TODO:
            - Note that escaped characters are preceded by a backslash. Modify the automaton creation to avoid this
        """
        content = ""
        with open(self.file_path, "r") as file:
            content = file.read()

        all_valid_grammars = []  # Keeps track of the available grammars to keep running the string
        # Note that the grammars are ordered by declaration in the yal file

        # Place all the Grammar objects in the list
        for rule in self.grammars:
            for automaton in self.grammars[rule]:
                all_valid_grammars.append(automaton)

        lines = content.split("\n")
        tokens_dicts = []
        for num_line in range(len(lines)):
            line = lines[num_line]
            start_index = 0
            end_index = 1
            while end_index <= len(line):
                current_valid_grammars = all_valid_grammars.copy()
                current_lexeme = ""
                while current_valid_grammars and end_index <= len(line):
                    # While there's still running grammars, increase the lexeme
                    current_lexeme = lines[num_line][start_index:end_index]
                    for grammar in current_valid_grammars:
                        # If it can be run, increase the end index
                        if grammar['grammar'].is_runnable_accepted(current_lexeme)[0]:
                            end_index += 1
                            break
                        else:
                            current_valid_grammars.remove(grammar)

                if len(current_lexeme) > 1:
                    current_lexeme = current_lexeme[:-1]
                    end_index -= 1

                # Find the grammar that accepted the string
                accepted_grammar = None
                for grammar in all_valid_grammars:
                    if grammar['grammar'].is_runnable_accepted(current_lexeme)[1]:
                        accepted_grammar = grammar
                        break

                if accepted_grammar:
                    new_token_dict = {
                        "line": num_line,
                        "pos": start_index,
                        "lexeme": current_lexeme,
                        "type": accepted_grammar['return']
                    }
                else:  # Error
                    new_token_dict = {
                        "line": num_line,
                        "pos": start_index,
                        "lexeme": current_lexeme,
                        "type": "ERROR"
                    }
                print(
                    f"{new_token_dict['line']}:{new_token_dict['pos']} → {new_token_dict['lexeme']} : {new_token_dict['type']}")
                tokens_dicts.append(new_token_dict)

                # Update index
                start_index = end_index
                end_index += 1

        for token_dict in tokens_dicts:
            print(f"{token_dict["line"]}:{token_dict["pos"]} → '{token_dict["lexeme"]}' : {token_dict["type"]}")
        return tokens_dicts


def lex_main(file_path: str):
    lexer = Lexer(file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Tokenize a file.')
    parser.add_argument('file_path', type=str, help='The path to the file to process')

    args = parser.parse_args()

    lex_main(args.file_path)
    # lex_main("D:\\UVG\\Compiladores\\Compiler\\other\\sample_code.txt")

# YALEX FOOTER