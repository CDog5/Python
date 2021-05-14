from main import Lexer, Parser, set_var
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
    #using this for now as setting vars not available in parser
    if "setvar" in a.lower():
        c = input('Name: ')
        d = input('Value: ')
        set_var(c,d)
    else:
        b = Parser().parse(Lexer().lex(a))
        print(b.calculate().token)
'''
#New func that returns formatted string
'''
while True:
    a=input("Lex:")
    b = Lexer().lex(a)
    print(b.as_strf('Value: %v Type: %t')
'''

