#This lexer relies on regex to work
import re
from utils import *
class Vars:
    def __init__(self):
        self.vars={"__name__":"'<stdin>'"}
        self.user_vars={}
        self.builtins = ['__name__','__vars__','__uservars__']
    def get_var(self,name):
            if name == '__uservars__':
                return str(self.user_vars)
            elif name == '__vars__':
                x = self.vars
                x.update(self.user_vars)
                return str(x)
            try:
                return self.vars[name]
            except:
                raise UndefinedVarError(name) from None
    def get_builtins(self):
        return self.builtins
    def set_var(self,name,val):
        res=Parser().parse(Lexer().lex(val)).calculate().token
        self.user_vars[name] = res
    def direct_set_var(self,name,val):
        self.vars[name] = val
varhandler = Vars()
def get_values(lVals):
    res = []
    for val in lVals:
        if type(val) not in [list, set, tuple]:
            res.append(val)
        else:
            res.extend(get_values(val))
    return res


class Token:
    def __init__(self,inp,tktype,pos,endpos):
        self.type = tktype
        self.token = str(inp)
        self.start = pos
        self.end = endpos
    def to_actual_type(self):
        a = {TokenType.INT:lambda x: int(x),TokenType.FLOAT:lambda x: float(x),TokenType.STR:lambda x: str(x)}
        return a.get(self.type,TokenType.STR)(self.token)
    def as_list(self):
        return[self.token,self.type,self.start,self.end]
    def as_tuple(self):
        return(self.token,self.type,self.start,self.end)
    def as_strf(self,strf):
        formats=[("%v",self.token),("%t",self.type),("%s",self.start),("%e",self.end)]
        for frmt in formats:
            strf = strf.replace(frmt[0],str(frmt[1]))
        return strf
    def as_dict(self):
        return{'TOKEN':self.token,'TOKEN_TYPE':self.type,'START_POS':self.start,'END_POS':self.end}
class LexedItem:
    def __init__(self,out):
        self.__list = out
    def filter(self,keep=None,remove=None):
        out=[]
        if not remove:
            remove=[]
        if not keep:
            a = Lexer()
            a.lex('1')
            keep = [TokenType.FLOAT, TokenType.INT, TokenType.IDENTIFIER, TokenType.STR, TokenType.COMMENT, TokenType.MULT, TokenType.DIV, TokenType.PLUS,TokenType.MINUS, TokenType.LPAREN, TokenType.RPAREN, TokenType.SPACE, TokenType.NEWLINE,
                    TokenType.SEMICOLON, TokenType.COLON, TokenType.RCURLY, TokenType.LCURLY, TokenType.LSQUARE, TokenType.RSQUARE, TokenType.COMMA, TokenType.ASSIGN, TokenType.LTE, TokenType.GTE, TokenType.LT, TokenType.GT, TokenType.EQ,
                    TokenType.FULLSTOP, TokenType.EXCLAIM]
        for token in self.__list:
            if token.type in keep and token.type not in remove:
                out.append(token)
        return out
    def reconstruct(self):
        out=''
        for x in self.__list:
            out+=x.token
        return out
    def reconstruct_file(self,path):
        data = self.reconstruct()
        with open(path,'w') as f:
            f.write(data)
    #You can display the output as a list of token objects, or have them formatted nicely
    def as_raw(self):
        return self.__list
    def as_dict(self):
        return [x.as_dict() for x in self.__list]
    def as_list(self):
        return [x.as_list() for x in self.__list]
    def as_tuple(self):
        return [x.as_tuple() for x in self.__list]
    def as_strf(self,strf):
        return [x.as_strf(strf) for x in self.__list]
class ParsedItem:
    def __init__(self,out):
        self.__list = out
    def convert_tktype(self,tk):
        if tk.type == TokenType.STR:
            tkn = str(tk.token)
            tkn = tkn[1:len(tkn)-1]
            return str(tkn)
        if tk.type == TokenType.FLOAT:
            return float(tk.token)
        if tk.type == TokenType.INT:
            return int(tk.token)
    def calc(self,tk1,tk2,method,typ,allowed,tp1,tp2):

        if method in allowed:
            if method == TokenType.MINUS:
                return Token(tk1 - tk2,typ,0,0)
            elif method == TokenType.PLUS:
                return Token(tk1 + tk2,typ,0,0)
            elif method == TokenType.MULT:
                return Token(tk1 * tk2,typ,0,0)
            elif method == TokenType.DIV:
                res = tk1 / tk2
                if res.is_integer() and typ == TokenType.INT:
                    res = int(res)
                else:
                    res = float(res)
                    typ = TokenType.FLOAT
                return Token(str(res),typ,0,0)
                
        raise UnsupportedOperandError(method,tp1,tp2) from None
    def tk_type(self,tk):
        if type(tk) is int:
            return TokenType.INT
        if type(tk) is float:
            return TokenType.FLOAT
        if type(tk) is str:
            return TokenType.STR
    def convert_var(self,var):
        if (var.startswith("'") or var.startswith('"')) and (var.endswith("'") or var.endswith('"')):
            return var[1:len(var)-1]
        else:
            return var
    def get_vars(self,tpl):
        rettpl=[]

        if tpl[0].type == TokenType.IDENTIFIER and tpl[1].type != TokenType.ASSIGN:
            var = varhandler.get_var(tpl[0].token)
            rettpl.append(Token(var,self.tk_type(self.convert_tktype(Lexer().lex(varhandler.get_var(tpl[0].token)).as_raw()[0])),0,0))
        else:
            rettpl.append(tpl[0])
        rettpl.append(tpl[1])
        if tpl[2].type == TokenType.IDENTIFIER and tpl[1].type != TokenType.ASSIGN:
            var = varhandler.get_var(tpl[2].token)
            rettpl.append(Token(var,self.tk_type(self.convert_tktype(Lexer().lex(varhandler.get_var(tpl[2].token)).as_raw()[0])),0,0))
        else:
            rettpl.append(tpl[2])
        return tuple(rettpl)
    def deconvert_tk(self,tk):
        if tk.type == TokenType.STR:
            out = ''
            var = tk.token
            if not (var.startswith("'") or var.startswith('"')):
                out += "'"
            out += tk.token
            if not(var.endswith("'") or var.endswith('"')):
                out += "'"
            return out
        else:
            return tk.token
    def convert_tktypes(self,tpl):
        if len(tpl) < 3:
            return None
        token1=tpl[0]
        method=tpl[1]
        token2=tpl[2]
        if token1.type == TokenType.IDENTIFIER and method.type == TokenType.ASSIGN and token2.type in (TokenType.IDENTIFIER,TokenType.INT,TokenType.FLOAT,TokenType.STR):
            if token2.type == TokenType.IDENTIFIER:
                token2 = self.convert_var(varhandler.get_var(token2.token))
            else:
                token2 = self.deconvert_tk(token2)            
            if token1.token in varhandler.get_builtins():
                raise VarEditError(token1) from None
            varhandler.set_var(token1.token,token2)
            return None
        tpl = self.get_vars(tpl)
        token1=tpl[0]
        method=tpl[1]
        token2=tpl[2]
        
        if token1.type == TokenType.STR and token2.type == TokenType.STR:
            return self.calc(self.convert_tktype(token1),self.convert_tktype(token2),method.type,TokenType.STR,[TokenType.PLUS],token1.type,token2.type)
        elif (token1.type == TokenType.STR and token2.type == TokenType.INT) or (token1.type == TokenType.INT and token2.type == TokenType.STR):
            return self.calc(self.convert_tktype(token1),self.convert_tktype(token2),method.type,TokenType.STR,[TokenType.MULT],token1.type,token2.type)
        elif token1.type == TokenType.FLOAT or token2.type == TokenType.FLOAT and (token1.type != TokenType.STR and token2.type != TokenType.STR):
            return self.calc(self.convert_tktype(token1),self.convert_tktype(token2),method.type,TokenType.FLOAT,[TokenType.PLUS,TokenType.MULT,TokenType.DIV,TokenType.MINUS],token1.type,token2.type)
        elif token1.type == TokenType.INT and token2.type == TokenType.INT:
            return self.calc(int(token1.token),int(token2.token),method.type,TokenType.INT,[TokenType.PLUS,TokenType.MULT,TokenType.DIV,TokenType.MINUS],token1.type,token2.type)
        msg = ', '.join([str(x.as_tuple()) for x in tpl])
        raise InvalidSyntaxError(f"Unsupported type in {msg}.") from None

    def solve_tlayers(self,b):
        conttuples = False
        a=[]
        for layer in b:
            if type(layer) is tuple:
                conttuples = True
                a.append(self.solve_tlayers(layer))
            else:
                a.append(layer)
        res=self.convert_tktypes(a)
        return res

    #calculates the values
    def calculate(self):
        if len(self.__list) == 1 and type(self.__list[0])== Token:
            if self.__list[0].type == TokenType.IDENTIFIER:
                return Token(self.convert_var(varhandler.get_var(self.__list[0].token)),TokenType.RES_CALC,0,0)
            return self.__list[0]
        out=[]
        for c in self.__list:

            if type(c) is tuple:
                solved = self.solve_tlayers(c)
                if solved:
                    out.append(solved)
            else:
                out.append(c)
        out = self.solve_tlayers(out)
        if not out:
            return Token('SET VAR',TokenType.RES_SETVAR,None,None)
        return out

    #allows modification of all vals in tuples, and even in nested tuuples 
    def unpack_t(self,tpl,method):
        a=[]
        for t in tpl:
            if type(t) is tuple:
                a.append(self.unpack_t(t,method))
            elif type(t) is Token:
                a.append(method(t))
        return tuple(a)
    #unpacks multiple tuples in a list, depends on function above
    def unpack(self,method,lst=None):
        out=[]
        if not lst:
            lst = self.__list
        for item in lst:
            if type(item) is Token:
                out.append(method(item))
            elif type(item) is tuple:
                out.append(self.unpack_t(item,method))
        return out
    def unpack_strf_t(self,tpl,strf):
        a=[]
        for t in tpl:
            if type(t) is tuple:
                a.append(self.unpack_strf_t(t,strf))
            elif type(t) is Token:
                a.append(Token.as_strf(t,strf))
        return tuple(a)
    def unpack_strf(self,strf):
        out=[]
        for item in self.__list:
            if type(item) is Token:
                out.append(Token.as_strf(item,strf))
            elif type(item) is tuple:
                out.append(self.unpack_strf_t(item,strf))
        return out
    #You can display the output as a list of token objects, or have them formatted nicely
    def as_raw(self):
        return self.__list
    def as_dict(self):
        return self.unpack(Token.as_dict)
    
    def as_list(self):
        return self.unpack(Token.as_list)
    def as_tuple(self):
        return self.unpack(Token.as_tuple)
    def as_strf(self,strf):
        return self.unpack_strf(strf)
class ParsedList:
    def __init__(self,tokens):
        self.__list = tokens
    def ln_res(self):
        return ", ".join([x.calculate().token for x in self.__list])
    def as_tuple(self):
        return [x.as_tuple() for x in self.__list]
    def as_list(self):
        return [x.as_list() for x in self.__list]
    def as_dict(self):
        return [x.as_dict() for x in self.__list]
class Lexer:
    def __init__(self,types=None,other=None):
        if types:
            self.types = types
        else:
            #main identifiers. you could combine float&int, rename the types or even add more ones. Replace the hashtag in the comment for other denotations, such as // if needed
            self.types = {TokenType.FLOAT:r'(-\d*\.\d+|\d*\.\d+)',TokenType.INT:r'(-\d+|\d+)',TokenType.IDENTIFIER:r'\w+',TokenType.STR:r'(\".*?\"|\'.*?\')',TokenType.COMMENT:r'#.*'}
        if other:
            self.other = other
        else:
            # can add your own keywords here such as 'KW_IF':'IF'
            self.other = {TokenType.MULT:'*',TokenType.DIV:'/',TokenType.PLUS:'+',TokenType.MINUS:'-',TokenType.LPAREN:'(',TokenType.RPAREN:')',TokenType.SPACE:' ',TokenType.NEWLINE:'\n',TokenType.SEMICOLON:';',TokenType.COLON:':',TokenType.RCURLY:'{',TokenType.LCURLY:'}',
                          TokenType.LSQUARE:'[',TokenType.RSQUARE:']',TokenType.COMMA:',',TokenType.ASSIGN:'=',TokenType.LTE:'<=',TokenType.GTE:'>=',TokenType.LT:'<',TokenType.GT:'>',TokenType.EQ:'==',TokenType.FULLSTOP:'.',TokenType.EXCLAIM:'!'}
    def get_tktypes(self):
        return list(self.types.keys())+list(self.other.keys())
    def clean(self,out):
        tmp=[out[0]]
        for i in range(1,len(out)):
            if out[i].start > tmp[len(tmp)-1].end:
                tmp.append(out[i])
        return tmp
    #lex line by line
    def lex_lbl(self,path):
        varhandler.direct_set_var("__name__",path)
        out=[]
        try:
            with open(path,'r') as f:
                data = f.read()
            for ln in data.split('\n'):
                out.append(self.lex(ln))
            return out
        except:
            raise Exception(f'Could not find file: {path}') from None
        
    #opens chosen file, reads all data, and uses lex method    
    def lex_file(self,path):
        varhandler.direct_set_var("__name__",path)
        try:
            with open(path,'r') as f:
                data = f.read()
        except:
            raise Exception(f'Could not find file: {path}') from None
        return self.lex(data)
    def lex(self,inp):
        try:
            out=[]
            #iterate through main types and find regex, add all occurrences to list
            for k,v in self.types.items():
                for test in list(re.finditer(v,inp)) :
                    out.append(Token(test[0],k,test.start(),(test.end()-1)))
            #do same thing with the other stuff
            for k,v in self.other.items():
                for test in list(re.finditer(re.escape(v),inp)):
                    out.append(Token(test[0],k,test.start(),(test.end()-1)))
            #sort final list in order of the start position of token
            out.sort(key=lambda x: x.start)
            #use clean method to fix data
            out = self.clean(out)
            return LexedItem(out)
        except:
            raise InvalidSyntaxError('Invalid syntax while lexing.') from None
class Parser:
    def __init__(self):
        self.tokens = []
        self.current_token = None
        self.i = -1
    def raise_error(self):
        raise InvalidSyntaxError('Invalid syntax while parsing.') from None
    
    def advance(self):
        try:
                self.current_token = next(self.tokens)
                self.i +=1
        except StopIteration:
                self.current_token = None
    def peek(self):
        return self.tklist[self.i+1]
    def parse(self,tokens):
        disallowed = (TokenType.SPACE,TokenType.COMMENT,TokenType.NEWLINE,'TAB')
        self.tokens = []
        self.current_token = None
        self.i = -1
        if type(tokens) is LexedItem:
            self.tokens = tokens.filter(keep=None,remove=disallowed)
        else:
            self.tokens = LexedItem(tokens).filter(keep=None,remove=disallowed)
        self.tklist = self.tokens
        self.tokens = iter(self.tokens)
        self.advance()
        if self.current_token == None:
                return ParsedItem([])
        if len(self.tklist) == 1:
            return ParsedItem(self.tklist)
        result = self.expr()

        if self.current_token != None:
               self.raise_error()
        return ParsedItem(list(result))
    #parse the lexed tokens line by line
    def parse_lbl(self,tokens):
        out = []
        for ln in tokens:
            out.append(self.parse(ln))
        return ParsedList(out)
    def expr(self):
            if self.current_token.type == TokenType.IDENTIFIER and self.peek().type == TokenType.ASSIGN:
                var = self.current_token

                self.advance()
                if self.current_token.type == TokenType.ASSIGN:
                        assign = self.current_token
                        
                        self.advance()
                        return [(var,assign,self.term())]

                
            result = self.term()

            while self.current_token != None and self.current_token.type in (TokenType.PLUS,TokenType.MINUS):
                    if self.current_token.type == TokenType.PLUS:
                            self.advance()
                            result = (result,Token('+',TokenType.PLUS,None,None), self.term())
                    
                    elif self.current_token.type == TokenType.MINUS:
                            self.advance()
                            result = (result,Token('-',TokenType.MINUS,None,None), self.term())
            return result

    def term(self):
            result = self.factor()

            while self.current_token != None and self.current_token.type in (TokenType.MULT,TokenType.DIV):
                    if self.current_token.type == TokenType.MULT:
                            self.advance()
                            result = (result,Token('*',TokenType.MULT,None,None), self.factor())
                    elif self.current_token.type == TokenType.DIV:
                            self.advance()
                            result = (result,Token('/',TokenType.DIV,None,None), self.factor())   
            return result

    def factor(self):
            token = self.current_token

            if token.type == TokenType.LPAREN:
                    self.advance()
                    result = self.expr()

                    if self.current_token.type != TokenType.RPAREN:
                            self.raise_error()
                    
                    self.advance()
                    return result

            elif token.type in (TokenType.FLOAT,TokenType.INT,TokenType.STR,TokenType.IDENTIFIER):
                    self.advance()
                    return (token)

            elif token.type in TokenType.PLUSMINUS:
                    self.advance()
                    return (self.factor())
            
            
            self.raise_error()

