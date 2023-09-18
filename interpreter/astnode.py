class AstNode:
    def __init__(self) -> None:
        self.position = None

    def set_position(self, position):
        self.position = position
        return self

class UnaryOpNode(AstNode):
    def __init__(self, operator: str, expression) -> None:
        super().__init__()
        self.operator = operator
        self.expression = expression

    def __repr__(self) -> str:
        return f'(UnaryOpNode: {self.operator} {self.expression})'

class BinaryOpNode(AstNode):
    def __init__(self, left_node, operator: str, right_node) -> None:
        super().__init__()
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __repr__(self) -> str:
        return f'(BinaryOpNode: {self.left_node} {self.operator} {self.right_node})'
    
class NoneNode(AstNode):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return f'(NoneNode)'
    
class BooleanNode(AstNode):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = True if value == 'true' else False

    def __repr__(self) -> str:
        return f'(BooleanNode: {self.value})'

class NumberNode(AstNode):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = float(value)

    def __repr__(self) -> str:
        return f'(NumberNode: {self.value})'
    
class StringNode(AstNode):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        return f'(StringNode: {self.value})'

class PrintNode(AstNode):
    def __init__(self, expression) -> None:
        super().__init__()
        self.expression = expression

    def __repr__(self) -> str:
        return f'(PrintNode: {self.expression})'
    
class CodeBlockNode(AstNode):
    def __init__(self, statements) -> None:
        super().__init__()
        self.statements = statements

    def __repr__(self) -> str:
        return f'(CodeBlockNode: {self.statements})'
    
class VariableDeclarationNode(AstNode):
    def __init__(self, data_type: str, name: str, expression) -> None:
        super().__init__()
        self.data_type = data_type
        self.name = name
        self.expression = expression

    def __repr__(self) -> str:
        return f'(VariableDeclarationNode: {self.data_type} {self.name} {self.expression if self.expression else ""})'
    
class VariableAssignmentNode(AstNode):
    def __init__(self, name: str, expression) -> None:
        super().__init__()
        self.name = name
        self.expression = expression

    def __repr__(self) -> str:
        return f'(VariableAssignmentNode: {self.name} {self.expression})'
    
class VariableAccessNode(AstNode):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __repr__(self) -> str:
        return f'(VariableAccessNode: {self.name})'
    
class IfNode(AstNode):
    def __init__(self, condition, true_statement, else_statement) -> None:
        super().__init__()
        self.condition = condition
        self.true_statement = true_statement
        self.else_statement = else_statement

    def __repr__(self) -> str:
        return f'(IfNode: {self.condition} then {self.true_statement} {f"else {self.else_statement}" if self.else_statement else ""})'

class WhileNode(AstNode):
    def __init__(self, condition, statement) -> None:
        super().__init__()
        self.condition = condition
        self.statement = statement

    def __repr__(self) -> str:
        return f'(WhileLoopNode: {self.condition} then {self.statement})'
    
class BreakNode(AstNode):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return f'(BreakNode)'
    
class ContinueNode(AstNode):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return f'(ContinueNode)'
    
class FunctionDeclarationNode(AstNode):
    def __init__(self, name, parameters: list[list], return_type, statements) -> None:
        super().__init__()
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.statements = statements

    def __repr__(self) -> str:
        return f'(FunctionDeclarationNode {self.return_type} {self.name} {self.parameters} {self.statements})'
    
class FunctionCallNode(AstNode):
    def __init__(self, node_to_call, args: list) -> None:
        super().__init__()
        self.node_to_call = node_to_call
        self.args = args

    def __repr__(self) -> str:
        return f'(FunctionCallNode {self.node_to_call} {self.args})'
    
class ClassDeclarationNode(AstNode):
    def __init__(self, name, inheritance_list, statements) -> None:
        super().__init__()
        self.name = name
        self.inheritance_list = inheritance_list
        self.statements = statements

    def __repr__(self) -> str:
        return f'(ClassDeclarationNode {self.name} : {self.inheritance_list})'

class ListNode(AstNode):
    def __init__(self, element_nodes) -> None:
        super().__init__()
        self.element_nodes = element_nodes

    def __repr__(self) -> str:
        return f'(ListNode {self.element_nodes})'