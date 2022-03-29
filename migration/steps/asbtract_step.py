from abc import ABC, abstractmethod
from typing import List

from neo4j.graph import Node

from services.demeter.architecture_service import DemeterArchitectureService
from utils.configuration.default_configuration import DefaultConfiguration


class AbstractStep(ABC):

    def __init__(self):
        """
        Abstract class step
        """
        self.__configuration = DefaultConfiguration()
        self.__application = self.__configuration.get_value("general", "application")

        self.__architecture_service = DemeterArchitectureService()


    def get_application(self):
        """
        Get the application name
        :return:
        """
        return self.__application

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the step
        :return: The name
        """
        pass

    @abstractmethod
    def launch(self):
        pass