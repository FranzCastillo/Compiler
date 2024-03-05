def remove_comments(content):
    result = ""
    in_comment = False
    i = 0
    while i < len(content):
        if content[i:i + 2] == '(*':
            in_comment = True
            i += 2
        elif content[i:i + 2] == '*)':
            in_comment = False
            i += 2
        elif not in_comment:
            result += content[i]
            i += 1
        else:
            i += 1
    return result


def split_file(content: str):
    content = content
    if not content:
        raise Exception("Empty file")
    content = remove_comments(content)
    try:
        d, r, c = content.split("%%")
    except ValueError:
        raise Exception("Invalid file format. Missing %%")
    return d.strip(), r.strip(), c.strip()


class FileParser:
    def __init__(self, file_content: str):
        self.file_content = file_content
        self.declarations, self.rules, self.code = split_file(file_content)
        self.variables = {}
        self.process_rules(self.rules)

    def process_rules(self, rules: str):
        rules = rules.split("\n")
        for rule in rules:
            rule.strip()
            if not rule:
                continue
            parts = rule.split(" ")
            if parts[0] == "let":
                self.variables[parts[1]] = ' '.join(parts[3:])


