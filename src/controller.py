class Controller:
    def __init__(self, regex=None):
        self.regex = regex
        self.direct_dfa = None
        self.direct_dfa_grammar = None

    def run_yal_file(self, print_console: callable, content: str):
        try:
            pass
        except Exception as e:
            print_console(f"Error: {e}")

    def run_yalp_file(self, print_console: callable, content: str):
        pass

    def set_regex(self, regex):
        self.regex = regex
        self.process_grammars()
