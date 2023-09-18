class Exception(BaseException):
    def __init__(self, message) -> None:
        self.message = message
    
    def __repr__(self) -> str:
        return self.message
    
class ParseException(Exception):
    def __init__(self, message) -> None:
        super().__init__(f'Parsing Exception: {message}')

class RuntimeException(Exception):
    def __init__(self, message) -> None:
        super().__init__(f'Runtime Exception: {message}')