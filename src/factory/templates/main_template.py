import argparse

from lexical_analyzer import Lexer
from syntactic_analyzer import SLR


def main(code_path: str):
    lexer = Lexer(code_path)
    parser = SLR(
        #TOKENS#,
        #IGNORED_TOKENS#,
        #PRODUCTIONS#
    )
    parser.build_lr0_automaton()

    print(f"First: {parser.first()}")
    print(f"Follow: {parser.follow()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Path to the code to be analyzed")
    parser.add_argument("code_path", type=str, help="Path to the code file")
    args = parser.parse_args()
    code_path = args.code_path
    main(code_path)
