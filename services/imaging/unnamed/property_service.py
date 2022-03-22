from typing import List, Any

from neo4j.graph import Node

from db.neo4j.neo4j_al import Neo4jAl
from services.imaging.abstract_imaging_service import AbstractImagingService
from utils.configuration.tag_configuration import TagConfiguration
from utils.query_loader import QueryLoader


class RecommendationPropertyService(AbstractImagingService):
    """
    Handle the management of property on the Imaging objects
    """

    def __init__(self):
        super(AbstractImagingService, self).__init__()

        self._neo4j_al = Neo4jAl()
        self._query_service = QueryLoader()

        self.__tag_configuration = TagConfiguration()

    def add_recommendation_property_by_id(self, node_id: int, recommendation: str):
        """
        Add a property to the object
        :param node_id: Id of the node to tag
        :param recommendation Recommendation
        :return:
        """

        # Get the query to link an aip object
        query = self._query_service.get_query("properties", "apply_property_as_list")
        query.replace_anchors({"PROPERTY_NAME": self.__tag_configuration.get_object_recommendation_property()})

        params = {
            "value": recommendation,
            "node_id": node_id
        }

        # Execute
        return self._neo4j_al.execute(query, params)

    def get_objects_with_recommendation_property(self, application: str) -> List[Node]:
        """
        Get the list of objects containing the recommendation property
        :return: The list of node
        """

        # Get the query to link an aip object

        query = self._query_service.get_query("properties", "get_objects_by_exist_property")
        query.replace_anchors({ "PROPERTY_NAME": self.__tag_configuration.get_object_recommendation_property()})
        query.replace_anchors({"APPLICATION": application})

        # Execute
        return self._neo4j_al.execute(query)

    def get_recommendation_property(self,  node_id: int) -> List[str]:
        """
        Get the value of the recommendation property for a specific object
        :return: The list of node
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("properties", "get_property")
        query.replace_anchors({"PROPERTY_NAME": self.__tag_configuration.get_object_recommendation_property()})

        params = {
            "node_id": node_id
        }

        # Execute
        return self._neo4j_al.execute(query, params)

    def get_recommendation(self, node: Node, object_property: str) -> Any or None:
        """
        Get the value of a property for a specific object
        :return: The list of node
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("properties", "get_property")
        query.replace_anchors({"PROPERTY_NAME": object_property})

        params = {
            "node_id": node.id
        }

        # Execute
        res = self._neo4j_al.execute(query, params)
        if len(res) == 0:
            return None
        else:
            return res[0]

    def add_property(self,  node: Node, object_property: str, value: str) -> None:
        """
        Add a property on a set of node
        :param node: Node to process
        :param object_property: Name of the property to add
        :param value: Value of the property
        :return: None
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("properties", "add_property")
        query.replace_anchors({"PROPERTY_NAME": object_property})

        params = {
            "node_id": node.id,
            "property": value
        }

        # Execute
        self._neo4j_al.execute(query, params)