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
    
class BooleanNode(AstNode):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = True if value == 'true' else False

    def __repr__(self) -> str:
        return f'(BooleanNode: {self.value})'

class NumberNode(AstNode):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        return f'(NumberNode: {self.value})'
    
class StringNode(AstNode):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        return f'(StringNode: {self.value})'
    
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

class PrintNode(AstNode):
    def __init__(self, expression) -> None:
        super().__init__()
        self.expression = expression

    def __repr__(self) -> str:
        return f'(PrintNode: {self.expression})'