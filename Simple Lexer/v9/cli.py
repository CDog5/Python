import sys
from main import Lexer, Parser
from utils import VERSION
##try:
##    tmp = sys.argv[1]
##except:
##    raise Exception("This program is a CLI application only. Please specify args.") from None
##my_text = " ".join(sys.argv[1:])
##l = Lexer().lex(my_text)
##parseres = Parser().parse(l)
##calcres = parseres.calculate()
##print(calcres.token,end="")

if "pythonw.exe" not in sys.executable:
    print(f"CSLang version {VERSION}.")
    while True:
        text = input(">>>")
        if text == "" or text.lower() == "exit":
            break
        l = Lexer().lex(text)
        parseres = Parser().parse(l)
        calcres = parseres.calculate()
        print(calcres.token)
else:
    raise Exception("This program is a CLI application only.") from None
