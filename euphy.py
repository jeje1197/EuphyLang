from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.runtime import Runtime

VERSION_NUMBER = '0.0.1'

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
            file_path = user_input[2:].strip()
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
    message = f'=== Welcome to EuphyLang v{VERSION_NUMBER} ===\n'
    message += 'Type "help" or "info" for more infomation.'
    print(message)

def help_message():
    message = """
This is the EuphyLang REPL (Read-Eval-Print-Loop).
You can type code directly into the REPL or run code from a file
using the -r flag. To exit, use CTRL + C or type "exit()" in the console.

Flags:
    -r [filepath]: Run module from file path
       Examples:
            Type "-r hello_world.euphy" to run the file hello_world.euphy
            Type "-r examples/variables.euphy" to run variables.euphy in the examples folder

Report Issue: https://github.com/jeje1197/EuphyLang/issues
"""
    message = '\n' + message.strip()
    print(message)

def info_message():
    message = f"""
Euphy is a general-purpose programming language that combines 
the world of static and dynamic types. It serves as a prototype to
features such as:
    - Mixing static and dynamic types
    - Cast Behavior Definition

Creator: Joseph Evans
Version: {VERSION_NUMBER}

EuphyLang is in the development stage and open to contribution.
Whether you want to help with the project or 
just chat with the community, we'd love to have you.

Two ways to join the discord: 
    1) Run discord() from the REPL or,
    2) Click on the following link: https://discord.gg/Yck2Y9zNw

Two ways to visit the github:
    1) Run github() from the REPL or,
    2) Click on the following link: https://github.com/jeje1197/EuphyLang
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