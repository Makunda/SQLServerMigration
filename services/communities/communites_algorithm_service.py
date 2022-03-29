from typing import List

from neo4j.graph import Node

from db.neo4j.neo4j_al import Neo4jAl
from utils.query.query_loader import QueryLoader


class CommunitiesAlgorithmService:

    def __init__(self):
        self.__neo4j_al = Neo4jAl()
        self.__query_service = QueryLoader()

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
            "iterations": iterations
        }

        # Execute
        self.__neo4j_al.execute(query, parameters)

    def get_communities_below(self, application: str, object_property: str, communitySize: int) -> List[Node]:
        """
        Get the list of object belonging to communities under n objects
        :param application: Name of the application
        :param object_property:  Object property to query
        :param communitySize: Size of the community
        :return: The list of node from the community
        """
        # Get the query to link an aip object
        query = self.__query_service.get_query("communities", "get_communities_below")
        query.replace_anchors({"APPLICATION": application, "PROPERTY": object_property})

        parameters = {
            "communitySize": communitySize
        }

        # Execute
        return self.__neo4j_al.execute(query, parameters)

    def get_communities_above(self, application: str, object_property: str, communitySize: int) -> List[Node]:
        """
        Get the list of object belonging to communities above n objects
        :param application: Name of the application
        :param object_property:  Object property to query
        :param communitySize: Size of the community
        :return: The list of node from the community
        """
        # Get the query to link an aip object
        query = self.__query_service.get_query("communities", "get_communities_above")
        query.replace_anchors({"APPLICATION": application, "PROPERTY": object_property})

        parameters = {
            "communitySize": communitySize
        }

        # Execute
        return self.__neo4j_al.execute(query, parameters)