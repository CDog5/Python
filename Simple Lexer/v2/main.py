#This lexer relies on regex to work
import re, ErrorHandler
ErrorHandler.DEBUG = True
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
class ParsedItem:
    def __init__(self,out):
        self.__list = out

    #calculates the values, a bit broken at the moment though
    def calculate(self):
        tmp=[]
        for r in self.__list:
            if type(r) is tuple:
                
                if r[0].type in ('FLOAT','INT'):
                    num1 = float(r[0].token)
                if r[2].type in ('FLOAT','INT'):
                    num2 = float(r[2].token)
                if r[1].type == 'PLUS':
                    tmp.append(Token(float(num1+num2),'FLOAT',r[0].start,r[0].end))
                elif r[1].type == 'MINUS':
                    tmp.append(Token(float(num1-num2),'FLOAT',r[0].start,r[0].end))
                elif r[1].type == 'DIV':
                    tmp.append(Token(float(num1/num2),'FLOAT',r[0].start,r[0].end))
                elif r[1].type == 'MULT':
                    tmp.append(Token(float(num1*num2),'FLOAT',r[0].start,r[0].end))
            else:
                tmp.append(r)
        if len(tmp) == 1:
            return tmp[0]
                
        if tmp[0].type in ('FLOAT','INT'):
            num1 = float(tmp[0].token)
        if tmp[2].type in ('FLOAT','INT'):
            num2 = float(tmp[2].token)
        
        if tmp[1].type == 'PLUS':
            return Token(float(num1+num2),'FLOAT',tmp[0].start,tmp[0].end)
        elif tmp[1].type == 'MINUS':
            return Token(float(num1-num2),'FLOAT',tmp[0].start,tmp[0].end)
        elif tmp[1].type == 'DIV':
            return Token(float(num1/num2),'FLOAT',tmp[0].start,tmp[0].end)
        elif tmp[1].type == 'MULT':
            return Token(float(num1*num2),'FLOAT',tmp[0].start,tmp[0].end)
    #You can display the output as a list of token objects, or have them formatted nicely
    def as_raw(self):
        return self.__list
    def as_dict(self):
        main=[]
        for val in self.__list:
            if type(val) is not tuple:
                if val:
                    main.append(val.as_dict())
            else:
                tmp = []
                for x in val:
                    if x:
                        tmp.append(x.as_dict())
                
                main.append(tuple(tmp))
        return main
    def as_list(self):
        main=[]
        for val in self.__list:
            if type(val) is not tuple:
                if val:
                    main.append(val.as_list())
            else:
                tmp = []
                for x in val:
                    if x:
                        tmp.append(x.as_list())
                
                main.append(tuple(tmp))
        return main
    def as_tuple(self):
        main=[]
        for val in self.__list:
            if type(val) is not tuple:
                if val:
                    main.append(val.as_tuple())
            else:
                tmp = []
                for x in val:
                    if x:
                        tmp.append(x.as_tuple())
                
                main.append(tuple(tmp))
        return main
    
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
        self.reset()

    def parse(self, tokens):
        try:
            if type(tokens) is LexedItem:
                tokens = tokens.as_raw()
            self.reset()
            for tok in tokens:
                if tok.type not in ('SPACE'):
                    self.tokens.append(tok)
            self.next_token()
            return ParsedItem(self.clean(self.expression()))
        except:
            if ErrorHandler.DEBUG:
                raise ErrorHandler.ParserError()
    def clean(self,res):
        main=[]
        for val in res:
            if type(val) is not tuple:
                if val:
                    main.append(val)
            else:
                tmp = []
                for x in val:
                    if x:
                        tmp.append(x)
                if len(tuple(tmp)) < 2:
                    main.append(val[0])
                else:
                    main.append(tuple(tmp))
        return main
    def reset(self):
        self.tokens = []
        self.index = int(-1)
        self.curtk = None

    def next_token(self):
        if self.index < len(self.tokens)-1:
            self.index += 1
            self.curtk = self.tokens[self.index]
            return self.curtk

    def bin_op(self, func, ops):
        left = func()
        op_tok = None
        right = None
        
        while self.curtk.type in ops:
            op_tok = self.curtk
            self.next_token()
            right = func()
        return (left, op_tok, right)

    def factor(self):
        tok = self.curtk
        if tok.type in ('INT', 'FLOAT'):
            self.next_token()
        return tok

    def term(self):
        return self.bin_op(self.factor, ('MULT', 'DIV'))

    def expression(self):
        return self.bin_op(self.term, ('PLUS', 'MINUS'))
