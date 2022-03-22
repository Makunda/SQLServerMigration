import logging
import os

import configparser
from definitions import ROOT_DIR
from metaclass.SingletonMeta import SingletonMeta


class DefaultConfiguration(metaclass=SingletonMeta):
    """
    Configuration Class reading the ini file
    """
    __config_path = os.path.join(ROOT_DIR, 'configuration/application.ini')

    def __init__(self):
        # Read configuration
        try:
            self.__config = configparser.ConfigParser()
            self.__config.read(self.__config_path)
        except Exception as e:
            logging.error("Failed to process configuration file at {0}".format(self.__config_path), e)
            raise FileNotFoundError("Failed to process file at {0}.".format(self.__config_path))

    def get_section(self, section: str):
        """
        Read and return a section of the configuration
        :param section: Name of the section to read
        :return: The section
        """
        if self.__config is None:
            raise ValueError("Configuration has not been initialized.")

        if not self.__config.has_section(section):
            raise KeyError("Section with name %s does not exist".format(section))
        return self.__config[section]

    def get_value(self, section: str, key: str, default=None) -> str:
        """
        Get the value in a specific section of the configuration
        :param default:
        :param section: Name of the section
        :param key: Name of the key
        :param default Default Value ( Returns None by default )
        :return: Value
        """
        section = self.get_section(section)

        if key not in section.keys():
            return default

        return str(section[key])
