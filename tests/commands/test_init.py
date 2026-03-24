import os

from pit.commands import InitCommand, InitCommandArgs
from pit.config import PIT_DIRECTORY_NAME


def test_init_no_target(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    args = InitCommandArgs()
    init_command = InitCommand(args)

    init_command.execute()

    assert os.path.isdir(tmp_path / PIT_DIRECTORY_NAME)
    assert os.path.isdir(tmp_path / PIT_DIRECTORY_NAME / "objects")


def test_init_target(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    args = InitCommandArgs(target="test")
    init_command = InitCommand(args)

    init_command.execute()

    assert os.path.isdir(tmp_path / "test" / PIT_DIRECTORY_NAME)
    assert os.path.isdir(tmp_path / "test" / PIT_DIRECTORY_NAME / "objects")
