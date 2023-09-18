from interpreter.lexer import Lexer

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


if __name__ == '__main__':
    repl()