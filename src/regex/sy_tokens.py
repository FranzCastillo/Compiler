class SyToken:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __eq__(self, other):
        return self.type == other.token_type and self.value == other.value

    def __str__(self):
        return f"{self.value}"
