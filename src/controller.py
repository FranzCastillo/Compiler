from src.yalex.lex_analyzer_factory import create_lex_analyzer


def run_yal_file(print_console: callable, yal_path: str):
    try:
        create_lex_analyzer(
            yal_path,
            "output/lex_analyzer"
        )
    except Exception as e:
        print_console(f"Error: {e}")


class Controller:
    def __init__(self, regex=None):
        self.regex = regex
        self.direct_dfa = None
        self.direct_dfa_grammar = None

    def run_yalp_file(self, print_console: callable, content: str):
        pass

    def set_regex(self, regex):
        self.regex = regex
        self.process_grammars()
