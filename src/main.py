from src.regex.shunting_yard import ShuntingYard
from src.regex.nfa import NFA
from src.regex.dfa import DFA
from src.regex.min_dfa import MinifiedDFA
from src.view.automaton import ViewAutomaton


def __main__():
    """
    todo:
        a+ → a.a*
        a? → a|ε
        [a-zA-Z] → a|b|c|...|z|A|B|C|...|Z
        Error stack
    """
    # regex = 'a(a|ba)*|c*a'
    regex = 'a(a|b)*b'
    # regex = 'a*|b'
    sy = ShuntingYard()
    sy.set_regex(regex)
    postfix = sy.get_postfix()

    nfa = NFA(postfix)
    nfa_grammar = nfa.get_grammar()

    dfa = DFA(nfa_grammar)
    dfa_grammar = dfa.get_grammar(show_death_state=True)

    min_dfa = MinifiedDFA(dfa_grammar)
    min_dfa_grammar = min_dfa.get_grammar()

    view = ViewAutomaton(nfa_grammar)
    view.view("NFA")

    view = ViewAutomaton(dfa_grammar)
    view.view("DFA")

    view = ViewAutomaton(min_dfa_grammar)
    view.view("MinDFA")


if __name__ == "__main__":
    __main__()
