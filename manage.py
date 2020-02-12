import sys

from ICECREAM.core_manager import CommandManager


def main():
    command = CommandManager(sys.argv)
    core = command.execute()
    return core


if __name__ == '__main__':
    main()
