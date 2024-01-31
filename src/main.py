from src.view.automaton import ViewAutomaton
from src.regex.nfa import NFA
from src.regex.shunting_yard import ShuntingYard


def __main__():
    regex = 'a.(a|b.a)*|c*.a'
    # regex = 'a(a|b)*b'
    # regex = 'a*|b'
    sy = ShuntingYard()
    sy.set_regex(regex)
    postfix = sy.get_postfix()

    nfa = NFA(postfix)
    nfa_grammar = nfa.get_grammar()

    view = ViewAutomaton(nfa, "NFA")
    view.view("NFA")


if __name__ == "__main__":
    __main__()
