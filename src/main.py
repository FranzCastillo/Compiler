from src.regex.shunting_yard import ShuntingYard
from src.regex.nfa import NFA
from src.regex.dfa import DFA
from src.view.automaton import ViewAutomaton


def __main__():
    """
    todo:
        a+ → a.a*
        a? → a|ε
    """
    regex = 'a(a|ba)*|c*a'
    # regex = 'a(a|b)*b'
    # regex = 'a*|b'
    sy = ShuntingYard()
    sy.set_regex(regex)
    postfix = sy.get_postfix()

    nfa = NFA(postfix)
    nfa_grammar = nfa.get_grammar()

    dfa = DFA(nfa_grammar)
    dfa_grammar = dfa.get_grammar(show_death_state=False)

    view = ViewAutomaton(nfa_grammar, "NFA")
    view.view("NFA")

    view = ViewAutomaton(dfa_grammar, "DFA")
    view.view("DFA")


if __name__ == "__main__":
    __main__()
