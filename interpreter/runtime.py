from .exception import RuntimeException
from .astnode import *
from .datatypes import *
from .native_functions import *
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
        self.LOGS = ''

        self.should_break = False
        self.should_continue = False

    def execute(self, ast):
        global_symbol_table = SymbolTable()
        global_symbol_table.insert('println', print_function)
        for node in ast:
            self.visit(node, global_symbol_table)
        
    def visit(self, node, symbol_table):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.visit_Error)
        return method(node, symbol_table)
    
    def visit_Error(self, node, symbol_table):
        raise RuntimeError(f"Visit method for {type(node).__name__} has not been implemented yet.")
    
    def visit_UnaryOpNode(self, node: UnaryOpNode, symbol_table):
        pass

    def visit_BinaryOpNode(self, node: BinaryOpNode, symbol_table):
        pass

    def visit_NoneNode(self, node: NoneNode, symbol_table):
        return NoneValue()
    
    def visit_BooleanNode(self, node: BooleanNode, symbol_table):
        return BooleanValue(node.value)
        
    def visit_NumberNode(self, node: NumberNode, symbol_table):
        return NumberValue(node.value)
    
    def visit_StringNode(self, node: StringNode, symbol_table):
        return StringValue(node.value)
    
    def visit_PrintNode(self, node: PrintNode, symbol_table):
        value = self.visit(node.expression, symbol_table)
        print(value)
        return None
    
    def visit_CodeBlockNode(self, node: CodeBlockNode, symbol_table):
        if not node.statements: return

        new_symbol_table = SymbolTable(symbol_table)
        for statement in node.statements:
            self.visit(statement, new_symbol_table)
        return None
    
    def visit_VariableDeclarationNode(self, node: VariableDeclarationNode, symbol_table: SymbolTable):
        if symbol_table.contains_locally(node.name):
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
        return None
    
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
        return None

    def visit_VariableAccessNode(self, node: VariableAccessNode, symbol_table: SymbolTable):
        container: Container = symbol_table.get(node.name)
        if not container:
            raise RuntimeException(f'\'{node.name}\' cannot be resolved at {node.position}')
        return container.get_value()
    
    def visit_IfNode(self, node: IfNode, symbol_table: SymbolTable):
        condition_value = self.visit(node.condition, symbol_table)
        if condition_value.is_truthy():
            self.visit(node.true_statement, symbol_table)
        elif node.else_statement:
            self.visit(node.else_statement, symbol_table)
        return None
    
    def visit_WhileNode(self, node: WhileNode, symbol_table: SymbolTable):
        while self.visit(node.condition, symbol_table).is_truthy():
            self.visit(node.statement, symbol_table)
            if self.should_break: break
            if self.should_continue: continue
        return None
    
    def visit_BreakNode(self, node: BreakNode, symbol_table: SymbolTable):
        self.should_break = True
        return None

    def visit_ContinueNode(self, node: ContinueNode, symbol_table: SymbolTable):
        self.should_continue = True
        return None

    def visit_FunctionDeclarationNode(self, node: FunctionDeclarationNode, symbol_table: SymbolTable):
        if symbol_table.contains_locally(node.name):
            raise RuntimeException(f'\'{node.name}\' is already declared in scope at {node.position}')

        discovered_parameters = set()
        for i in range(len(node.parameters)):
            parameter_name = node.parameters[i][1]
            if parameter_name in discovered_parameters:
                raise RuntimeException(f'\'{parameter_name}\' is already declared in function parameters at {node.position}')
            discovered_parameters.add(parameter_name)
        
        function = FunctionValue(node.name, node.parameters, node.return_type, node.statements, False)
        container = Container('function', function)
        symbol_table.insert(node.name, container)
        return None
    
    def visit_FunctionCallNode(self, node: FunctionCallNode, symbol_table: SymbolTable):
        function = self.visit(node.node_to_call, symbol_table)
        if not isinstance(function, FunctionValue):
            raise RuntimeException(f'{function.type} is not callable {node.position}')
        
        # Check number of args
        parameter_count = len(function.parameters)
        arg_count = len(node.args)
        if parameter_count != arg_count:
            raise RuntimeException(f'Function {function.name} expected {parameter_count} args, but received {arg_count} at {node.position}')

        # Check type of args
        new_symbol_table = SymbolTable(symbol_table)
        for i in range(len(node.args)):
            parameter_type = function.parameters[i][0]
            key = function.parameters[i][1]
            value = self.visit(node.args[i], symbol_table)
            if parameter_type != 'dynamic' and parameter_type != value.type:
                raise RuntimeException(f'Function \'{function.name}\' arg {i} expects type {parameter_type}, but received type {value.type} at {node.position}')
            container = Container(parameter_type, value)
            new_symbol_table.insert(key, container)

        if function.is_native:
            return function.native_function(new_symbol_table)

        # Execute statements
        for statement in function.statements:
            self.visit(statement, new_symbol_table)
        return NoneValue()