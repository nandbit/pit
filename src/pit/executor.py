from pit.commands import Command
from pit.errors import CommandExecutionError

from .cli import Parser


class Executor:
    def __init__(self) -> None:
        self._parser = Parser()

    def run(self) -> None:
        command: Command = self._parser.parse_command()
        try:
            command.execute()
        except CommandExecutionError as e:
            print(f"Error executing the command: {e}")
