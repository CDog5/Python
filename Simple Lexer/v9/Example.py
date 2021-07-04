from main import Lexer
import matplotlib.pyplot as plt
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
'''
parseres = Lexer().lex_file("Fizzbuzz.py")
print(parseres.as_tuple())
new = []
for res in parseres.as_tuple():
    if res[1] != "COMMENT":
        new.append(res[0])
with open("new.txt","w") as f:
    f.write("".join(new))
'''
#Func that returns formatted string
'''
while True:
    a=input("Lex:")
    b = Lexer().lex(a)
    print(b.as_strf('Value: %v Type: %t Pos: (%s,%e)'))
'''
#analyse types in code and graph it
'''
fname = r"C:\Path\To\File.txt"
lexres = Lexer().lex_file(fname)
d = {}
for token in lexres:
    d[token.type] = d.get(token.type, 0) + 1
d = {k: v for k, v in sorted(d.items(), key=lambda res: res[1],reverse=True)}
plt.tick_params(labelsize=7)

plt.bar(list(d.keys()),list(d.values()),color=["green","black"])
plt.title(fname)
plt.show()
'''
