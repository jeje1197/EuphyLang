TOKEN_NUMBER = 'number'
TOKEN_STRING = 'string'
TOKEN_KEYWORD = 'keyword'
TOKEN_IDENTIFIER = 'identifier'
TOKEN_OPERATOR = 'operator'
TOKEN_SEPARATOR = 'separator'

class Token:
    def __init__(self, type, value=None, position=None):
        self.type = type
        self.value = value
        self.position = position
    
    def __repr__(self) -> str:
        return f'<Token type: {self.type}, value: {self.value}>'