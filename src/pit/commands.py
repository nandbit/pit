import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from pit.config import PIT_DIRECTORY_NAME


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
        path = os.path.join(os.getcwd(), PIT_DIRECTORY_NAME)

        try:
            os.mkdir(path)
        except FileExistsError:
            # TODO: raise error
            pass
        except FileNotFoundError:
            # TODO: raise error
            pass
