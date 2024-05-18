from src.factory.factory import Factory


def main():
    try:
        factory = Factory(
            yalex_path="D:\\UVG\\Compiladores\\Compiler\\other\\yal\\EX1.yal",
            yapar_path="D:\\UVG\\Compiladores\\Compiler\\other\\yalp\\EX1.yalp",
            output_path="D:\\UVG\\Compiladores\\Compiler\\other\\output"
        )
        factory.create_analyzer()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
