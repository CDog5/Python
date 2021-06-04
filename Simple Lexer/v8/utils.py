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
    def __init__(self, var):
        self.message = f'Undefined variable {var}.'
        super().__init__(self.message)
class VarEditError(Exception):
    def __init__(self, token):
        self.message = f'Cannot edit builtin variable {token.token}'
        super().__init__(self.message)
#IF THERE IS NOT A SPECIFIC ERROR CLASS, USE THIS
class InvalidSyntaxError(Exception):
    def __init__(self, error):
        self.message = error
        super().__init__(self.message)

class UnsupportedOperandError(Exception):
    def __init__(self, operand,tp1,tp2):
        self.message = f"Unsupported operand {self.operand(operand)} for type: {tp1} {tp2}"
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
