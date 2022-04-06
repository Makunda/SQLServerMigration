from typing import List

from neo4j.graph import Relationship

from db.neo4j.neo4j_al import Neo4jAl
from utils.configuration.default_configuration import DefaultConfiguration
from utils.configuration.graph_prop_configuration import GraphSpreadConfiguration
from utils.query.query_loader import QueryLoader


class CommunitiesAlgorithmService:
    """
    Community Algorithm service
    """

    def __init__(self):
        self.__neo4j_al = Neo4jAl()
        self.__query_service = QueryLoader()

        self.__configuration = DefaultConfiguration()
        self.__graph_configuration = GraphSpreadConfiguration()

    def launch_label_propagation(self, graph_name: str, to_write_property: str, iterations: int = 400):
        """
        Launch the label propagation on a graph and write results on property
        :param graph_name: Name of the graph
        :param to_write_property: To write property
        :param iterations: Number of iterations
        :return:
        """
        # Get the query to link an aip object
        query = self.__query_service.get_query("gds_graph", "execute_label_propagation")

        parameters = {
            "graphName": graph_name,
            "toWrite": to_write_property,
            "iterations": iterations,
            "relationshipWeightProperty": self.__graph_configuration.get_graph_spread_property()
        }

        # Execute
        self.__neo4j_al.execute(query, parameters)

