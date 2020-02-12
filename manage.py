import getopt
import sys

from ICECREAM.core_manager import CommandManager


def main():
    """"using get opt to pass arguments and options from command line"""
    options, argv = getopt.getopt(sys.argv[1:], 'o:v', )
    command = CommandManager(argv)
    core = command.execute()
    return core


if __name__ == '__main__':
    main()
