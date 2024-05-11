from src.factory.yalex_factory import Factory as YalexFactory
from src.factory.yapar_factory import Factory as YaparFactory
from src.factory.main_factory import Factory as MainFactory


def copy_token_file(output_path: str) -> None:
    with open("../structures/token.py", "r") as file:
        with open(f"{output_path}/custom_token.py", "w") as token_file:
            token_file.write(file.read())


class Factory:
    def __init__(self, yalex_path: str, yapar_path: str, output_path: str):
        self.yalex_path = yalex_path
        self.yal_factory = YalexFactory(yalex_path, output_path)

        self.yapar_path = yapar_path
        self.yap_factory = YaparFactory(yapar_path, output_path)

        self.main_factory = MainFactory(output_path)

        self.output_path = output_path

    def create_analyzer(self):
        self.main_factory.create_main()

        # YALex Files
        copy_token_file(self.output_path)
        self.yal_factory.create_lex_analyzer()

        # YAPar Files
        self.yap_factory.create_parser()
