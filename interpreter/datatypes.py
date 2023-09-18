class Value: 
    def __init__(self) -> None:
        pass

class NoneValue(Value):
    def __init__(self) -> None:
        super().__init__()
    
    def __repr__(self) -> str:
        return f'None'

class BooleanValue(Value):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
    
    def __repr__(self) -> str:
        return f'{"true" if self.value else "false"}'

class NumberValue(Value):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
    
    def __repr__(self) -> str:
        return f'{self.value}'

class StringValue(Value):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        return self.value