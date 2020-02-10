import sys
from manager.core_manager import Core

if __name__ == '__main__':
    # pass host and port address to core from commandline
    Core(args=sys.argv)
