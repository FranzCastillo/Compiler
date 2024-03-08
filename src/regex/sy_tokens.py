class SyToken:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __eq__(self, other):
        return self.type == other.token_type and self.value == other.value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"

    def __hash__(self):
        return hash((self.type, self.value))
