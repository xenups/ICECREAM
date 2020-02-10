import sys
from manager.core_manager import execute_from_command_line, Core

if __name__ == '__main__':
    address = execute_from_command_line(argv=sys.argv)
    Core(address)
