import os
from abc import ABC, abstractmethod
from typing import List, Any

import yaml

from db.neo4j.neo4j_al import Neo4jAl
from definitions import ROOT_DIR
from logger import Logger
from metaclass.SingletonMeta import SingletonMeta
from utils.folder.folder_utils import FolderUtils


class YMLConfiguration(metaclass=SingletonMeta):
    """
        Loads the query from the configuration file
        """

    def get_configuration_folder(self):
        return os.path.join(ROOT_DIR, 'configuration/')

    def __init__(self):
        super().__init__()
        self.__logger = Logger.get_logger("YML Configuration")
        self.__configuration = dict()
        self.__neo4j_al = Neo4jAl()

        # List and load files
        files = self.__list_file()
        self.__logger.info("{0} .yml files were discovered.".format(len(files)))

        self.__configuration = {}
        for f in files:
            try:
                # Load the records in the file
                temp_dict = self.__load_file(f)
                if temp_dict is not None:
                    # Add the records to the configuration
                    self.__configuration.update(temp_dict)

            except Exception as e:
                self.__logger.warn("Invalid YML configuration file {0}. File will  be skipped.".format(f))

        self.__logger.info("{0} yaml sections loaded.".format(len(self.__configuration)))

    def __list_file(self) -> List[str]:
        """
            List yml files
            :return: the list of files containing queries
        """
        return FolderUtils.list_folder(self.get_configuration_folder(), True, ".yml")

    def __load_file(self, file_path: str) -> Any or None:
        """
            Process a Yml file, and return a list of query
            :param file_path: File to process
            :return: The list of query discovered
        """
        # Verify yml
        if not file_path.endswith(".yml"):
            raise FileNotFoundError("Cannot process non-yml files.")

        # open the file and get the configuration
        yml_conf: Any = None
        with open(file_path, "r") as stream:
            try:
                yml_conf = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                self.__logger.error("Failed to process yml configuration file at '{0}'.".format(file_path), e)
                return

        # If file is empty
        if yml_conf is None:
            self.__logger.error("Time file at '{0}' is empty.".format(file_path))
            return None

        return yml_conf

    def get_section(self, name: str) -> Any:
        """
        Load a section containing queries
        :param name: Name of the section
        :param content:  Content of the section
        :return:
        """

        # Verify the configuration
        if name not in self.__configuration.keys():
            raise KeyError("The section {0} does not exist in the configuration".format(name))

        return self.__configuration[name]

    def get_value(self, *path, conf=None) -> Any or None:
        """
        Load a section containing queries
        :param conf:
        :param name: Name of the section
        :return:
        """
        args_list = list(path)
        if len(args_list) <= 0:
            return None

        if conf is None:
            conf = self.__configuration

        elem = path[0]
        if len(args_list) == 1:
            return conf[elem]

        # Verify if the key is in the configuration
        if elem not in conf.keys():
            return None

        args_list.pop(0)
        return self.get_value(*args_list, conf=conf[elem])

    def get_configuration(self) -> any:
        """
        Get configuration
        :return:  T
        """
        return self.__configuration
