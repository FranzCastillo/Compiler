from src.controller import Controller


def __main__():
    """
    todo:
        [a-zA-Z] → a|b|c|...|z|A|B|C|...|Z
    """
    # regex = 'a(a|ba)*|c*a'
    # regex = 'a(a|b)*b'
    # regex = 'a*|b'
    regex = '(ab)+a'

    chain = "ab"

    controller = Controller()
    controller.regex = regex
    controller.chain = chain
    controller.run()


if __name__ == "__main__":
    __main__()
