import argparse

from lexical_analyzer import Lexer
from syntactic_analyzer import SLR
from prettytable import PrettyTable


def main(code_path: str):
    lexer = Lexer(code_path)
    parser = SLR(
        #TOKENS#,
        #IGNORED_TOKENS#,
        #PRODUCTIONS#
    )
    parser.build_lr0_automaton()
    parser.build_parsing_table()

    # Start the parsing process
    was_accepted = False
    process: list[dict] = []
    while lexer.has_next_token():
        token = lexer.get_next_token()
        action, was_accepted = parser.parse(token)
        process.append({
            "stack": parser.parsing_stack.copy(),
            "symbols": parser.parsing_symbols.copy(),
            "action": action,
        })

    table = PrettyTable(["STACK", "SYMBOLS", "ACTION"])
    table.align = "l"

    for step in process:
        new_stack = ""
        for state in step["stack"]:
            new_stack += f"{state.set_id} "

        new_symbols = ""
        for symbol in step["symbols"]:
            new_symbols += f"{symbol} "

        if step["action"][0] == "SHIFT":
            new_action = "desplazar"
        elif step["action"][0] == "REDUCE":
            new_action = f"reducir mediante {step['action'][1]['production_head']} → {step['action'][1]['production_body']}"
        elif step["action"][0] == "ACCEPT":
            new_action = "aceptar"
        else:
            new_action = "ERROR"

        table.add_row([new_stack, new_symbols, new_action])

    print(table)

    if was_accepted:
        print("The input was accepted!")
    else:
        print("The input was NOT accepted")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Path to the code to be analyzed")
    parser.add_argument("code_path", type=str, help="Path to the code file")
    args = parser.parse_args()
    code_path = args.code_path
    main(code_path)
