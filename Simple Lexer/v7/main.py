#This lexer relies on regex to work
import re
class Vars:
    def __init__(self):
        self.vars={"__name__":"'<stdin>'"}
        self.user_vars={}
        self.builtins = ['__name__']
    def get_var(self,name):
            if name == '__vars__':
                return self.get_uservars()
            try:
                return self.vars[name]
            except:
                raise Exception(f"Undefined var {name}") from None
    def get_uservars(self):
        out=[]
        for k,v in self.user_vars.items():
            out.append(f'{{{k}:{v}}}')
        return ', '.join(out)
    def get_builtins(self):
        return self.builtins
    def set_var(self,name,val):
        res=Parser().parse(Lexer().lex(val)).calculate().token
        self.vars[name] = res
        self.user_vars[name] = res
    def direct_set_var(self,name,val):
        self.vars[name] = val
        self.user_vars[name] = val
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
        if tk.type == 'STR':
            tkn = str(tk.token)
            tkn = tkn[1:len(tkn)-1]
            return str(tkn)
        if tk.type == 'FLOAT':
            return float(tk.token)
        if tk.type == 'INT':
            return int(tk.token)
    def operand(self,method):
        if method == 'MINUS':
            return '-'
        elif method == 'PLUS':
            return '+'
        elif method == 'MULT':
            return '*'
        elif method == 'DIV':
            return '/'
    def calc(self,tk1,tk2,method,allowed,typ):

        if method in allowed:
            if method == 'MINUS':
                return Token(tk1 - tk2,typ,0,0)
            elif method == 'PLUS':
                return Token(tk1 + tk2,typ,0,0)
            elif method == 'MULT':
                return Token(tk1 * tk2,typ,0,0)
            elif method == 'DIV':
                res = tk1 / tk2
                if res.is_integer() and typ == 'INT':
                    res = int(res)
                else:
                    res = float(res)
                    typ = 'FLOAT'
                return Token(str(res),typ,0,0)
                
        raise Exception(f"Unsupported operand {self.operand(method)} for type: {typ}") from None
    def tk_type(self,tk):
        if type(tk) is int:
            return 'INT'
        if type(tk) is float:
            return 'FLOAT'
        if type(tk) is str:
            return 'STR'
    def convert_var(self,var):
        if (var.startswith("'") or var.startswith('"')) and (var.endswith("'") or var.endswith('"')):
            return var[1:len(var)-1]
        else:
            return var
    def get_vars(self,tpl):
        rettpl=[]

        if tpl[0].type == 'IDENTIFIER' and tpl[1].type != 'ASSIGN':
            var = varhandler.get_var(tpl[0].token)
            rettpl.append(Token(var,self.tk_type(self.convert_tktype(Lexer().lex(varhandler.get_var(tpl[0].token)).as_raw()[0])),0,0))
        else:
            rettpl.append(tpl[0])
        rettpl.append(tpl[1])
        if tpl[2].type == 'IDENTIFIER' and tpl[1].type != 'ASSIGN':
            var = varhandler.get_var(tpl[2].token)
            rettpl.append(Token(var,self.tk_type(self.convert_tktype(Lexer().lex(varhandler.get_var(tpl[2].token)).as_raw()[0])),0,0))
        else:
            rettpl.append(tpl[2])
        return tuple(rettpl)
    def deconvert_tk(self,tk):
        if tk.type == 'STR':
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
        if token1.type == 'IDENTIFIER' and method.type == 'ASSIGN' and token2.type in ('IDENTIFIER','INT','FLOAT','STR'):
            if token2.type == 'IDENTIFIER':
                token2 = self.convert_var(varhandler.get_var(token2.token))
            else:
                token2 = self.deconvert_tk(token2)            
            if token1.token in varhandler.get_builtins():
                raise Exception(f'Cannot edit builtin variable {token1.token}')from None
            varhandler.set_var(token1.token,token2)
            return None
        tpl = self.get_vars(tpl)
        token1=tpl[0]
        method=tpl[1]
        token2=tpl[2]
        
        if token1.type == 'STR' and token2.type == 'STR':
            return self.calc(self.convert_tktype(token1),self.convert_tktype(token2),method.type,['PLUS'],'STR')
        elif (token1.type == 'STR' and token2.type == 'INT') or (token1.type == 'INT' and token2.type == 'STR'):
            return self.calc(self.convert_tktype(token1),self.convert_tktype(token2),method.type,['MULT'],'STR')
        elif token1.type == 'FLOAT' or token2.type == 'FLOAT' and (token1.type != 'STR' and token2.type != 'STR'):
            return self.calc(self.convert_tktype(token1),self.convert_tktype(token2),method.type,['PLUS','MULT','DIV','MINUS'],'FLOAT')
        elif token1.type == 'INT' and token2.type == 'INT':
            return self.calc(int(token1.token),int(token2.token),method.type,['PLUS','MULT','DIV','MINUS'],'INT')
        msg = ', '.join([str(x.as_tuple()) for x in tpl])
        raise Exception(f"Unsupported type in {msg}.") from None

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
            if self.__list[0].type == 'IDENTIFIER':
                return Token(self.convert_var(varhandler.get_var(self.__list[0].token)),'UNKNOWN',0,0)
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
            return Token('SET VAR','RES_SETVAR',None,None)
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
            self.types = {'FLOAT':r'(-\d*\.\d+|\d*\.\d+)','INT':r'(-\d+|\d+)','IDENTIFIER':r'\w+','STR':r'(\".*?\"|\'.*?\')','COMMENT':r'#.*'}
        if other:
            self.other = other
        else:
            # can add your own keywords here such as 'KW_IF':'IF'
            self.other = {'MULT':'*','DIV':'/','PLUS':'+','MINUS':'-','LPAREN':'(','RPAREN':')','SPACE':' ','NEWLINE':'\n','SEMICOLON':';','COLON':':','RCURLY':'{','LCURLY':'}',
                          'LSQUARE':'[','RSQUARE':']','COMMA':',','ASSIGN':'=','LTE':'<=','GTE':'>=','LT':'<','GT':'>','EQ':'==','FULLSTOP':'.','EXCLAIM':'!'}
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
            raise Exception('Invalid syntax.') from None
class Parser:
    def __init__(self):
        self.tokens = []
        self.current_token = None
        self.i = -1
    def raise_error(self):
        raise Exception('Invalid syntax.') from None
    
    def advance(self):
        try:
                self.current_token = next(self.tokens)
                self.i +=1
        except StopIteration:
                self.current_token = None
    def peek(self):
        return self.tklist[self.i+1]
    def parse(self,tokens):
        self.tokens = []
        self.current_token = None
        self.i = -1
        if type(tokens) is LexedItem:
            tokens = tokens.as_raw()
    
        for tok in tokens:
            if tok.type not in ('SPACE','COMMENT','NEWLINE','TAB'):
                self.tokens.append(tok)
        self.tklist = self.tokens
        self.tokens = iter(self.tokens)
        self.advance()
        if self.current_token == None:
                return None
        if len(tokens) == 1:
            return ParsedItem(tokens)
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
            if self.current_token.type == 'IDENTIFIER' and self.peek().type == 'ASSIGN':
                var = self.current_token

                self.advance()
                if self.current_token.type == 'ASSIGN':
                        assign = self.current_token
                        
                        self.advance()
                        return [(var,assign,self.term())]

                
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
