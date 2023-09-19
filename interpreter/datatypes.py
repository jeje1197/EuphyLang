from .exception import RuntimeException

class Value: 
    def __init__(self, type) -> None:
        self.type = type

    def get_value(self):
        return self.value
    
    def is_truthy(self):
        return True
    
    def invalid_operation(self, operator, other, position):
        raise RuntimeException(f'Invalid operation \'{operator}\' on types {self.type}, {other.type} at {position}')
    
    def op_add(self, other, position):
        self.invalid_operation('+', other, position)

    def op_sub(self, other, position):
        self.invalid_operation('-', other, position)

    def op_mul(self, other, position):
        self.invalid_operation('*', other, position)

    def op_div(self, other, position):
        self.invalid_operation('/', other, position)

    def op_rem(self, other, position):
        self.invalid_operation('%', other, position)

    def op_lt(self, other, position):
        self.invalid_operation('<', other, position)

    def op_gt(self, other, position):
        self.invalid_operation('>', other, position)

    def op_lte(self, other, position):
        self.invalid_operation('<=', other, position)

    def op_gte(self, other, position):
        self.invalid_operation('>=', other, position)

    def op_ee(self, other, position):
        if self.type != other.type:
            return BooleanValue(False)
        return BooleanValue(self.get_value() == other.get_value())

    def op_ne(self, other, position):
        return BooleanValue(self.get_value() != other.get_value())

    def op_and(self, other, position):
        return BooleanValue(self.is_truthy() and other.is_truthy())

    def op_or(self, other, position):
        return BooleanValue(self.is_truthy() or other.is_truthy())


class NoneValue(Value):
    def __init__(self) -> None:
        super().__init__('none')
        self.value = None
    
    def get_value(self):
        return self.value

    def is_truthy(self):
        return False

    def __repr__(self) -> str:
        return f'none'

class BooleanValue(Value):
    def __init__(self, value) -> None:
        super().__init__('boolean')
        self.value = value

    def get_value(self):
        return self.value

    def is_truthy(self):
        return self.value
    
    def __repr__(self) -> str:
        return f'{"true" if self.value else "false"}'

class NumberValue(Value):
    def __init__(self, value) -> None:
        super().__init__('number')
        self.value = value

    def get_value(self):
        return self.value

    def is_truthy(self):
        return bool(self.value)
    
    def op_add(self, other, position):
        if isinstance(other, NumberValue):
            return NumberValue(self.value + other.value)
        self.invalid_operation('+', other, position)

    def op_sub(self, other, position):
        if isinstance(other, NumberValue):
            return NumberValue(self.value - other.value)
        self.invalid_operation('-', other, position)

    def op_mul(self, other, position):
        if isinstance(other, NumberValue):
            return NumberValue(self.value * other.value)
        self.invalid_operation('*', other, position)

    def op_div(self, other, position):
        if isinstance(other, NumberValue):
            return NumberValue(self.value / other.value)
        self.invalid_operation('/', other, position)

    def op_rem(self, other, position):
        if isinstance(other, NumberValue):
            return NumberValue(self.value % other.value)
        self.invalid_operation('%', other, position)

    def op_lt(self, other, position):
        if isinstance(other, NumberValue):
            return NumberValue(self.value < other.value)
        self.invalid_operation('<', other, position)

    def op_gt(self, other, position):
        if isinstance(other, NumberValue):
            return NumberValue(self.value > other.value)
        self.invalid_operation('>', other, position)

    def op_lte(self, other, position):
        if isinstance(other, NumberValue):
            return NumberValue(self.value <= other.value)
        self.invalid_operation('<=', other, position)

    def op_gte(self, other, position):
        if isinstance(other, NumberValue):
            return NumberValue(self.value >= other.value)
        self.invalid_operation('>=', other, position)
    
    def __repr__(self) -> str:
        return f'{self.value}'

class StringValue(Value):
    def __init__(self, value) -> None:
        super().__init__('string')
        self.value = value

    def get_value(self):
        return self.value

    def is_truthy(self):
        return bool(self.value)
    
    def op_add(self, other, position):
        if isinstance(other, StringValue):
            return StringValue(self.value + other.value)
        self.invalid_operation('+', other, position)

    def op_lt(self, other, position):
        if isinstance(other, StringValue):
            return StringValue(self.value < other.value)
        self.invalid_operation('<', other, position)

    def op_gt(self, other, position):
        if isinstance(other, StringValue):
            return StringValue(self.value > other.value)
        self.invalid_operation('>', other, position)

    def op_lte(self, other, position):
        if isinstance(other, StringValue):
            return StringValue(self.value <= other.value)
        self.invalid_operation('<=', other, position)

    def op_gte(self, other, position):
        if isinstance(other, StringValue):
            return StringValue(self.value >= other.value)
        self.invalid_operation('>=', other, position)

    def __repr__(self) -> str:
        return self.value
    
class FunctionValue(Value):
    def __init__(self, name, parameters, return_type, statements, is_native, native_function=None) -> None:
        super().__init__('function')
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.statements = statements
        self.is_native = is_native
        self.native_function = native_function

    def get_value(self):
        return self

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
    
class ClassDefinition(Value):
    def __init__(self, name, parents) -> None:
        super().__init__(name)
        self.name = name
        self.parents = parents
        self.class_attributes = {}
        self.object_fields = {}
    
    def __repr__(self) -> str:
        return f'<class \'{self.name}\'>'

class ListValue(Value):
    def __init__(self) -> None:
        super().__init__()
        self.elements = []

    def is_truthy(self):
        return len(self.elements) != 0
    
    def __repr__(self) -> str:
        return str(self.elements)