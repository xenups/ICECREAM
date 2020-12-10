import os
import sys
import pathlib
import logging
import rootpath
import sentry_sdk
from shutil import copy
from pydoc import locate
from getpass import getpass
from sqlalchemy_searchable import sync_trigger

from .api_cache import CachePlugin
from .db_initializer import db
from .filters import SmartFiltersPlugin
from .plugin import DBInjectorPlugin
from .util import strip_path
from .wrappers import db_handler, cors
from ICECREAM.baseapp import BaseApp
from .models.query import get_or_create
from app_user.models import Person, User
from app_user.authentication import jwt_plugin
from bottle import Bottle, run, static_file, BaseTemplate
from sentry_sdk.integrations.bottle import BottleIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from app_user.schemas import user_serializer, superuser_serializer
from settings import default_address, apps, sentry_dsn, DEBUG, media_path, searches_index, redis_cache


def get_default_address():
    _default = default_address
    return _default


rootpath.append()
ICECREAM_PATH = str(pathlib.Path(__file__).resolve().parent)
commands_list = ['startapp', 'runserver', 'wsgi', 'makealembic', 'createsuperuser', 'index_search']
list_files = ['models.py', 'controller.py', 'schemas.py', 'urls.py']


class CommandsParser(object):
    def __init__(self, opt_commands):
        self.command = None
        self.subcommands = None
        self.opt_commands = opt_commands

    def get_command(self, ):
        if self.opt_commands[0] in commands_list:
            self.command = self.opt_commands[0]
            return self.command

    def get_subcommand(self, ):
        if self.opt_commands[0] in commands_list:
            self.command = self.opt_commands[0]
            self.opt_commands.remove(self.command)
            self.subcommands = []
            for command in self.opt_commands:
                self.subcommands.append(str(command))
        return self.subcommands

    def has_value(self) -> bool:
        if not self.opt_commands:
            return True
        return False

    def has_subcommand(self) -> bool:
        if not self.get_subcommand():
            return False
        return True


class CommandManager(object):

    def __init__(self, opt_commands):
        self.command = CommandsParser(opt_commands)

    def execute(self):
        if self.command.has_value():
            core = Core()
            return core.execute_wsgi()
        if self.command.get_command() == 'makealembic':
            self.init_alembic_env()
        if self.command.get_command() == "index_search":
            self.index_search()
        if self.command.get_command() == "createsuperuser":
            self.create_super_user()
        if self.command.get_command() == 'startapp':
            if self.command.has_subcommand():
                self.create_app(self.command.get_subcommand()[0])
            else:
                sys.stdout.write('ICECREAM: Need to provide an app name' + '\n')
        elif self.command.get_command() == 'runserver':
            core = Core()
            if self.command.has_subcommand():
                return core.execute_runserver(self.command.get_subcommand()[0])
            else:
                return core.execute_runserver(None)

    @staticmethod
    def create_app(app_name):
        try:
            path = app_name
            if not os.path.exists(path):
                os.makedirs(path)
            for file in list_files:
                filename = file
                with open(os.path.join(path, filename), 'wb') as temp_file:
                    temp_file.write('"ICECREAM"'.encode())
        except IOError as err:
            raise err.filename

    @staticmethod
    def init_alembic_env():
        dst = rootpath.detect() + "/alembic/"
        if os.path.exists(dst):
            src = ICECREAM_PATH + "/migration_tool/env.py"
            copy(src, dst)
        else:
            logging.info("please alembic init alembic , before makealembic")

    @db_handler
    def create_super_user(self, db_session):
        try:
            name = input("Name:")
            person = get_or_create(Person, db_session, Person.name == name)
            person.last_name = input("LastName:")
            password = getpass("Password: ")
            phone = input("Phone:")
            person.name = name
            person.email = input("Email:")
            db_session.add(person)
            user = get_or_create(User, db_session, User.phone == phone)
            user.username = input("UserName:")
            user.phone = phone
            user.set_roles(["admin"])
            user.set_password(password)
            user.person = person
            # superuser_serializer.load(user_serializer.dump(user))
            db_session.add(user)
            db_session.commit()
            result = user_serializer.dump(db_session.query(User).get(user.id))
            return result
        except Exception as e:
            print(e.args)

    @staticmethod
    def index_search():
        try:
            for _index in searches_index:
                sync_trigger(db.engine, *_index)
        except Exception:
            raise


class Core(object):
    def __init__(self, ):
        try:
            self.core = Bottle()
            BaseTemplate.defaults['get_url'] = self.core.get_url
            self.__route_homepage()
            self.__init_jwt()
            self.__route_file_server()
            self.__init_api_cache()
            self.__initialize_log()
            self.__initialize_filters()
            self.__init_cors()
            self.__init_inject_db()
            self.__initialize_sentry_log()
            self.__register_routers()
            self.__route_404_error()
            # self.__initialize_throttle()
            logging.info("ICECREAM initialized")

        except Exception as e:
            logging.error("icecream core cannot initialize")
            raise ValueError(e)

    def __route_404_error(self):
        print("nothing")

        @self.core.error(404)
        def custom_page(error):
            return "nothing"

    def __init_jwt(self):
        if jwt_plugin.auth_endpoint:
            self.core.install(jwt_plugin)
            return True
        return False

    def __init_cors(self):
        self.core.install(cors)

    def __init_inject_db(self):
        __db_plugin = DBInjectorPlugin()
        self.core.install(__db_plugin)

    def __init_api_cache(self):
        cache = CachePlugin('url_cache', 'redis', host=redis_cache['redis_host'], port=redis_cache['redis_port'],
                            password=redis_cache['redis_pass'])
        self.core.install(cache)

    def __route_homepage(self, ):
        if DEBUG:
            self.core.hook('before_request')(strip_path)
            self.core.route('/api', callback=self._serve_homepage_template)
            self.core.route('/api/icecream/static/<filepath:path>', callback=self.server_homepage_static)

    def __route_file_server(self):
        self.core.hook('before_request')(strip_path)
        self.core.route('/api/media/<filepath:path>', callback=self.__serve_static_media)

    @staticmethod
    def _serve_homepage_template():
        __homepage_file = static_file("index.html",
                                      root=ICECREAM_PATH + '/statics/templates')
        return __homepage_file

    @staticmethod
    def server_homepage_static(filepath):
        return static_file(filepath, root=ICECREAM_PATH + '/statics/images/')

    @staticmethod
    def __serve_static_media(filepath):
        return static_file(filepath, root=media_path)

    def execute_wsgi(self):
        try:
            return self.core
        except Exception:
            raise

    def execute_runserver(self, address=None):
        try:
            __address = self.__convert_command_to_address(address)
            run(self.core, host=__address['host'], port=__address['port'], server='tornado', debug=DEBUG, reloader=True)
            return self.core
        except Exception as err:
            sys.stdout.write('execute runserver has problem')
            raise err

    @staticmethod
    def __convert_command_to_address(argv):
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
    def __initialize_log():
        log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        root_logger = logging.getLogger()

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        root_logger.addHandler(console_handler)

        file_handler = logging.FileHandler(filename='icecream.log', mode='a')
        file_handler.setLevel(level=logging.ERROR)
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)
        root_logger.setLevel(level=logging.INFO)

    @staticmethod
    def __initialize_sentry_log():
        sentry_logging = LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR  # Send errors as events
        )
        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[BottleIntegration(), sentry_logging]
        )

    @staticmethod
    def __initialize_baseapps():
        try:
            for app in apps:
                baseapp_class = locate(app)
                if baseapp_class:
                    instance = baseapp_class()
        except Exception as exception:
            raise ValueError("undefined app")

    def __get_subclasses(self, cls):
        for subclass in cls.__subclasses__():
            yield from self.__get_subclasses(subclass)
            yield subclass

    def __register_routers(self):
        self.__initialize_baseapps()
        base_app_subclasses = self.__get_subclasses(BaseApp)
        for sub_class in base_app_subclasses:
            sub_class.call_router(sub_class, core=self.core)

    def __initialize_filters(self):
        self.core.install(SmartFiltersPlugin())
