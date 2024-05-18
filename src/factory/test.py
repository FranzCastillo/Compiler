from src.factory.factory import Factory


def main():
    factory = Factory(
        yalex_path="D:\\UVG\\Compiladores\\Compiler\\other\\yal\\MEDIUM.yal",
        yapar_path="D:\\UVG\\Compiladores\\Compiler\\other\\yalp\\MEDIUM.yalp",
        output_path="D:\\UVG\\Compiladores\\Compiler\\other\\output"
    )
    factory.create_analyzer()


if __name__ == "__main__":
    main()
