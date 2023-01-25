from . import convert


class Translate(convert.Translate):
    def __init__(self, path: str) -> None:
        super().__init__(path)