from src.regex.state import State
from src.regex.operators import Operator


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


def add_kleene(frag):
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
    start.add_transition(symbol, out)
    return Fragment(start, out)


def build_automaton(regex):
    """Parse a postfix regular expression into a fragment"""
    stack = []
    for char in regex:
        if char == Operator.UNION.value:
            frag2 = stack.pop()
            frag1 = stack.pop()
            stack.append(add_union(frag1, frag2))
        elif char == Operator.CONCAT.value:
            frag2 = stack.pop()
            frag1 = stack.pop()
            stack.append(add_concat(frag1, frag2))
        elif char == Operator.KLEENE_STAR.value:
            frag = stack.pop()
            stack.append(add_kleene(frag))
        else:
            stack.append(add_symbol(char))
    return stack.pop()


class NFA:
    """
    A non-deterministic finite automaton.
    """

    def __init__(self, regex):
        self.regex = regex
        self.start = None
        self.end = None
        self.accepting_states = self.end
        self.automaton = None

        if regex == '' or regex == Operator.EPSILON.value:
            self.end = self.start
        else:
            self.automaton = build_automaton(regex)
            self.start = self.automaton.start
            self.end = self.automaton.out
            self.end.set_is_accepting(True)
