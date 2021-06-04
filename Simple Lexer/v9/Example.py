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

#reads from file and prints line by line results
'''
a=Lexer().lex_lbl('example.txt')
b = Parser().parse_lbl(a)
print(b.ln_res())
'''
#calculator using lexer and parser

while True:
    userinput = input("Calc:")
    parseres = Parser().parse(Lexer().lex(userinput))
    calcres = parseres.calculate()
    if calcres.type != 'RES_SETVAR':
        print(calcres.token)

#Func that returns formatted string
'''
while True:
    a=input("Lex:")
    b = Lexer().lex(a)
    print(b.as_strf('Value: %v Type: %t Pos: (%s,%e)'))
'''
