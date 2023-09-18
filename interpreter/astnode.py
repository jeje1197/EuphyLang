class AstNode:
    def __init__(self) -> None:
        self.position = None

    def set_position(self, position):
        self.position = position
        return self

class NumberNode(AstNode):
    def __init__(self, value) -> None:
        self.value = value
    
class StringNode(AstNode):
    def __init__(self, value) -> None:
        self.value = value