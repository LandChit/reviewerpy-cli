

class Error:
    def __init__(self, pos, error_name, details, content) -> None:
        self.pos = pos
        self.error_name = error_name
        self.details = details
        self.content = content
        
    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\n\tLine:{self.pos: 4d} | {self.content}'
        return result
    

# For  Transforming string into json file
class UnidentifiedGroup(Error):
    def __init__(self, pos, content, details) -> None:
        super().__init__(pos, __class__.__name__, details, content)
        
class ColumnNotFound(Error):
    def __init__(self, pos, content, details) -> None:
        super().__init__(pos, __class__.__name__, details, content)

        