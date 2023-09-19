from .datatypes import Value, NoneValue, BooleanValue, NumberValue, StringValue, FunctionValue
from .container import Container

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

type_function = package('type', FunctionValue('type', [['dynamic', 'object']], 'none', [], True, fn_type))

native_data = [
    print_function, type_function,
]

