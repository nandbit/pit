from pit.commands import HashObjectCommand, HashObjectCommandArgs


def test_hash_string():
    args = HashObjectCommandArgs("test content", stdin=True)
    command = HashObjectCommand(args)
    result = command.execute()
    correct_result = "08cf6101416f0ce0dda3c80e627f333854c4085c"

    assert result == correct_result
