from typing import Dict, List

from neo4j.graph import Node

from db.neo4j.neo4j_al import Neo4jAl
from migration.interfaces.imaging_community import ImagingCommunity
from services.imaging.object_service import ObjectService
from utils.configuration.default_configuration import DefaultConfiguration
from utils.query.query_loader import QueryLoader


class CommunityService:
    """
    Community Service
    """
    def __init__(self):
        self.__neo4j_al = Neo4jAl()
        self.__query_service = QueryLoader()

        self.__object_service = ObjectService()
        self.__configuration = DefaultConfiguration()

        self.__community_property = self.__configuration.get_value("community", "community_property")
        self.__community_object_property = self.__configuration.get_value("community", "community_object_property")

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

    def get_incoming_communities(self, application: str, object_property: str, community_value: int) -> List[Node] or None:
        """
        Get the list of incoming communities
        :param application: Name of the application
        :param object_property:  Object property to query
        :param community_value: Value of the community
        :return: The list of node from the community
        """
        # Get the query to link an aip object
        query = self.__query_service.get_query("communities", "get_incoming_communities")
        query.replace_anchors({"APPLICATION": application, "PROPERTY": object_property})

        parameters = {
            "prop_value": community_value
        }

        # Execute
        return self.__neo4j_al.execute(query, parameters)

    def get_outgoing_communities(self, application: str, object_property: str, community_value: int) -> List[Node] or None:
        """
        Get the list of incoming communities
        :param application: Name of the application
        :param object_property:  Object property to query
        :param community_value: Value of the community
        :return: The list of node from the community
        """
        # Get the query to link an aip object
        query = self.__query_service.get_query("communities", "get_outgoing_communities")
        query.replace_anchors({"APPLICATION": application, "PROPERTY": object_property})

        parameters = {
            "prop_value": community_value
        }

        # Execute
        return self.__neo4j_al.execute(query, parameters)

    def get_communities_map(self, application: str) -> Dict[int, List[Node]]:
        """
        Get the community map
        :return: A map of the communities with their associated list of nodes
        """
        query = self.__query_service.get_query("communities", "get_communities_node")
        query.replace_anchors({"APPLICATION": application, "PROPERTY": self.__community_object_property})

        community_map: Dict[int, List[Node]] = {}

        res = self.__neo4j_al.execute(query)
        for record in res:
            # Community
            community_map[record[0]] = record[1]

        return community_map

    def node_to_imaging_community(self, application: str, community_id: int, nodes: List[Node]):
        """
        Convert a node to an imaging community
        :param application: Name of the application
        :param community_id: Id of the community
        :param nodes: List of node in the community
        :return:
        """

        # Get Community
        community_type = "Community"
        object_number = len(nodes)
        transactions_list = set()

        cyclomatic_complexity = 0.0
        essential_complexity = 0.0
        integration_complexity = 0.0

        # Parse the nodes part of the community
        for n in nodes:
            cyclomatic_complexity += self.__object_service.get_object_complexity(n, "Cyclomatic Complexity")
            essential_complexity += self.__object_service.get_object_complexity(n, "Essential Complexity")
            integration_complexity += self.__object_service.get_object_complexity(n, "Integration Complexity")

            t_list = self.__object_service.get_object_transactions(n)
            transactions_list.update(t_list)

        # Get communities linked
        incoming_communities = self.get_incoming_communities(application, self.__community_object_property, community_id)
        outgoing_communities = self.get_outgoing_communities(application, self.__community_object_property, community_id)

        # Build the imaging community
        return ImagingCommunity(
            community_id,
            community_type,
            object_number,
            cyclomatic_complexity,
            essential_complexity,
            integration_complexity,
            len(transactions_list),
            incoming_communities,
            outgoing_communities
        )