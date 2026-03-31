import argparse
import sys

from pit.commands import (
    Command,
    HashObjectCommandArgs,
    InitCommand,
    InitCommandArgs,
    UpdateIndexCommand,
    UpdateIndexCommandArgs,
)


class Parser:
    def __init__(self) -> None:
        self._parser = self._setup_parser()

    def parse_command(self) -> Command:
        args = self._parser.parse_args()
        return self._parse_command(args)

    def _parse_command(self, args: argparse.Namespace) -> Command:
        if args.command == "init":
            command_args = InitCommandArgs(target=args.init_dest)

            return InitCommand(command_args)
        elif args.command == "hash-object":
            if args.hash_object_stdin:
                content = sys.stdin.read()
                if not content:
                    print(
                        "Input must be provided when using the --stdin option for hash-object command."
                    )
                    sys.exit(1)
                command_args = HashObjectCommandArgs(
                    target=content,
                    write=args.hash_object_write,
                    stdin=args.hash_object_stdin,
                )
            else:
                command_args = HashObjectCommandArgs(
                    target=args.hash_object_target,
                    write=args.hash_object_write,
                    stdin=args.hash_object_stdin,
                )
        elif args.command == "update-index":
            command_args = UpdateIndexCommandArgs(
                oid=args.update_index_oid,
                filepath=args.update_index_filepath,
                mode=args.update_index_mode,
                add=args.update_index_add,
                cacheinfo=args.update_index_cacheinfo,
            )
            return UpdateIndexCommand(command_args)

    def _setup_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="pit",
            description="A toy implementation of a subset of git.",
        )
        subparsers = parser.add_subparsers(dest="command")

        self._setup_init_parser(subparsers)
        self._setup_hash_object_parser(subparsers)
        self._setup_update_index_parser(subparsers)

        return parser

    def _setup_init_parser(self, subparsers: argparse._SubParsersAction) -> None:
        init_parser = subparsers.add_parser("init")
        init_parser.add_argument(
            dest="init_dest",
            help="Specify the name of the repository to initialize.",
            type=str,
            nargs="?",
            action="store",
        )

    def _setup_hash_object_parser(self, subparsers: argparse._SubParsersAction) -> None:
        hash_object_parser = subparsers.add_parser("hash-object")
        hash_object_parser.add_argument(
            dest="hash_object_target",
            help="Content to hash.",
            type=str,
            nargs="?",
            action="store",
        )
        hash_object_parser.add_argument(
            "-w",
            "--write",
            dest="hash_object_write",
            help="Whether to write the hashed object into the objects directory.",
            action="store_true",
        )
        hash_object_parser.add_argument(
            "--stdin",
            dest="hash_object_stdin",
            help="Whether the content to be hashed comes from stdin.",
            action="store_true",
        )

    def _setup_update_index_parser(
        self, subparsers: argparse._SubParsersAction
    ) -> None:
        update_index_parser = subparsers.add_parser("update-index")

        update_index_parser.add_argument(
            dest="update_index_mode",
            help="Mode of the file added to the index.",
            type=str,
            nargs="?",
            action="store",
        )
        update_index_parser.add_argument(
            dest="update_index_oid",
            help="Object ID of the file added to the index.",
            type=str,
            nargs="?",
            action="store",
        )
        update_index_parser.add_argument(
            dest="update_index_filepath",
            help="Filepath of the file added to the index.",
            type=str,
            nargs="?",
            action="store",
        )
        update_index_parser.add_argument(
            "--add",
            dest="update_index_add",
            help="The blob hash of the file to add to the staging area.",
            action="store_true",
        )
        update_index_parser.add_argument(
            "--cacheinfo",
            dest="update_index_cacheinfo",
            help="The blob hash of the file to add to the staging area.",
            action="store_true",
        )
