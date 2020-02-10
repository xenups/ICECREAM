from abc import abstractmethod, ABC


class BaseApp(ABC):

    @staticmethod
    @abstractmethod
    def call_router(core):
        pass
