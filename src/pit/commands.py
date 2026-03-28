import hashlib
import os
import zlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from pit.config import PIT_DIRECTORY_NAME
from pit.errors import CommandExecutionError


@dataclass
class CommandArgs(ABC):
    pass


class Command(ABC):
    def __init__(self, args: CommandArgs) -> None:
        self._args = args

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


@dataclass
class InitCommandArgs(CommandArgs):
    target: Optional[str] = None


@dataclass
class HashObjectCommandArgs(CommandArgs):
    target: str
    write: Optional[bool] = False
    stdin: Optional[bool] = False
    content_type: Optional[str] = "blob"


@dataclass
class UpdateIndexCommandArgs(CommandArgs):
    oid: str
    filepath: str
    mode: str
    add: bool
    cacheinfo: bool


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
            except (FileExistsError, FileNotFoundError) as e:
                raise CommandExecutionError(f"Error during command execution: {e}")
            base_path = os.path.join(cwd, repo_name)

        # Create the .pit directory
        pit_path = os.path.join(base_path, PIT_DIRECTORY_NAME)

        try:
            os.mkdir(pit_path)
        except (FileExistsError, FileNotFoundError) as e:
            raise CommandExecutionError(f"Error during command execution: {e}")

        # Create .pit/objects
        objects_path = os.path.join(pit_path, "objects")
        try:
            os.mkdir(objects_path)
        except (FileExistsError, FileNotFoundError) as e:
            raise CommandExecutionError(f"Error during command execution: {e}")

        # Create .pit/index
        index_path = os.path.join(pit_path, "index")
        try:
            with open(index_path, "w") as _:
                pass
        except OSError as e:
            raise CommandExecutionError(f"Error during command execution: {e}")

        print(f"Successfully initialized a pit repository at {pit_path}")


class HashObjectCommand(Command):
    def __init__(self, args: HashObjectCommandArgs) -> None:
        self._args = args

    def execute(self) -> None:
        if not self._args.target:
            return
        if self._args.stdin:
            content = self._args.target
        else:
            content = self._extract_file_content(self._args.target)

        # Create hash
        hash = self._create_hash(
            content,
            self._args.content_type,
            self._args.stdin,
        )

        if not self._args.write:
            return hash

        # Create file to write to
        objects_dir = os.path.join(PIT_DIRECTORY_NAME, "objects")
        file_dir = os.path.join(objects_dir, hash[:2])
        filepath = os.path.join(file_dir, hash[2:])

        # Create the subdirectory in objects directory
        try:
            os.mkdir(file_dir)
        except FileExistsError as e:
            raise CommandExecutionError(f"Error during command execution: {e}")
        except FileNotFoundError as e:
            raise CommandExecutionError(f"Error during command execution: {e}")

        # Compress contents and write
        compressed_content = zlib.compress(content.encode("utf-8"))

        with open(filepath, "wb") as f:
            f.write(compressed_content)

        return hash

    def _create_hash(self, content: str, content_type: str, stdin: bool) -> str:
        header = self._construct_header(content, content_type)
        store = header + content
        h = hashlib.sha1()
        h.update(bytes(store, encoding="utf-8"))

        return h.hexdigest()[:40]

    def _extract_file_content(self, target: str) -> str:
        with open(target, "r", encoding="utf-8") as f:
            return f.read()

    def _construct_header(self, content: str, content_type: str) -> str:
        # Content type can be blob, tree, commit, tag
        content_len = len(content.encode("utf-8"))
        header = f"{content_type} {content_len}\0"

        return header


class UpdateIndexCommand(Command):
    def __init__(self, args: UpdateIndexCommandArgs) -> None:
        self._args = args

    def execute(self) -> None:
        print("Updating index")
