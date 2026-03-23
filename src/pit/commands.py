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
        cwd = os.getcwd()
        base_path = cwd

        # Create the repo folder if named
        repo_name = self._args.target
        if repo_name:
            try:
                os.mkdir(repo_name)
            except FileExistsError as e:
                raise CommandExecutionError(f"Error during command execution: {e}")
            except FileNotFoundError as e:
                raise CommandExecutionError(f"Error during command execution: {e}")
            base_path = os.path.join(cwd, repo_name)
        pit_path = os.path.join(base_path, PIT_DIRECTORY_NAME)


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


class HashObjectCommand(Command):
    # SHA256 hash of contents and filename
    def __init__(self, args: HashObjectCommandArgs) -> None:
        self._args = args

    def execute(self) -> None:
        target = self._args.target
        content = extract_file_content(target)
        header = contrust_header(content_type, content)
        store = header + content

        # try:
        #     raise CommandExecutionError(f"Error during command execution: hash-object target does not exist.")

    def extract_file_content(self, target: str) -> str:
        with open(target, "r", encoding="utf-8") as f:
            return f.read()

    def construct_header(self, content: str, content_type: str = "blob") -> str:
        # Content type can be blob, tree, commit, tag
        content_len = len(content.encode("utf-8"))
        header = f"{content_type} {content_len}\0"

        return header
