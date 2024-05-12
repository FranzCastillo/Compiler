from src.yapar.file_parser import FileParser


def copy_slr_file(output_path: str) -> None:
    with open("../yapar/slr.py", "r", encoding='utf-8') as file:
        with open(f"{output_path}/syntactic_analyzer.py", "w", encoding='utf-8') as slr_file:
            slr_file.write(
                file.read()
                .replace('src.regex.state_id', 'state_id')
                .replace('src.yapar.lr_set', 'lr_set')
                .replace('src.yapar.lr_symbol', 'lr_symbol')
            )


def copy_state_id_file(output_path: str) -> None:
    with open("../regex/state_id.py", "r", encoding='utf-8') as file:
        with open(f"{output_path}/state_id.py", "w") as state_id_file:
            state_id_file.write(file.read())


def copy_lr_set_file(output_path: str) -> None:
    with open("../yapar/lr_set.py", "r", encoding='utf-8') as file:
        with open(f"{output_path}/lr_set.py", "w", encoding='utf-8') as lr_set_file:
            lr_set_file.write(file.read())


def copy_lr_symbol_file(output_path: str) -> None:
    with open("../yapar/lr_symbol.py", "r", encoding='utf-8') as file:
        with open(f"{output_path}/lr_symbol.py", "w", encoding='utf-8') as lr_symbol_file:
            lr_symbol_file.write(file.read())


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
        copy_state_id_file(self.output_path)
        copy_lr_set_file(self.output_path)
        copy_lr_symbol_file(self.output_path)
