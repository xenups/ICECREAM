from abc import abstractmethod, ABC


class BaseApp(ABC):
    """every new app must inherit from  BaseApp"""

    @staticmethod
    @abstractmethod
    def call_router(core):
        pass
