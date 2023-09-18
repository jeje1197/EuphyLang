class Value: 
    def __init__(self, type) -> None:
        self.type = type
    
    def is_truthy(self):
        return True

class NoneValue(Value):
    def __init__(self) -> None:
        super().__init__('none')

    def is_truthy(self):
        return False

    def __repr__(self) -> str:
        return f'none'

class BooleanValue(Value):
    def __init__(self, value) -> None:
        super().__init__('boolean')
        self.value = value

    def is_truthy(self):
        return self.value
    
    def __repr__(self) -> str:
        return f'{"true" if self.value else "false"}'

class NumberValue(Value):
    def __init__(self, value) -> None:
        super().__init__('number')
        self.value = value

    def is_truthy(self):
        return bool(self.value)
    
    def __repr__(self) -> str:
        return f'{self.value}'

class StringValue(Value):
    def __init__(self, value) -> None:
        super().__init__('string')
        self.value = value

    def is_truthy(self):
        return bool(self.value)

    def __repr__(self) -> str:
        return self.value
    
class FunctionValue(Value):
    def __init__(self, name, parameters, return_type, statements, is_native) -> None:
        super().__init__('function')
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.statements = statements
        self.is_native = is_native

    def is_truthy(self):
        return True

    def __repr__(self) -> str:
        if len(self.parameters) == 0:
            return f'<function {self.name} -> {self.return_type}>'

        signature = ''
        for i in range(len(self.parameters)):
            signature += self.parameters[i][0]
        signature += f' -> {self.return_type}'
        return f'<function {self.name} {signature}>'
    
class ListValue(Value):
    def __init__(self) -> None:
        super().__init__()
        self.elements = []

    def is_truthy(self):
        return len(self.elements) != 0
    
    def __repr__(self) -> str:
        return str(self.elements)