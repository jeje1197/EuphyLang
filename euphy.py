from interpreter.lexer import Lexer
from interpreter.parser import Parser

def repl():
    while True:
        user_input = input("Euphy>")

        if user_input:
            run('Console', user_input)

def run(file_name, code):
    lexer = Lexer(file_name, code)
    tokens = lexer.generate_tokens()

    if not tokens: return
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = parser.generate_ast()

    if not ast: return
    for node in ast:
        print(node)


if __name__ == '__main__':
    repl()