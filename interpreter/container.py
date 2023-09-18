class Container:
    def __init__(self, data_type: str, value) -> None:
        self.data_type = data_type
        self.value = value

    def get_data_type(self):
        return self.data_type

    def get_value(self):
        return self.value
    
    def update_value(self, value):
        self.value = value