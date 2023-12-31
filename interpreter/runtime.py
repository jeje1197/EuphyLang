from .exception import RuntimeException
from .astnode import *
from .datatypes import *
from .native_functions import *
from .symboltable import SymbolTable
from .container import Container


DEFAULT_DYNAMIC_VALUE = NoneValue()
DEFAULT_NONE_VALUE = NoneValue()
DEFAULT_BOOLEAN_VALUE = BooleanValue('false')
DEFAULT_NUMBER_VALUE  = NumberValue(0)
DEFAULT_STRING_VALUE  = StringValue('')

DEFAULT_VALUES = {
    'dynamic': DEFAULT_DYNAMIC_VALUE,
    'none': DEFAULT_NONE_VALUE,
    'boolean': DEFAULT_BOOLEAN_VALUE,
    'number': DEFAULT_NUMBER_VALUE,
    'string': DEFAULT_STRING_VALUE
}

class Runtime:
    def __init__(self) -> None:
        self.LOGS = ''

        self.should_break = False
        self.should_continue = False
        self.should_return = False
        self.return_value = NoneValue()

        self.cast_control_references = {}
        self.casted_value = None

    def insert_native_data(self, global_symbol_table: SymbolTable):
        for package in native_data:
            global_symbol_table.insert(package[0], package[1])

    def execute(self, ast):
        global_symbol_table = SymbolTable()
        self.insert_native_data(global_symbol_table)
        
        for node in ast:
            self.visit(node, global_symbol_table)
        
    def visit(self, node, symbol_table):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.visit_Error)
        return method(node, symbol_table)
    
    def visit_Error(self, node, symbol_table):
        raise RuntimeError(f"Visit method for {type(node).__name__} has not been implemented yet.")
    
    def visit_UnaryOpNode(self, node: UnaryOpNode, symbol_table):
        operand: Value = self.visit(node.expression, symbol_table)
        operator = node.operator
        position = node.position
        match operator:
            case '+':
                return operand
            case '-':
                return operand.op_negate(position)
            case '!':
                return operand.op_not()
            case '_':
                raise RuntimeError(f"Unary operation '{operator}' has not been implemented yet.")

    def visit_BinaryOpNode(self, node: BinaryOpNode, symbol_table):
        left_value = self.visit(node.left_node, symbol_table)
        right_value = self.visit(node.right_node, symbol_table)
        operator = node.operator
        position = node.position

        match operator:
            case '+':
                return left_value.op_add(right_value, position)
            case '-':
                return left_value.op_sub(right_value, position)
            case '*':
                return left_value.op_mul(right_value, position)
            case '/':
                return left_value.op_div(right_value, position)
            case '%':
                return left_value.op_rem(right_value, position)
            case '<':
                return left_value.op_lt(right_value, position)
            case '<=':
                return left_value.op_lte(right_value, position)
            case '>':
                return left_value.op_gt(right_value, position)
            case '>=':
                return left_value.op_gte(right_value, position)
            case '==':
                return left_value.op_ee(right_value, position)
            case '!=':
                return left_value.op_ne(right_value, position)
            case '&&':
                return left_value.op_and(right_value, position)
            case '||':
                return left_value.op_or(right_value, position)
            case '':
                raise RuntimeError(f"Binary operation '{operator}' has not been implemented yet.")


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
            if self.should_break or self.should_continue or self.should_return: break
        return None
    
    def visit_VariableDeclarationNode(self, node: VariableDeclarationNode, symbol_table: SymbolTable):
        if symbol_table.contains_locally(node.name):
            raise RuntimeException(f'\'{node.name}\' is already declared in scope at {node.position}')
        
        declared_type = node.data_type
        if node.expression:
            value = self.visit(node.expression, symbol_table)
            if declared_type != 'dynamic' and declared_type != value.type:
                if not self.process_cast(value, declared_type, symbol_table, node.position):
                    raise RuntimeException(f'\'{node.name}\' expects type {declared_type}, but received type {value.type} at {node.position}')
                value = self.get_casted_value()
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
        if declared_type != 'dynamic' and declared_type != value.type:
            if not self.process_cast(new_value, declared_type, symbol_table, node.position):
                raise RuntimeException(f'\'{node.name}\' expects type {declared_type}, but received type {value.type} at {node.position}')
            value = self.get_casted_value()
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
            if self.should_break: 
                self.should_break = False
                break
            elif self.should_continue: 
                self.should_continue = False
                continue
            elif self.should_return: break
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
        if not (isinstance(function, FunctionValue) or isinstance(function, ClassDefinition)):
            raise RuntimeException(f'{function.type} is not callable at {node.position}')
        
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
                if not self.process_cast(value, parameter_type, symbol_table, node.position):
                    raise RuntimeException(f'Function \'{function.name}\' arg {i} expects type {parameter_type}, but received type {value.type} at {node.position}')
                value = self.get_casted_value()
            container = Container(parameter_type, value)
            new_symbol_table.insert(key, container)

        if function.is_native:
            return function.native_function(new_symbol_table)

        # Execute statements
        for statement in function.statements:
            self.visit(statement, new_symbol_table)
            if self.should_return:
                return_value = self.return_value
                self.return_value = NoneValue()
                self.should_break = False
                self.should_continue = False
                self.should_return = False
                if function.return_type != 'dynamic' and function.return_type != return_value.type:
                    raise RuntimeException(f'Function \'{function.name}\' should return type {function.return_type}, but received type {return_value.type} at {node.position}')
                return return_value

        return NoneValue()
    
    def invoke_function(self, values: list, function, symbol_table: SymbolTable, position):
        # Check number of args
        parameter_count = len(function.parameters)
        arg_count = len(values)
        if parameter_count != arg_count:
            raise RuntimeException(f'Function {function.name} expected {parameter_count} args, but received {arg_count} at {position}')

        # Check type of args
        new_symbol_table = SymbolTable(symbol_table)
        for i in range(len(values)):
            parameter_type = function.parameters[i][0]
            key = function.parameters[i][1]
            if parameter_type != 'dynamic' and parameter_type != values[i].type:
                raise RuntimeException(f'Function \'{function.name}\' arg {i} expects type {parameter_type}, but received type {values[i].type} at {position}')
            container = Container(parameter_type, values[i])
            new_symbol_table.insert(key, container)

        if function.is_native:
            return function.native_function(new_symbol_table)

        # Execute statements
        for statement in function.statements:
            self.visit(statement, new_symbol_table)
            if self.should_return:
                return_value = self.return_value
                self.return_value = NoneValue()
                self.should_break = False
                self.should_continue = False
                self.should_return = False
                if function.return_type != 'dynamic' and function.return_type != return_value.type:
                    raise RuntimeException(f'Function \'{function.name}\' should return type {function.return_type}, but received type {return_value.type} at {position}')
                return return_value

        return NoneValue()

    def visit_ReturnNode(self, node: ReturnNode, symbol_table: SymbolTable):
        self.should_return = True

        if node.expression:
            self.return_value = self.visit(node.expression, symbol_table)
        else:
            self.return_value = NoneValue()
        return None
    
    def generate_cast_id(self, datatype1, datatype2):
        cast_id = f'{datatype1}->{datatype2}'
        return cast_id
    
    def visit_CastControlNode(self, node: CastControlNode, symbol_table: SymbolTable):
        cast_id = self.generate_cast_id(node.datatype1, node.datatype2)
        if node.activate:
            function = self.visit(node.expression, symbol_table)
            if not (isinstance(function, FunctionValue)):
                raise RuntimeException(f'{function.type} is not callable at {node.position}')
            function: FunctionValue
    
            if len(function.parameters) != 1:
                raise RuntimeException(f'Cast control reference should only take one argument at {node.position}')
            elif function.parameters[0][0] != node.datatype1:
                raise RuntimeException(f'Cast control reference should take a(n) {node.datatype1} at {node.position}')
            elif not function.return_type == node.datatype2:
                raise RuntimeException(f'Cast control reference should return type {node.datatype2} {node.position}')
            self.cast_control_references[cast_id] = function
        else:
            del self.cast_control_references[cast_id]
        return None
    
    def process_cast(self, value: Value, expected_type, symbol_table, position):
        cast_id = self.generate_cast_id(value.type, expected_type)
        function = self.cast_control_references.get(cast_id)
        if not function:
            return False

        self.casted_value = self.invoke_function([value], function, symbol_table, position)
        return True
    
    def get_casted_value(self):
        return self.casted_value

    
    def visit_ClassDeclarationNode(self, node: ClassDeclarationNode, symbol_table: SymbolTable):
        if symbol_table.find(node.name):
            raise RuntimeException(f'\'{node.name}\' is already declared in scope at {node.position}')
        
        class_definition = ClassDefinition(node.name, node.inheritance_list)
        field_declarations = []
        methods = SymbolTable()
        
        for declaration in node.statements:
            if not (isinstance(declaration, VariableDeclarationNode) or isinstance(declaration, FunctionDeclarationNode)):
                raise RuntimeException(f'Invalid declaration in class body at {declaration.position}')
            if isinstance(declaration, VariableDeclarationNode):
                field_declarations.append(declaration)
            else:
                declaration: FunctionDeclarationNode
                self.visit(declaration, methods)
        
        class_definition.field_declarations = field_declarations
        class_definition.methods = methods
        container = Container(node.name, class_definition)
        symbol_table.insert(node.name, container)

    def createInstance(self):
        pass


        