class Token:
    def __init__(self, line: int, pos: int, lexeme: str, type: str):
        self.line = line
        self.pos = pos
        self.lexeme = lexeme
        self.type = type

    def __str__(self):
        return f"{self.line:02}:{self.pos:02} → {self.type} [{self.lexeme}]"
