class SymbolTable:
    def __init__(self, parent=None) -> None:
        self.symbols = {}
        self.parent = parent

    def contains_locally(self, key):
        return key in self.symbols

    def find(self, key):
        table = self
        while table:
            if key in table.symbols: return table
            table = self.parent
        return None

    def insert(self, key, value):
        self.symbols[key] = value
    
    def get(self, key):
        table = self.find(key)
        if table:
            return table.symbols[key]
        return None

    def update(self, key, value):
        table = self.find(key)
        if table:
            table.symbols[key] = value
        raise Exception(f'Could not find key \'{key}\'')
    