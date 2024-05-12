from src.factory.main_factory import Factory as MainFactory
from src.factory.yalex_factory import Factory as YalexFactory
from src.factory.yapar_factory import Factory as YaparFactory


def copy_token_file(output_path: str) -> None:
    with open("../structures/token.py", "r") as file:
        with open(f"{output_path}/custom_token.py", "w") as token_file:
            token_file.write(file.read())


class Factory:
    def __init__(self, yalex_path: str, yapar_path: str, output_path: str):
        copy_token_file(output_path)

        yal_factory = YalexFactory(yalex_path, output_path)

        yap_factory = YaparFactory(yapar_path, output_path)

        self.main_factory = MainFactory(output_path, yal_factory, yap_factory)

        self.output_path = output_path

    def create_analyzer(self):
        self.main_factory.create_main()
