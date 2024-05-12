from src.factory.yalex_factory import Factory as YalexFactory
from src.factory.yapar_factory import Factory as YaparFactory

class Factory:
    def __init__(self, output_path: str, yal_factory: YalexFactory, yap_factory: YaparFactory):
        self.output_path = output_path
        self.yal_factory = yal_factory
        self.yap_factory = yap_factory

    def create_main(self):
        self.yal_factory.create_lex_analyzer()
        self.yap_factory.create_syntax_analyzer()

        with open("templates/main_template.py", "r", encoding='utf-8') as file:
            with open(f"{self.output_path}/main.py", "w", encoding='utf-8') as main_file:
                main_file.write(
                    file.read()
                    .replace('#TOKENS#', str(self.yap_factory.tokens))
                    .replace('#IGNORED_TOKENS#', str(self.yap_factory.ignored_tokens))
                    .replace('#PRODUCTIONS#', str(self.yap_factory.productions))
                )
