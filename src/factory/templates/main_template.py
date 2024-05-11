import argparse

from lexical_analyzer import Lexer


def main(code_path: str):
    lexer = Lexer(code_path)

    while lexer.has_next_token():
        token = lexer.get_next_token()
        print(token)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Path to the code to be analyzed")
    parser.add_argument("code_path", type=str, help="Path to the code file")
    args = parser.parse_args()
    code_path = args.code_path
    main(code_path)
