from src.yalex.regex_parser import RegexParser
from src.regex.operators_values import EPSILON, CONCAT


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
        self.rules = {}  # {rule: {regex: return}}
        self.process_rules(self.rules_content)
        self.replace_identifiers()
        self.replace_rules()
        self.parse_rules()

    def process_rules(self, rules_content: str):
        """
        Process the identifiers/rules from the file content and store them in dictionaries.
        """
        lines = rules_content.split("\n")
        # Remove empty lines
        lines = [line for line in lines if line.strip() != ""]

        i = 0
        while i < len(lines):
            line = lines[i].strip()
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
                j = i + 2
                while j < len(lines) and lines[j].strip().startswith("|"):
                    next_rule = lines[j].strip()
                    next_rule_parts = next_rule.split("{")
                    rule_regex = next_rule_parts[0].strip()[1:]  # Remove the '|'
                    # rule_return = next_rule_parts[1].replace('}', '').strip()
                    rule_return = next_rule_parts[1].strip()[:-1]  # Remove the '}'
                    self.rules[parts[1]][rule_regex] = rule_return
                    j += 1
                i = j
            i += 1

    def replace_identifiers(self):
        """
        Replace the identifiers with the value of other identifiers if needed.
        """
        sorted_keys = sorted(self.identifiers.keys(), key=len, reverse=True)

        for key in sorted_keys:
            for identifier in self.identifiers:
                if key in self.identifiers[identifier]:
                    self.identifiers[identifier] = self.identifiers[identifier].replace(key,
                                                                                        f"({self.identifiers[key]})")

    def replace_rules(self):
        """
        Replace the rules with the value of other identifiers if needed.
        """
        sorted_keys = sorted(self.identifiers.keys(), key=len, reverse=True)

        new_rules = {}
        for rule in self.rules:
            new_rules[rule] = {}
            for regex in self.rules[rule].keys():
                new_regex = regex
                for key in sorted_keys:
                    if key in new_regex:
                        new_regex = new_regex.replace(key, f"({self.identifiers[key]})")
                new_rules[rule][new_regex] = self.rules[rule][regex]
        self.rules = new_rules

    def parse_rules(self):
        """
        Parse the rules from a yalex syntax to the internal regex syntax.
        """
        parser = RegexParser(self.identifiers)
        new_rules = {}
        for rule in self.rules:
            new_rules[rule] = {}
            for regex in self.rules[rule].keys():
                # Since the keys are the regex, we need to parse them and create new keys
                new_regex = parser.parse(regex)
                new_rules[rule][new_regex] = self.rules[rule][regex]
        self.rules = new_rules

    def get_full_regex(self):
        full_regex = f''
        for rule in self.rules:
            for regex in self.rules[rule].keys():
                full_regex += f"({EPSILON}{CONCAT}{regex})|"
        return full_regex[:-1]  # Remove the last '|'
