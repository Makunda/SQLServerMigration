from typing import List, Any

from neo4j.graph import Node

from db.neo4j.neo4j_al import Neo4jAl
from services.imaging.abstract_imaging_service import AbstractImagingService
from utils.query.query_loader import QueryLoader


class ImagingPropertyService(AbstractImagingService):
    """
    Handle the management of property on the Imaging objects
    """

    def __init__(self):
        super(AbstractImagingService, self).__init__()

        self.neo4j_al = Neo4jAl()
        self.query_service = QueryLoader()

    def add_property(self,  node: Node, object_property: str, value: str) -> None:
        """
        Add a property on a set of node
        :param node: Node to process
        :param object_property: Name of the property to add
        :param value: Value of the property
        :return: None
        """
        # Get the query to link an aip object
        query = self.query_service.get_query("properties", "add_property")
        query.replace_anchors({"PROPERTY_NAME": object_property})

        params = {
            "node_id": node.id,
            "property": value
        }

        # Execute
        self.neo4j_al.execute(query, params)

    def add_property_by_types(self, application: str, type_list: List[str], object_property: str, value: str) -> None:
        """
        Add a property based on the Type of object
        :param application: Name of the application
        :param type_list: List of type to process
        :param object_property: Name of the property to add
        :param value: Value of the property
        :return: None
        """
        # Get the query to link an aip object
        query = self.query_service.get_query("properties", "add_property_by_type")
        query.replace_anchors({"PROPERTY_NAME": object_property, "APPLICATION": application})

        params = {
            "objectTypes": type_list,
            "propertyValue": value
        }

        # Execute
        self.neo4j_al.execute(query, params)

    def remove_property_with_value(self,  application: str, object_property: str, value: str) -> None:
        """
        Add a property on a set of node
        :param application: Name of the application
        :param object_property: Name of the property to add
        :param value: Value of the property
        :return: None
        """
        # Get the query to link an aip object
        query = self.query_service.get_query("properties", "clean_property_by_value")
        query.replace_anchors({"APPLICATION": application, "PROPERTY_NAME": object_property})

        params = {
            "propertyValue": value
        }

        # Execute
        self.neo4j_al.execute(query, params)