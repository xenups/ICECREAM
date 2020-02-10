import os
import sys
from pydoc import locate
from bottle import Bottle, run
from ICECREAM.baseapp import BaseApp
from settings import default_address, apps


def get_default_address():
    _default = default_address
    return _default
commands_list = ['startapp', 'runserver']
list_files = ['models.py', 'controller.py', 'schemas.py', 'urls.py']


class CommandManager(object):
    def __init__(self, argv):
        if argv[1] in str(commands_list):
            self.subcommand = None
            self.command = argv[1]
            if len(argv) > 2:
                self.subcommand = argv[2]

    def execute(self):
        if self.command == 'startapp':
            if self.subcommand is not None:
                self.create_app(self.subcommand)
            else:
                sys.stdout.write('ICECREAM: Need to provide app name' + '\n')
        elif self.command == 'runserver':
            Core(address=self.subcommand)

    def create_app(self, app_name):
        try:
            path = app_name
            if not os.path.exists(path):
                os.makedirs(path)
            for file in list_files:
                filename = file
                with open(os.path.join(path, filename), 'wb') as temp_file:
                    temp_file.write('"ICECREAM"'.encode())
        except IOError as err:
            raise IOError.filename


class Core(object):
    def __init__(self, address):
        core = Bottle()
        self.__register_routers(core)
        __address = self.__convert_command_to_address(address)
        run(core, host=__address['host'], port=__address['port'])

    @staticmethod
    def __convert_command_to_address(argv):
        """convert command to address"""
        try:
            _address = get_default_address()
            if argv is not None:
                arg_address = argv.split(':')
                _address['host'] = arg_address[0]
                _address['port'] = arg_address[1]
        except Exception as e:
            raise ValueError('ICECREAM: Please provide a valid address')
        return _address

    @staticmethod
    def __initialize_baseapps():
        """subclasses populate from settings route"""
        try:
            for app in apps:
                baseapp_class = locate(app)
                instance = baseapp_class()
        except Exception as exception:
            raise ValueError("undefined app")

    def __get_subclasses(self, cls):
        """all of inherited classes from base app populate"""
        for subclass in cls.__subclasses__():
            yield from self.__get_subclasses(subclass)
            yield subclass

    def __register_routers(self, core):
        """pass bottle core to subclasses"""
        self.__initialize_baseapps()
        base_app_subclasses = self.__get_subclasses(BaseApp)
        for sub_class in base_app_subclasses:
            sub_class.call_router(sub_class, core=core)
