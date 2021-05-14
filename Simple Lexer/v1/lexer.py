#This lexer relies on regex to work
import re, ErrorHandler
class Token:
    def __init__(self,inp,tktype,pos,endpos):
        self.type = tktype
        self.token = inp
        self.start = pos
        self.end = endpos
        self.as_list = [self.token,self.type,self.start,self.end]
        self.as_tuple = (self.token,self.type,self.start,self.end)
        self.as_dict = {'TOKEN':self.token,'TOKEN_TYPE':self.type,'START_POS':self.start,'END_POS':self.end}
class LexedItem:
    def __init__(self,out):
        self.__list = out

    def reconstruct(self):
        out=""
        for x in self.list:
            out+=x.token
        return out
    #You can display the output as a list of token objects, or have them formatted nicely
    def as_raw(self):
        return self.__list
    def as_dict(self):
        out=[]
        for x in self.__list:
            out.append(x.as_dict)
        return out
    def as_list(self):
        out=[]
        for x in self.__list:
            out.append(x.as_list)
        return out
    def as_tuple(self):
        out=[]
        for x in self.__list:
            out.append(x.as_tuple)
        return out
class Lexer:
    def __init__(self,types=None,other=None):
        if types:
            self.types = types
        else:
            #main identifiers. you could combine float&int, rename the types or even add more ones
            self.types = {'FLOAT':r'(\d*\.\d+)','INT':r'\d+','IDENTIFIER':r'\w+','STR':r'\".{3,}\"|\'.{3,}\''}
        if other:
            self.other = other
        else:
            # can add your own keywords here such as 'KW_IF':'IF'
            self.other = {'MULT':"*",'DIV':'/','PLUS':'+','MINUS':'-',
                          'LPAREN':'(','RPAREN':')','SPACE':' ','NEWLINE':'\n',
                          'SEMICOLON':';','COLON':':','RCURLY':'{','LCURLY':'}',
                          'LSQUARE':'[','RSQUARE':'[','COMMA':',','ASSIGN':'=','EQ':'==','FSTOP':'.','EXCLAIM':'!'}
    def sort_lexed(self,e):
        return e.start
    def clean(self,out):
        #janky code, slow but works. will improve later
        #ensures that no other types are detected inside a string
        for j in range(len(out)):
            i = 0
            prev = None
            for x in out:
                if prev:
                    if x.start <= prev.end:
                        del out[i]
                        prev = None
                    else:
                        prev = x
                else:
                    prev = x
                i+=1
        return out
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

