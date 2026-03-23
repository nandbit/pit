import argparse

from pit.commands import Command


class Parser:
    def __init__(self) -> None:
        self._parser = self._setup_parser()

    def parse(self) -> argparse.Namespace:
        return self._parser.parse_args()

    def _parse_command(self) -> Command:
        pass

    def _setup_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="pit",
            description="A toy implementation of a subset of git.",
        )

        return parser
