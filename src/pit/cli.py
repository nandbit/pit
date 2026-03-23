import argparse

from pit.commands import Command, InitCommand, InitCommandArgs


class Parser:
    def __init__(self) -> None:
        self._parser = self._setup_parser()

    def parse_command(self) -> Command:
        args = self._parser.parse_args()
        return self._parse_command(args)

    def _parse_command(self, args: argparse.Namespace) -> Command:
        if args.command == "init":
            command_args = InitCommandArgs(args.init_dest)
            return InitCommand(command_args)

    def _setup_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="pit",
            description="A toy implementation of a subset of git.",
        )
        subparsers = parser.add_subparsers(dest="command")

        parser_init = subparsers.add_parser("init")
        parser_init.add_argument(
            dest="init_dest",
            help="Specify the name of the repository to initialize.",
            type=str,
            nargs="?",
            default=".",
            action="store",
        )

        return parser
