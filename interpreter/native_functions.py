from .datatypes import FunctionValue
from .container import Container

def package(euphy_value):
    container = Container('function', euphy_value)
    return container

def fn_print(symbol_table):
    print(symbol_table.get('object').get_value())

print_function = package(FunctionValue('print', [['dynamic', 'object']], 'none', [], True, fn_print))