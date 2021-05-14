from lexer import Lexer 

lexer = Lexer()
lexed = lexer.lex("2.2 + 2")
print(lexed.as_raw())
print(lexed.as_tuple())
print(lexed.as_list())
print(lexed.as_dict())
lexer = Lexer()
