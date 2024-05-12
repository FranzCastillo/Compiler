from src.factory.factory import Factory


def main():
    factory = Factory(
        yalex_path="D:\\UVG\\Compiladores\\Compiler\\other\\yal\\TEST.yal",
        yapar_path="D:\\UVG\\Compiladores\\Compiler\\other\\yalp\\TEST.yalp",
        output_path="D:\\UVG\\Compiladores\\Compiler\\other\\output"
    )
    factory.create_analyzer()


if __name__ == "__main__":
    main()
