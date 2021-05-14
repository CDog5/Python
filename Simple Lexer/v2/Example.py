from main import Lexer, Parser 
#shows lexer working
'''
lexer = Lexer()
lexed = lexer.lex("2.2 + 2")
print(lexed.as_raw())
print(lexed.as_tuple())
print(lexed.as_list())
print(lexed.as_dict())
'''
#calculator using lexer and parser
'''
while True:
    a=input("Calc:")
    print(Parser().parse(Lexer().lex(a)).calculate().token)
'''
while True:
    a=input("Calc:")
    print(Parser().parse(Lexer().lex(a)).calculate().token)
