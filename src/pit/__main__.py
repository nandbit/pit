import sys

from .executor import Executor


def main() -> None:
    executor = Executor()
    executor.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
