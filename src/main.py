from src.controller import Controller


def __main__():
    # regex = 'a(a|ba)*|c*a'
    # regex = 'a(a|b)*b'
    # regex = 'a+d|b'
    regex = 'a[a-e]*b'

    chain = "ab"

    try:
        controller = Controller()
        controller.regex = regex
        controller.chain = chain
        controller.run()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    __main__()
