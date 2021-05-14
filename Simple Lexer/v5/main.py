#This lexer relies on regex to work
import re, ErrorHandler
ErrorHandler.DEBUG = True
#my_vars={"a":"5"}
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
    def reconstruct(self):
        out=''
        for x in self.__list:
            out+=x.token
        return out
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
        if tk.type == 'STR':
            tkn = str(tk.token)
            tkn = tkn[1:len(tkn)-1]
            return tkn
        if tk.type == 'FLOAT':
            return float(tk.token)
        if tk.type == 'INT':
            return int(tk.token)
    def calc(self,tk1,tk2,method,allowed,typ):

        if method in allowed:
            if method == 'MINUS':
                return Token(tk1 - tk2,typ,0,0)
            elif method == 'PLUS':
                return Token(tk1 + tk2,typ,0,0)
            elif method == 'MULT':
                return Token(tk1 * tk2,typ,0,0)
            elif method == 'DIV':
                return Token(tk1 / tk2,typ,0,0)
                
        raise Exception(f"Method not allowed with type {typ}.")
    def tk_type(self,tk):
        if type(tk) is int:
            return 'INT'
        if type(tk) is float:
            return 'FLOAT'
        if type(tk) is str:
            return 'STR'
    def get_vars(self,tpl):
        global my_vars
        rettpl=[]
        
        if tpl[0].type == 'IDENTIFIER':
            try:
                var = my_vars[tpl[0].token]
            except:
                raise Exception(f"Undefined var {tpl[0].token}")
            rettpl.append(Token(var,self.tk_type(self.convert_tktype(Lexer().lex(var).as_raw()[0])),0,0))
        else:
            rettpl.append(tpl[0])
        rettpl.append(tpl[1])
        if tpl[2].type == 'IDENTIFIER':
            try:
                var = my_vars[tpl[2].token]
            except:
                raise Exception(f"Undefined var {tpl[2].token}")
            rettpl.append(Token(var,self.tk_type(self.convert_tktype(Lexer().lex(var).as_raw()[0])),0,0))
        else:
            rettpl.append(tpl[2])
        return tuple(rettpl)
    def convert_tktypes(self,tpl):
        tpl = self.get_vars(tpl)
        token1=tpl[0]
        method=tpl[1]
        token2=tpl[2]
        
        if token1.type == 'STR' and token2.type == 'STR':
            return self.calc(self.convert_tktype(token1),self.convert_tktype(token2),method.type,['PLUS'],'STR')
        elif (token1.type == 'STR' and token2.type == 'INT') or (token1.type == 'INT' and token2.type == 'STR'):
            return self.calc(self.convert_tktype(token1),self.convert_tktype(token2),method.type,['MULT'],'STR')
        elif token1.type == 'FLOAT' or token2.type == 'FLOAT':
            return self.calc(self.convert_tktype(token1),self.convert_tktype(token2),method.type,['PLUS','MULT','DIV','MINUS'],'FLOAT')
        elif token1.type == 'INT' and token2.type == 'INT':
            return self.calc(int(token1.token),int(token2.token),method.type,['PLUS','MULT','DIV','MINUS'],'INT')
        msg = ''.join([str(x.as_tuple()) for x in tpl])
        raise Exception(f"Unsupported type in {msg}.")

    def solve_tlayers(self,b):
        conttuples = False
        a=[]
        for layer in b:
            if type(layer) is tuple:
                conttuples = True
                a.append(self.solve_tlayers(layer))
            else:
                a.append(layer)
        return self.convert_tktypes(a)

    #calculates the values, a bit broken at the moment though
    def calculate(self):
        out=[]
        for c in self.__list:
            if type(c) is tuple:
                out.append(self.solve_tlayers(c))
            else:
                out.append(c)
        out = self.solve_tlayers(out)
            
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

    #You can display the output as a list of token objects, or have them formatted nicely
    def as_raw(self):
        return self.__list
    def as_dict(self):
        return self.unpack(Token.as_dict)
    
    def as_list(self):
        return self.unpack(Token.as_list)
    def as_tuple(self):
        return self.unpack(Token.as_tuple)
    
class Lexer:
    def __init__(self,types=None,other=None):
        if types:
            self.types = types
        else:
            #main identifiers. you could combine float&int, rename the types or even add more ones. Replace the hashtag in the comment for other denotations, such as // if needed
            self.types = {'FLOAT':r'(-\d*\.\d+|\d*\.\d+)','INT':r'(-\d+|\d+)','IDENTIFIER':r'\w+','STR':r'(\".*?\"|\'.*?\')','COMMENT':r'#.*'}
        if other:
            self.other = other
        else:
            # can add your own keywords here such as 'KW_IF':'IF'
            self.other = {'MULT':'*','DIV':'/','PLUS':'+','MINUS':'-','LPAREN':'(','RPAREN':')','SPACE':' ','NEWLINE':'\n','SEMICOLON':';','COLON':':','RCURLY':'{','LCURLY':'}',
                          'LSQUARE':'[','RSQUARE':']','COMMA':',','ASSIGN':'=','LTE':'<=','GTE':'>=','LT':'<','GT':'>','EQ':'==','FULLSTOP':'.','EXCLAIM':'!'}
    def sort_lexed(self,e):
        return e.start
    def clean(self,out):
        tmp=[out[0]]
        for i in range(1,len(out)):
            if out[i].start > tmp[len(tmp)-1].end:
                tmp.append(out[i])
        return tmp
    #opens chosen file, reads all data, and uses lex method    
    def lex_file(self,path):
        try:
            with open(path,'r') as f:
                data = f.read()
        except:
            raise ErrorHandler.FileError(path)
            return None
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
            out.sort(key=self.sort_lexed)
            #use clean method to fix data
            out = self.clean(out)
            return LexedItem(out)
        except:
            raise ErrorHandler.LexerError()
class Parser:
    def __init__(self):
        self.tokens = []
        self.current_token = None
    def raise_error(self):
        raise Exception("Invalid syntax")
    
    def advance(self):
        try:
                self.current_token = next(self.tokens)
        except StopIteration:
                self.current_token = None

    def parse(self,tokens):

        if type(tokens) is LexedItem:
            tokens = tokens.as_raw()
    
        for tok in tokens:
            if tok.type not in ('SPACE'):
                self.tokens.append(tok)
        self.tokens = iter(self.tokens)
        self.advance()
        if self.current_token == None:
                return None

        result = self.expr()

        if self.current_token != None:
                self.raise_error()

        return ParsedItem(list(result))

    def expr(self):
            result = self.term()

            while self.current_token != None and self.current_token.type in ('PLUS','MINUS'):
                    if self.current_token.type == 'PLUS':
                            self.advance()
                            result = (result,Token('+','PLUS',None,None), self.term())
                    
                    elif self.current_token.type == 'MINUS':
                            self.advance()
                            result = (result,Token('-','MINUS',None,None), self.term())
                    
            return result

    def term(self):
            result = self.factor()

            while self.current_token != None and self.current_token.type in ('MULT','DIV'):
                    if self.current_token.type == 'MULT':
                            self.advance()
                            result = (result,Token('*','MULT',None,None), self.factor())
                    elif self.current_token.type == 'DIV':
                            self.advance()
                            result = (result,Token('/','DIV',None,None), self.factor())
    
                    
            return result

    def factor(self):
            token = self.current_token

            if token.type == 'LPAREN':
                    self.advance()
                    result = self.expr()

                    if self.current_token.type != 'RPAREN':
                            self.raise_error()
                    
                    self.advance()
                    return result

            elif token.type in ('FLOAT','INT','STR','IDENTIFIER'):
                    self.advance()
                    return (token)

            elif token.type in ('PLUS','MINUS'):
                    self.advance()
                    return (self.factor())
            
            
            self.raise_error()


print(Parser().parse(Lexer().lex("a = 5")).as_tuple())
