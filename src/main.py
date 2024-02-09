from src.controller import Controller


def __main__():
    # regex = 'a(a|ba)*|c*a'
    # regex = 'a(a|b)*b'
    # regex = 'a+d|b'
    # regex = 'a[a-e]*b'
    regex = '(a|b)*abb'

    chain = "abcdbveab"

    controller = Controller(regex)
    try:
        pass

    except Exception as e:
        print(e)

    controller.chain = chain
    print(f"NFA ({controller.chain_accepted_nfa(chain)}):\n{controller.simulate_nfa(chain)}")
    print(f"DFA ({controller.chain_accepted_dfa(chain)}):\n{controller.simulate_dfa(chain)}")
    print(f"Min DFA ({controller.chain_accepted_min_dfa(chain)}):\n{controller.simulate_min_dfa(chain)}")
    controller.view_automatons()


if __name__ == "__main__":
    __main__()
