from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.runtime import Runtime

def repl():
    welcome()
    while True:
        user_input = input('\nEuphy>').strip()

        if user_input == 'help':
            help_message()
            continue
        elif user_input == 'info':
            info_message()
            continue
        elif user_input.startswith('-r'):
            file_path = user_input[2:]
            f, file_content = None, ''
            try:
                f = open(file_path, "r")
                file_content = f.read()
            except Exception as e:
                print(f'Failed to read from file: \'{file_path}\'')
            finally:
                if f:
                    f.close()
            run(file_path, file_content)
        else:
            run('Console', user_input)

def welcome():
    message = '=== Welcome to EuphyLang v1.0 ===\n'
    message += 'Type "help" or "info" for more infomation.'
    print(message)

def help_message():
    message = """
This is the EuphyLang REPL (Read-Eval-Print-Loop).
You can type code directly into the REPL or run code from a file
using the -r flag.

Flags:
    -r [filepath]: Run module from file path
"""
    message = '\n' + message.strip()
    print(message)

def info_message():
    message = """
Euphy is a high-level, object-oriented programming language that combines static and dynamic types. It serves as a prototype to a unique system that allow
developers to focus

EuphyLang is currently open to contribution.

Creator: Joseph Evans
GitHub: https://github.com/jeje1197/EuphyLang
Discord: 
"""
    message = '\n' + message.strip()
    print(message)

def run(file_name, code):
    lexer = Lexer(file_name, code)
    tokens = []
    try:
        tokens = lexer.generate_tokens()
    except Exception as e:
        print(e)

    if not tokens: return
    # for token in tokens:
    #     print(token)

    parser = Parser(tokens)
    ast = []

    try:
        ast = parser.generate_ast()
    except Exception as e:
        print(e)

    if not ast: return
    # for node in ast:
    #     print(node)

    runtime = Runtime()
    try:
        runtime.execute(ast)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    repl()