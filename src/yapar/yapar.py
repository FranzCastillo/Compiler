import argparse

from src.yalex.lex_analyzer_factory import create_lex_analyzer


def parse_args():
    parser = argparse.ArgumentParser(description="Yet Another Parser")
    parser.add_argument("yalp_path", type=str, help="Path to the yalp file")
    parser.add_argument("yalex_path", type=str, help="Path to the yalex file")
    parser.add_argument("output_path", type=str, help="Output path")
    return parser.parse_args()


def main():
    # Receive Parameters
    # args = parse_args()
    # yalp_path = args.yalp_path
    # yalex_path = args.yalex_path
    # output_path = args.output_path
    yalp_path = ""
    yalex_path = "D:\\UVG\\Compiladores\\Compiler\\other\\yal\\CODE_Hard.yal"
    output_path = "D:\\UVG\\Compiladores\\Compiler\\other\\output"

    # Process the YALex File
    try:
        create_lex_analyzer(yalex_path, output_path)
    except Exception as e:
        print(f"Error processing the YALex file: {e}")
        return


if __name__ == "__main__":
    main()
