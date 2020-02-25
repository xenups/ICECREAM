import logging
import sys
import getopt
from ICECREAM.core_manager import CommandManager


def main():
    options, argv = getopt.getopt(sys.argv[1:], 'o:v', )
    command = CommandManager(argv)
    core = command.execute()
    return core


def wsgi_app(*args, **kwargs):
    sys.argv = ['--gunicorn']
    for k in kwargs:
        sys.argv.append("--" + k)
        sys.argv.append(kwargs[k])
    return main()


if __name__ == '__main__':
    main()
