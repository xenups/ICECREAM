from abc import ABC, abstractmethod

from bottle import Bottle, run

from manager.baseapp import BaseApp


def execute_from_command_line(argv):
    try:
        _address = {'host': '127.0.0.1', 'port': '8000'}
        if argv.__len__() > 1:
            arg_address = argv[1].split(':')
            _address['host'] = arg_address[0]
            _address['port'] = arg_address[1]
    except Exception as e:
        raise ValueError('wrong address')
    return _address


def get_subclasses(cls):
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


class Core(object):
    def __init__(self, address):
        core = Bottle()
        self.register_routers(core)
        run(core, host=address['host'], port=address['port'])

    @staticmethod
    def register_routers(core):
        base_app_subclasses = get_subclasses(BaseApp)
        for sub_class in base_app_subclasses:
            sub_class.call_router(sub_class, core=core)
