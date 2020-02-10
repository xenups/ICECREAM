import sys
from manager.core_manager import Core

if __name__ == '__main__':
    # pass host and port address to core from commandline
    # ex: python runserver 127.0.0.1:8000
    Core(args=sys.argv)
