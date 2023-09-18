from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.runtime import Runtime

def repl():
    while True:
        user_input = input('Euphy>')

        if user_input:
            run('Console', user_input)

def welcome():
    message = 'Welcome to Euphy v1.0'
    message += 'Type "info" for more infomation.'
    print(message)

def run(file_name, code):
    lexer = Lexer(file_name, code)
    tokens = []
    try:
        tokens = lexer.generate_tokens()
    except Exception as e:
        print(e)

    if not tokens: return
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = []

    # try:
    ast = parser.generate_ast()
    # except Exception as e:
    #     print(e)

    if not ast: return
    for node in ast:
        print(node)

    runtime = Runtime()
    try:
        runtime.execute(ast)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    repl()