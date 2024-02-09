from src.controller import Controller


def __main__():
    # regex = 'a(a|ba)*|c*a'
    # regex = 'a(a|b)*b'
    regex = 'a+d|b'
    # regex = 'a[a-e]*b'

    chain = "aad"

    controller = Controller(regex)
    try:
        pass

    except Exception as e:
        print(e)

    controller.chain = chain
    print(f"NFA: {controller.check_string_nfa(chain)}")
    print(f"DFA: {controller.check_string_dfa(chain)}")
    print(f"Minimized DFA: {controller.check_string_min_dfa(chain)}")
    # controller.view_automatons()


if __name__ == "__main__":
    __main__()
