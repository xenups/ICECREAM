import sys
import getopt
from ICECREAM.core_manager import CommandManager


def main():
    options, argv = getopt.getopt(sys.argv[1:], 'o:v', )

    command = CommandManager(argv)
    core = command.execute()
    return core


if __name__ == '__main__':
    main()
