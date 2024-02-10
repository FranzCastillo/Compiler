from src.controller import Controller


def __main__():
    regex = 'a*|b*'
    # regex = 'a(a|b)*b'
    # regex = 'a+d|b'
    # regex = 'a[a-e]*b'
    # regex = '(a|b)+abc?'
    # regex = 'a+b?'
    regex = '(a|b|c)+'
    chain = 'abc'

    try:
        controller = Controller(regex)
        controller.chain = chain
        print(f"NFA ({controller.chain_accepted_nfa(chain)}):\n{controller.simulate_nfa(chain)}")
        print(f"DFA ({controller.chain_accepted_dfa(chain)}):\n{controller.simulate_dfa(chain)}")
        print(f"Min DFA ({controller.chain_accepted_min_dfa(chain)}):\n{controller.simulate_min_dfa(chain)}")
        print(f"Direct DFA ({controller.chain_accepted_direct_dfa(chain)}):\n{controller.simulate_direct_dfa(chain)}")
        print(
            f"Min Direct DFA ({controller.chain_accepted_min_direct_dfa(chain)}):\n{controller.simulate_min_direct_dfa(chain)}"
        )
        controller.view_automatons()
        controller.view_syntax_tree()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    __main__()
