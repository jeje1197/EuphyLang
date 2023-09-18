from .exception import RuntimeException
from .astnode import *
from .datatypes import *
from .symboltable import SymbolTable


DEFAULT_BOOLEAN_VALUE = BooleanValue('false')
DEFAULT_NUMBER_VALUE  = NumberValue(0)
DEFAULT_STRING_VALUE  = StringValue('')

DEFAULT_VALUES = {
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
        
        if node.expression:
            value = self.visit(node.expression, symbol_table)
        else:
            value = DEFAULT_VALUES[node.data_type]
        symbol_table.insert(node.name, value)
    
    def visit_VariableAssignmentNode(self, node: VariableAssignmentNode, symbol_table: SymbolTable):
        table = symbol_table.find(node.name)
        if not table:
            raise RuntimeException(f'\'{node.name}\' could not be resolved at {node.position}')
        
        if node.expression:
            value = self.visit(node.expression, symbol_table)
        else:
            DEFAULT_VALUES[node.data_type]
        table.insert(node.name, value)

    def visit_VariableAccessNode(self, node: VariableAccessNode, symbol_table: SymbolTable):
        value = symbol_table.get(node.name)
        if not value:
            raise RuntimeException(f'\'{node.name}\' cannot be resolved at {node.position}')
        return value

