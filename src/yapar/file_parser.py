def read_file(file_path: str) -> str:
    """
    Read the content of a file and return it as a string (Except the comments)
    """
    with open(file_path, "r") as file:
        content = file.read()

    # Remove comments
    result = ""
    in_comment = False
    i = 0
    while i < len(content):
        if content[i:i + 2] == '/*':
            in_comment = True
            i += 2
        elif content[i:i + 2] == '*/':
            if not in_comment:
                result += content[i:i + 2]
            in_comment = False
            i += 2
        elif not in_comment:
            result += content[i]
            i += 1
        else:
            i += 1
    return result


class FileParser:
    def __init__(self, file_path: str):
        self.content = read_file(file_path)
        print(self.content)
