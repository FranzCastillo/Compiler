from src.controller import Controller


def __main__():
    """
    todo:
        a+ → a.a*
        a? → a|ε
        [a-zA-Z] → a|b|c|...|z|A|B|C|...|Z
        Error stack
    """
    # regex = 'a(a|ba)*|c*a'
    # regex = 'a(a|b)*b'
    # regex = 'a*|b'
    regex = 'c*|b(a|b)*a(a|b)*|a(a|b)*b'

    chain = "ab"

    controller = Controller()
    controller.regex = regex
    controller.chain = chain
    controller.run()


if __name__ == "__main__":
    __main__()
