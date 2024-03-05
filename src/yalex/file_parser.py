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
        self.declarations_content, self.rules_content, self.code_content = split_file(file_content)
        self.identifiers = {}
        self.rules = {}
        self.process_rules(self.rules_content)

    def process_rules(self, rules_content: str):
        lines = rules_content.split("\n")

        for i in range(len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            parts = line.split(" ")
            if parts[0] == "let":
                self.identifiers[parts[1]] = ' '.join(parts[3:])
            elif parts[0] == "rule":
                self.rules[parts[1]] = {}
                # The one without the '|' is the first specific rule
                first_rule = lines[i + 1].strip()
                first_rule_parts = first_rule.split("{")
                rule_regex = first_rule_parts[0].strip()
                rule_return = first_rule_parts[1].replace('}', '').strip()
                self.rules[parts[1]][rule_regex] = rule_return

                # Keep reading until no more specific rules are found for this rule
                for j in range(i + 2, len(lines)):
                    if lines[j].strip().startswith("|"):
                        next_rule = lines[j].strip()
                        next_rule_parts = next_rule.split("{")
                        rule_regex = next_rule_parts[0].replace('|', '').strip()
                        rule_return = next_rule_parts[1].replace('}', '').strip()
                        self.rules[parts[1]][rule_regex] = rule_return
                    else:
                        # To update the index of the main loop to the last line read
                        i = j
                        break
