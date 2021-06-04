VERSION = 9.0
class TokenType:
    FLOAT = 'FLOAT'
    INT = 'INT'
    IDENTIFIER = 'IDENTIFIER'
    STR = 'STR'
    COMMENT = 'COMMENT'
    MULT = 'MULT'
    DIV = 'DIV'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    SPACE = 'SPACE'
    NEWLINE = 'NEWLINE'
    SEMICOLON = 'SEMICOLON'
    COLON = 'COLON'
    RCURLY = 'RCURLY'
    LCURLY = 'LCURLY'
    LSQUARE = 'LSQUARE'
    RSQUARE = 'RSQUARE'
    COMMA = 'COMMA'
    ASSIGN = 'ASSIGN'
    LTE = 'LTE'
    GTE = 'GTE'
    LT = 'LT'
    GT = 'GT'
    EQ = 'EQ'
    FULLSTOP = 'FULLSTOP'
    EXCLAIM = 'EXCLAIM'
    RES_CALC = 'RES_CALC'
    RES_SETVAR = 'RES_SETVAR'
    PLUSMINUS = (PLUS,MINUS)

class UndefinedVarError(Exception):
    def __init__(self, var,line=None):
        self.message = f'Line {line}: Undefined variable {var}.'
        super().__init__(self.message)
class VarEditError(Exception):
    def __init__(self, token,line=None):
        self.message = f'Line {line}: Cannot edit builtin variable {token.token}'
        super().__init__(self.message)
class ConstEditError(Exception):
    def __init__(self, token,line=None):
        self.message = f'Line {line}: Cannot edit constant {token}'
        super().__init__(self.message)
#IF THERE IS NOT A SPECIFIC ERROR CLASS, USE THIS
class InvalidSyntaxError(Exception):
    def __init__(self, error,line=None):
        self.message = f'Line {line}: {error}'
        super().__init__(self.message)

class UnsupportedOperandError(Exception):
    def __init__(self, operand,tp1,tp2,line=None):
        self.message = f'Line {line}: Unsupported operand {self.operand(operand)} for type: {tp1} {tp2}'
        super().__init__(self.message)
    def operand(self,method):
        if method == TokenType.MINUS:
            return '-'
        elif method == TokenType.PLUS:
            return '+'
        elif method == TokenType.MULT:
            return '*'
        elif method == TokenType.DIV:
            return '/'
