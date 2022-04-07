from metaclass.SingletonMeta import SingletonMeta
from utils.configuration.default_configuration import DefaultConfiguration
from utils.yml.yml_folder_reader import YMLFolderReader


class PortConfiguration(metaclass=SingletonMeta):

    def __init__(self):
        self.__default_configuration = DefaultConfiguration()

    def get_websockets_port(self) -> int:
        """
        Get the port of the websocket server
        :return:
        """
        return int(self.__default_configuration.get_value("port", "websockets_port"))

    def get_rest_api_port(self) -> int:
        return int(self.__default_configuration.get_value("port", "rest_api_port"))
