def remove_comments(file_content: str) -> str:
    """
    Return the content of the file as a string (Except the comments)
    """
    result = ""
    in_comment = False
    i = 0
    while i < len(file_content):
        if file_content[i:i + 2] == '/*':
            in_comment = True
            i += 2
        elif file_content[i:i + 2] == '*/':
            if not in_comment:
                result += file_content[i:i + 2]
            in_comment = False
            i += 2
        elif not in_comment:
            result += file_content[i]
            i += 1
        else:
            i += 1
    return result


def split_file(file_content: str) -> tuple:
    """
    Split the content of a file into the tokens and productions sections
    """
    content = file_content
    if not content:
        raise Exception("Empty file")
    content = remove_comments(content)
    try:
        tokens_content, productions_content = content.split("%%")
    except ValueError:
        raise Exception("Invalid file format. Missing %%")
    return tokens_content.strip(), productions_content.strip()


def process_token_section(token_section: str) -> tuple:
    """
    Process the token section of the file
    """
    tokens = set()
    ignored_tokens = set()
    token_lines = token_section.split("\n")

    for line in token_lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("%token"):
            temp = line.split(" ")
            if len(temp) < 2:
                raise Exception(f"Invalid token line: {line}")

            for token in temp[1:]:
                tokens.add(token.upper())

        elif line.startswith("IGNORE"):
            temp = line.split(" ")
            if len(temp) < 2:
                raise Exception(f"Invalid ignore line: {line}")

            for token in temp[1:]:
                if token not in tokens:
                    raise Exception(f"Token {token} not defined.")
                ignored_tokens.add(token.upper())

    return tokens, ignored_tokens


class FileParser:
    def __init__(self, file_path: str):
        try:
            # Read the file
            with open(file_path, 'r') as file:
                content = file.read()

            # Split the file into tokens and productions
            tokens_section, productions_section = split_file(content)
            self.tokens, self.ignored_tokens = process_token_section(tokens_section)
        except Exception as e:
            raise Exception(f"Error processing the YAPar file: {e}")
