import argparse

from src.yalex.lex_analyzer_factory import create_lex_analyzer
from src.yapar.file_parser import FileParser
from src.yapar.slr import SLR
from src.yapar.lr_symbol import LrSymbol


def parse_args():
    parser = argparse.ArgumentParser(description="Yet Another Parser")
    parser.add_argument("yalp_path", type=str, help="Path to the yalp file")
    parser.add_argument("yalex_path", type=str, help="Path to the yalex file")
    parser.add_argument("output_path", type=str, help="Output path")
    return parser.parse_args()


def are_tokens_valid(yalex_tokens, yapar_tokens):
    for token in yapar_tokens:
        if token not in yalex_tokens:
            return False
    return True


def main():
    # Receive Parameters
    # args = parse_args()
    # yalp_path = args.yalp_path
    # yalex_path = args.yalex_path
    # output_path = args.output_path
    yalp_path = "D:\\UVG\\Compiladores\\Compiler\\other\\yalp\\Sintac2.yalp"
    yalex_path = "D:\\UVG\\Compiladores\\Compiler\\other\\yal\\CODE_Hard.yal"
    output_path = "D:\\UVG\\Compiladores\\Compiler\\other\\output"

    # Process the YALex File
    try:
        token_types = create_lex_analyzer(yalex_path, output_path)
        yapar_file = FileParser(yalp_path)
        tokens = yapar_file.tokens
        ignored_tokens = yapar_file.ignored_tokens
        productions = yapar_file.productions

        # if not are_tokens_valid(token_types, tokens):
        #     print("The tokens in the YALex file don't match the tokens in the YALp file")
        #     return

        slr = SLR(tokens, ignored_tokens, productions)
        temp = slr.goto(slr.initial_set, LrSymbol("E"))
        print("END")

    except Exception as e:
        print(f"Error processing the YALex file: {e}")
        return


if __name__ == "__main__":
    main()
