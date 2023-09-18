class Value: 
    def __init__(self, type) -> None:
        self.type = type

class NoneValue(Value):
    def __init__(self) -> None:
        super().__init__('none')
    
    def __repr__(self) -> str:
        return f'none'

class BooleanValue(Value):
    def __init__(self, value) -> None:
        super().__init__('boolean')
        self.value = value
    
    def __repr__(self) -> str:
        return f'{"true" if self.value else "false"}'

class NumberValue(Value):
    def __init__(self, value) -> None:
        super().__init__('number')
        self.value = value
    
    def __repr__(self) -> str:
        return f'{self.value}'

class StringValue(Value):
    def __init__(self, value) -> None:
        super().__init__('string')
        self.value = value

    def __repr__(self) -> str:
        return self.value