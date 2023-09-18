class Value: 
    def __init__(self) -> None:
        pass

class NumberValue(Value):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

class StringValue(Value):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value