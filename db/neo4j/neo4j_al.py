import logging
from typing import Any, List

from interfaces.query.cypher_query import CypherQuery
from logger import Logger
from metaclass.SingletonMeta import SingletonMeta
from neo4j import GraphDatabase

from utils.configuration.default_configuration import DefaultConfiguration


class Neo4jAl(metaclass=SingletonMeta):
    """
    Class handling the connection to the Neo4j Database
    """

    def __init__(self):
        """
        Initialize the database access and initialize the connection with the configuration file
        """
        super(Neo4jAl, self).__init__()
        self.__config = DefaultConfiguration()

        self.__logger = Logger.get_logger("Neo4j Access Layer")

        # Read imaging configuration
        self.__url = str(self.__config.get_value("neo4j", "bolt_url"))
        username = str(self.__config.get_value("neo4j", "username"))
        password = str(self.__config.get_value("neo4j", "password"))
        encryption = str(self.__config.get_value("neo4j", "encryption")) == 'True'

        logging.info("Connecting to Neo4j Database : {0} (Encryption: {1} )".format(self.__url, encryption))
        # Init connection
        try:
            self.__graph_database = GraphDatabase.driver(self.__url, auth=(username, password), encrypted=encryption)
        except Exception as e:
            self.__logger.error("Failed to connect to the remote Neo4j database...", e)
            raise ConnectionError("Failed to connect to {0}".format(self.__url))

    def get_url(self) -> str:
        """
        Get the URL of the server
        :return:
        """
        return self.__url

    def __query_builder(self, query: CypherQuery, params: dict):
        """
        Build the query concatenating query string and params in a callback
        :param query: Query to run
        :param params: Parameters of the query
        :return: Lambda function to be executed in a session
        """

        def callback(tx):
            results = tx.run(query.get_query(), **params)
            return results

        return lambda tx: callback(tx)

    def __get_result(self, row, values: list or str) -> Any:
        """
        Extract the results
        :param row: Row to treat
        :param values: List of values to extract
        :return:
        """
        if len(values) == 1:
            return row[values[0]]
        elif isinstance(values, str):
            return row[values]
        else:
            ret_val = []
            for val in values:
                ret_val.append(row[val])
            return ret_val

    def get_debug_query(self, query: CypherQuery, params: dict = {}) -> str:
        """
        Return the query formatted with parameters for debug purposes
        :param query: Query to format
        :param params: Parameters of the query
        :return: The formatted query as a string
        """
        s_query = query.get_query()
        for key in params.keys():
            to_replace = params[key]

            if isinstance(to_replace, list):
                to_replace = "['{}']".format("', '".join(to_replace))

            s_query = s_query.replace("${}".format(key), str(to_replace))

        return s_query

    def execute(self, query: CypherQuery, params: dict = {}) -> list or None:
        """
        Run a query on the Neo4j database
        :param query: Query to run
        :param params: Parameters of the query as a map
        :return:
        """
        # Verify the query
        query.verify_params(params)

        try:
            # Run query
            records = []
            with self.__graph_database.session() as session:
                results = list(session.run(query.get_query(), params))

                # If there is no return query, return None
                if not query.get_return_value():
                    return None

                # Get records list
                for rec in results:
                    ret_val = self.__get_result(rec, query.get_return_value())
                    records.append(ret_val)

            return records
        except Exception as e:
            self.__logger.error("Failed to run query: {}".format(self.get_debug_query(query, params)))
            raise e
