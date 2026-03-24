import os

import pytest

from pit.commands import HashObjectCommand, HashObjectCommandArgs


@pytest.fixture()
def empty_objects_dir(tmp_path):
    repo = tmp_path / ".pit" / "objects"
    repo.mkdir(parents=True, exist_ok=True)

    return repo


def test_hash_string():
    args = HashObjectCommandArgs(
        target="test content",
        write=False,
        stdin=True,
        content_type="blob",
    )
    command = HashObjectCommand(args)
    result = command.execute()
    correct_result = "08cf6101416f0ce0dda3c80e627f333854c4085c"

    assert result == correct_result


def test_hash_file(tmp_path):
    filepath = os.path.join(tmp_path, "test.txt")
    with open(filepath, "w") as f:
        f.write("test content")

    args = HashObjectCommandArgs(
        target=filepath,
        write=False,
        stdin=False,
        content_type="blob",
    )
    command = HashObjectCommand(args)
    result = command.execute()
    correct_result = "08cf6101416f0ce0dda3c80e627f333854c4085c"

    assert result == correct_result


def test_hash_string_write(empty_objects_dir):
    args = HashObjectCommandArgs(
        target="test content",
        write=True,
        stdin=True,
        content_type="blob",
    )
    command = HashObjectCommand(args)
    result = command.execute()
    correct_result = "08cf6101416f0ce0dda3c80e627f333854c4085c"

    created_file_path = os.join(
        empty_objects_dir,
        "08/cf6101416f0ce0dda3c80e627f333854c4085c",
    )

    assert result == correct_result
    assert os.path.exists(created_file_path)
    assert os.path.isfile(created_file_path)
