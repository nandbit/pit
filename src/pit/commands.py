import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from pit.config import PIT_DIRECTORY_NAME
from pit.errors import CommandExecutionError


@dataclass
class CommandArgs(ABC):
    pass


@dataclass
class InitCommandArgs(CommandArgs):
    target: Optional[str]


@dataclass
class HashObjectCommandArgs(CommandArgs):
    target: str
    write: bool


class Command(ABC):
    def __init__(self, args: CommandArgs) -> None:
        self._args = args

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class InitCommand(Command):
    # Initialize a .pit directory
    def __init__(self, args: InitCommandArgs) -> None:
        self._args = args

    def execute(self) -> None:
        # Create a .pit directory
        pit_path = os.path.join(os.getcwd(), PIT_DIRECTORY_NAME)

        try:
            os.mkdir(pit_path)
        except FileExistsError as e:
            raise CommandExecutionError(f"Error during command execution: {e}")
        except FileNotFoundError as e:
            raise CommandExecutionError(f"Error during command execution: {e}")

        # Objects subdir
        objects_path = os.path.join(pit_path, "objects")
        try:
            os.mkdir(objects_path)
        except FileExistsError as e:
            raise CommandExecutionError(f"Error during command execution: {e}")
        except FileNotFoundError as e:
            raise CommandExecutionError(f"Error during command execution: {e}")
