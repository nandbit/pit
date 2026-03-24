import os

from pit.commands import HashObjectCommand, HashObjectCommandArgs


def test_hash_string():
    args = HashObjectCommandArgs("test content", stdin=True)
    command = HashObjectCommand(args)
    result = command.execute()
    correct_result = "08cf6101416f0ce0dda3c80e627f333854c4085c"

    assert result == correct_result


def test_hash_file(tmp_path):
    filepath = os.path.join(tmp_path, "test.txt")
    with open(filepath, "w") as f:
        f.write("test content")

    args = HashObjectCommandArgs(filepath, stdin=False)
    command = HashObjectCommand(args)
    result = command.execute()
    correct_result = "08cf6101416f0ce0dda3c80e627f333854c4085c"

    assert result == correct_result
