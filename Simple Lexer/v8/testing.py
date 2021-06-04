from main import Lexer,Parser
import random
def runtests(amount=1):
    for i in range(amount):
        methods = ['*','/','+','-']
        x=random.randint(-100,100)
        m = random.choice(methods)
        y = random.randint(-100,100)
        if y == 0:
            y = 1
        test = f'{x} {m} {y}'
        print(f'Running test on {test}')
        myres = Parser().parse(Lexer().lex(test)).calculate().to_actual_type()
        actualres = eval(test)
        print(myres)
        if myres != actualres:
            raise Exception(f'Results differ, {myres} {actualres}')
runtests(100)

