from src.controller import Controller


def __main__():
    """
    todo:
        a+ → a.a*
        a? → a|ε
        [a-zA-Z] → a|b|c|...|z|A|B|C|...|Z
        Error stack
    """
    regex = 'a(a|ba)*|c*a'
    # regex = 'a(a|b)*b'
    # regex = 'a*|b'

    chain = "ab"

    controller = Controller()
    controller.regex = regex
    controller.chain = chain
    controller.process_grammars()
    controller.view_nfa("NFA")
    controller.view_dfa("DFA")
    controller.view_min_dfa("Min_DFA")


if __name__ == "__main__":
    __main__()
