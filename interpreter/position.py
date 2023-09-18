class Position:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.line = 0

    def advance(self):
        self.line += 1

    def copy(self):
        position = Position(self.file_name)
        position.line = self.line
        return position
    
    def __repr__(self) -> str:
        return f' line {self.line} in {self.file_name}'