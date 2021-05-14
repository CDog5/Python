DEBUG = False

class ParserError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Could not lex text. Illegal chars may be in this text."
class LexerError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "Could not parse text. Illegal chars may be in this text."
class FileError(Exception):
    def __init__(self,f):
        self.f = f
    def __str__(self):
        return f"Could not find file: {self.f}"

