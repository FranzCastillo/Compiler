from src.yapar.file_parser import FileParser


def copy_slr_file(output_path: str) -> None:
    with open("../yapar/slr.py", "r") as file:
        with open(f"{output_path}/syntactic_analyzer.py", "w") as slr_file:
            slr_file.write(file.read())


class Factory:
    def __init__(self, yapar_file_path: str, output_path: str):
        self.yapar_file_path = yapar_file_path
        self.output_path = output_path
        self.tokens = None
        self.ignored_tokens = None
        self.productions = None

    def create_syntax_analyzer(self):
        file = FileParser(self.yapar_file_path)
        self.tokens = file.tokens
        self.ignored_tokens = file.ignored_tokens
        self.productions = file.productions
        copy_slr_file(self.output_path)
