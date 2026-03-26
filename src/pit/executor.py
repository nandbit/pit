from pit.commands import Command

from .cli import Parser


class Executor:
    def __init__(self) -> None:
        self._parser = Parser()

    def run(self) -> None:
        command: Command = self._parser.parse_command()
        command.execute()
