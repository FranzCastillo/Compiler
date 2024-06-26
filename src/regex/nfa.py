from src.regex.grammar import Grammar
from src.regex.operators import Operator
from src.regex.state import State


class Fragment:
    def __init__(self, start, out):
        self.start = start
        self.out = out


def add_union(frag1, frag2):
    """Add a union between two fragments"""
    start = State()
    start.add_epsilon_transition(frag1.start)
    start.add_epsilon_transition(frag2.start)
    out = State()
    frag1.out.add_epsilon_transition(out)
    frag2.out.add_epsilon_transition(out)
    return Fragment(start, out)


def add_concat(frag1, frag2):
    """Add a concatenation between two fragments"""
    frag1.out.add_epsilon_transition(frag2.start)
    return Fragment(frag1.start, frag2.out)


def add_kleene_star(frag):
    """Add a kleene star to a fragment"""
    start = State()
    out = State()
    start.add_epsilon_transition(frag.start)
    start.add_epsilon_transition(out)
    frag.out.add_epsilon_transition(frag.start)
    frag.out.add_epsilon_transition(out)
    return Fragment(start, out)


def add_symbol(symbol):
    """Add a symbol to a fragment"""
    start = State()
    out = State()
    if symbol == Operator.EPSILON.symbol:
        start.add_epsilon_transition(out)
    else:
        start.add_transition(symbol, out)
    return Fragment(start, out)


def add_kleene_plus(frag):
    """Add a kleene plus to a fragment"""
    start = State()
    out = State()
    start.add_epsilon_transition(frag.start)
    frag.out.add_epsilon_transition(out)
    frag.out.add_epsilon_transition(frag.start)
    return Fragment(start, out)


def add_question_mark(frag):
    """Add a question mark to a fragment"""
    start = State()
    out = State()
    start.add_epsilon_transition(frag.start)
    start.add_epsilon_transition(out)
    frag.out.add_epsilon_transition(out)
    return Fragment(start, out)


def build_automaton(regex):
    """Parse a postfix regular expression into a fragment"""
    stack = []
    for char in regex:
        if char == Operator.UNION.symbol:
            if len(stack) < 2:
                raise Exception("Invalid regular expression. Not enough operands for union operator.")

            frag2 = stack.pop()
            frag1 = stack.pop()
            stack.append(add_union(frag1, frag2))
        elif char == Operator.CONCAT.symbol:
            if len(stack) < 2:
                raise Exception("Invalid regular expression. Not enough operands for concatenation operator.")

            frag2 = stack.pop()
            frag1 = stack.pop()
            stack.append(add_concat(frag1, frag2))
        elif char == Operator.KLEENE_STAR.symbol:
            if len(stack) < 1:
                raise Exception("Invalid regular expression. Not enough operands for kleene star operator.")

            frag = stack.pop()
            stack.append(add_kleene_star(frag))
        elif char == Operator.KLEENE_PLUS.symbol:
            if len(stack) < 1:
                raise Exception("Invalid regular expression. Not enough operands for kleene plus operator.")

            frag = stack.pop()
            stack.append(add_kleene_plus(frag))
        elif char == Operator.QUESTION_MARK.symbol:
            if len(stack) < 1:
                raise Exception("Invalid regular expression. Not enough operands for question mark operator.")

            frag = stack.pop()
            stack.append(add_question_mark(frag))
        else:
            stack.append(add_symbol(char))
    return stack.pop()


def get_states(initial_state):
    """
    Get the set of states that are reachable from the state.
    :param initial_state:
    :param state:
    :return:
    """
    states = set()
    _get_states(initial_state, states)
    return states


def _get_states(current_state, states):
    """
    Get the set of states that are reachable from the state.
    :param state:
    :return:
    """
    if current_state in states:
        return
    states.add(current_state)
    for next_state in current_state.get_epsilon_transitions():
        _get_states(next_state, states)

    for symbol in current_state.transitions:
        for next_state in current_state.transitions[symbol]:
            _get_states(next_state, states)


def get_alphabet(regex):
    """
    Get the alphabet of the regular expression.
    :param regex:
    :return:
    """
    alphabet = set()
    operators = [Operator.KLEENE_STAR.symbol, Operator.CONCAT.symbol, Operator.UNION.symbol]
    for char in regex:
        if char not in alphabet and char not in operators:
            alphabet.add(char)
    return alphabet


def get_transitions(state):
    """
    Get the transitions of the state.
    :param state:
    :return:
    todo:
        Just gets the transitions for the start state, need to recursively get the transitions for all states.
    """
    transitions = {}
    return transitions


def _get_transitions(state, transitions):
    """
    Get the transitions and the epsilon transitions of the state.
    :param state:
    :return:
    """
    if state in transitions:
        return
    transitions[state] = {}
    for symbol in state.transitions:
        transitions[state][symbol] = state.transitions[symbol]
    transitions[state][Operator.EPSILON.symbol] = state.epsilon_transitions
    for next_state in state.epsilon_transitions:
        _get_transitions(next_state, transitions)


class NFA:
    """
    A non-deterministic finite automaton.
    """

    def __init__(self, regex):
        self.regex = regex
        self.start = None
        self.end = None
        self.automaton = None

        if regex == '' or regex == Operator.EPSILON.symbol:
            self.end = self.start
        else:
            self.automaton = build_automaton(regex)
            self.start = self.automaton.start
            self.end = self.automaton.out
            self.end.set_is_accepting(True)
            self.accepting_states = {self.end}
        self.grammar = self.get_grammar()

    def get_grammar(self):
        """
        Get the grammar of the NFA.
        :return:
        """
        states = get_states(self.start)
        alphabet = get_alphabet(self.regex)
        accepting_states = self.accepting_states
        transitions = get_transitions(self.start)
        return Grammar(states, alphabet, self.start, accepting_states, transitions)
