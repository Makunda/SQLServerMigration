import logging
import os
from typing import Any

import yaml
from definitions import ROOT_DIR
from interfaces.query.cypher_query import CypherQuery
from metaclass.SingletonMeta import SingletonMeta
from utils.yml.yml_configuration import YMLConfiguration


class QueryLoader(metaclass=SingletonMeta):
    """
    Loads the query from the configuration file
    """

    def __init__(self):
        self.__configuration = YMLConfiguration()

    def __get_params(self, obj, params, default=None) -> Any:
        try:
            return obj[params]
        except:
            return default

    def build_query(self, raw_query) -> CypherQuery:
        """
        Build the query based on its YAML declaration
        :param raw_query: Raw query to process
        :return: CypherQuery Class
        """
        if not raw_query["query"]:
            raise KeyError("The query is malformed. Missing query")

        params = self.__get_params(raw_query, "params", [])
        anchors = self.__get_params(raw_query, "anchors", [])
        returns = self.__get_params(raw_query, "return", None)

        return CypherQuery(raw_query["query"], anchors, params, returns)

    def get_query(self, section: str, name: str) -> CypherQuery:
        """
        Get the query and return a wrapped class of it
        :param section: Name of the section containing the query
        :param name: Name of the query to extract
        :return: The CypherQuery
        """

        try:
            # Build and return the query
            query = self.__configuration.get_value(section, name)
            return self.build_query(query)
        except KeyError as e:
            logging.error("Failed to build query with name {0} in section {1}".format(name, section), e)
            raise ValueError("Failed to build query with name {0}. Check the logs".format(name))
