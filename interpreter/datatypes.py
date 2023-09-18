class Value: 
    def __init__(self) -> None:
        pass

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