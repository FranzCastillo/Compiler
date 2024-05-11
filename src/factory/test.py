from src.factory.factory import Factory


def main():
    factory = Factory(
        yalex_path="D:\\UVG\\Compiladores\\Compiler\\other\\yal\\EASY.yal",
        yapar_path="D:\\UVG\\Compiladores\\Compiler\\other\\yalp\\EASY.yalp",
        output_path="D:\\UVG\\Compiladores\\Compiler\\other\\output"
    )
    factory.create_analyzer()


if __name__ == "__main__":
    main()
