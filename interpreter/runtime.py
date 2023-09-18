from .datatypes import *
from .symboltable import SymbolTable

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

