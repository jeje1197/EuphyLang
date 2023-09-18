from .exception import RuntimeException
from .astnode import *
from .datatypes import *
from .symboltable import SymbolTable
from .container import Container


DEFAULT_DYNAMIC_VALUE = NoneValue()
DEFAULT_BOOLEAN_VALUE = BooleanValue('false')
DEFAULT_NUMBER_VALUE  = NumberValue(0)
DEFAULT_STRING_VALUE  = StringValue('')

DEFAULT_VALUES = {
    'dynamic': DEFAULT_DYNAMIC_VALUE,
    'boolean': DEFAULT_BOOLEAN_VALUE,
    'number': DEFAULT_NUMBER_VALUE,
    'string': DEFAULT_STRING_VALUE
}

class Runtime:
    def __init__(self) -> None:
        pass

    def execute(self, ast):
        global_symbol_table = SymbolTable()
        for node in ast:
            self.visit(node, global_symbol_table)
        
    def visit(self, node, symbol_table):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.visit_Error)
        return method(node, symbol_table)
    
    def visit_Error(self, node, symbol_table):
        raise RuntimeError(f"Visit method for {type(node).__name__} has not been implemented yet.")
    
    def visit_UnaryOpNode(self, node, symbol_table):
        pass

    def visit_BinaryOpNode(self, node, symbol_table):
        pass

    def visit_NoneNode(self, node, symbol_table):
        return NoneValue()
    
    def visit_BooleanNode(self, node, symbol_table):
        return BooleanValue(node.value)
        
    def visit_NumberNode(self, node, symbol_table):
        return NumberValue(node.value)
    
    def visit_StringNode(self, node, symbol_table):
        return StringValue(node.value)
    
    def visit_PrintNode(self, node, symbol_table):
        value = self.visit(node.expression, symbol_table)
        print(value)
        return None
    
    def visit_VariableDeclarationNode(self, node: VariableDeclarationNode, symbol_table: SymbolTable):
        if symbol_table.find(node.name):
            raise RuntimeException(f'\'{node.name}\' is already declared in scope at {node.position}')
        
        declared_type = node.data_type
        if node.expression:
            value = self.visit(node.expression, symbol_table)
            if declared_type != 'dynamic' and declared_type != value.type:
                raise RuntimeException(f'\'{node.name}\' expects type {declared_type}, but received type {value.type} at {node.position}')
        else:
            value = DEFAULT_VALUES[node.data_type]
    
        container = Container(declared_type, value)
        symbol_table.insert(node.name, container)
    
    def visit_VariableAssignmentNode(self, node: VariableAssignmentNode, symbol_table: SymbolTable):
        table = symbol_table.find(node.name)
        if not table:
            raise RuntimeException(f'\'{node.name}\' could not be resolved at {node.position}')
        
        container: Container = table.get(node.name)
        new_value = self.visit(node.expression, symbol_table)

        declared_type = container.get_data_type()
        if declared_type != 'dynamic' and declared_type != new_value.type:
            raise RuntimeException(f'\'{node.name}\' expects type {declared_type}, but received type {new_value.type} at {node.position}')
        container.update_value(new_value)

    def visit_VariableAccessNode(self, node: VariableAccessNode, symbol_table: SymbolTable):
        container: Container = symbol_table.get(node.name)
        if not container:
            raise RuntimeException(f'\'{node.name}\' cannot be resolved at {node.position}')
        return container.get_value()
    
    

