from .cli import Parser


class Executor:
    def __init__(self) -> None:
        self._parser = Parser()

    def run(self) -> None:
        args = self._parser.parse()
        print(args)
