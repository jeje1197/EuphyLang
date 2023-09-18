class Token:
    def __init__(self, type, value=None, position=None):
        self.type = type
        self.value = value
        self.position = position
    
    def __repr__(self) -> str:
        return f'<Token type: {self.type}, value: {self.value}>'