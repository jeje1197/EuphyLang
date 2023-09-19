from .datatypes import Value, NoneValue, BooleanValue, NumberValue, StringValue, FunctionValue
from .container import Container

##
import webbrowser
##

def package(variable_name: str, euphy_value: Value):
    """This function packages a value into a list[symbol_name, value]"""
    container = Container('function', euphy_value)
    return [variable_name, container]

def fn_print(symbol_table):
    print(symbol_table.get('object').get_value())
    return NoneValue()

print_function = package('println', FunctionValue('println', [['dynamic', 'object']], 'none', [], True, fn_print))

def fn_type(symbol_table):
    euphy_value = symbol_table.get('object').get_value()
    return StringValue(euphy_value.type)

type_function = package('type', FunctionValue('type', [['dynamic', 'object']], 'string', [], True, fn_type))

def fn_input(symbol_table):
    user_input = input()
    return StringValue(user_input)

input_function = package('input', FunctionValue('input', [], 'string', [], True, fn_input))

def fn_exit(symbol_table):
    exit()

exit_function = package('exit', FunctionValue('exit', [], 'dynamic', [], True, fn_exit))

def fn_github(symbol_table):
    URL = 'https://github.com/jeje1197/EuphyLang'
    webbrowser.open(URL)
    return NoneValue()

github_function = package('github', FunctionValue('github', [], 'none', [], True, fn_github))

def fn_discord(symbol_table):
    URL = 'https://discord.gg/Yck2Y9zNwb'
    webbrowser.open(URL)
    return NoneValue()

discord_function = package('discord', FunctionValue('discord', [], 'none', [], True, fn_discord))

native_data = [
    print_function, type_function, input_function, exit_function, github_function, discord_function
]

