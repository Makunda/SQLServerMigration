from typing import List

from neo4j.graph import Node

from interfaces.imaging.imaging_object import ImagingObject
from services.imaging.abstract_imaging_service import AbstractImagingService


class ObjectService(AbstractImagingService):
    """
    Service managing the object in cast imaging
    """

    def __init__(self):
        super(ObjectService, self).__init__()

    def get_object_complexity(self, node: Node, complexity: str):
        """
        Get the complexity of an object in the KB
        :param node: Object to get
        :param complexity: Complexity to get
        :return: The complexity
        """
        # Get the query to link an aip object
        query = self.query_service.get_query("objects", "get_object_complexity")

        # Declare parameters
        parameters = {
            "id": node.id,
            "complexity": complexity
        }

        # Execute
        return self.neo4j_al.execute(query, parameters)

    def get_object_property(self, node: Node, object_property: str, default=None) -> str:
        """
        Get the complexity of an object in the KB
        :param default: Default value to return
        :param node: Object to get
        :param object_property: Property to get
        :return: The Property as a string
        """
        # Get the query to link an aip object
        query = self.query_service.get_query("objects", "get_object_property")

        # Declare parameters
        parameters = {
            "id": node.id,
            "property": object_property
        }

        # Execute
        res = self.neo4j_al.execute(query, parameters)
        if len(res) > 0:
            return res[0]
        else:
            return default

    def get_object_number_by_type(self, application: str, object_type: str) -> int:
        """
        Get the number of Object in one application
        :param application: Name of the application
        :param object_type: Object type to query
        :return: The number of Object of this type
        """
        query = self.query_service.get_query("objects", "get_object_number")
        query.replace_anchors({"APPLICATION": application})

        # Execute
        result = self.neo4j_al.execute(query, { "type": object_type })
        if len(result) == 0:
            raise RuntimeError("Query {0} returned no results. At least one row is expected.")

        return int(result[0])

    def get_unused_object_number_by_type(self, application: str, object_type: str) -> int:
        """
        Get the number of Object not called in the application
        :param application: Name of the application
        :param object_type: Object type to query
        :return: The number of Object of this type
        """
        query = self.query_service.get_query("objects", "get_unused_object_number")
        query.replace_anchors({"APPLICATION": application})

        # Execute
        result = self.neo4j_al.execute(query, { "type": object_type })
        if len(result) == 0:
            raise RuntimeError("Query {0} returned no results. At least one row is expected.")

        return result[0]

    def get_unused_object_by_type(self, application: str, object_type: str) -> List[Node]:
        """
        Get the list of Object not called in the application
        :param application: Name of the application
        :param object_type: Object type to query
        :return: The list of Object matching these requirements
        """
        query = self.query_service.get_query("objects", "get_unused_objects_by_type")
        query.replace_anchors({"APPLICATION": application})

        # Execute
        return self.neo4j_al.execute(query, { "type": object_type })

    def object_to_imaging_object(self, node: Node) -> ImagingObject:
        """
        Convert the object to the JSON
        :param node: Node to convert
        :return: a JSON text
        """
        cyclomatic_complexity = self.get_object_complexity(node, "Cyclomatic Complexity")
        essential_complexity = self.get_object_complexity(node, "Essential Complexity")
        file_path = self.get_object_property(node, "File")
        line_of_code = int(self.get_object_property(node, "Number of code lines", 0))

        val_cyclo = cyclomatic_complexity[0] if len(cyclomatic_complexity) >= 1 else 0
        val_essential = essential_complexity[0] if len(essential_complexity) >= 1 else 0

        return ImagingObject(
            str(node.get("Name", "")),
            str(node.get("FullName", "")),
            str(node.get("Type", "")),
            str(node.get("InternalType", "")),
            str(node.get("Level", "")),
            str(file_path),
            line_of_code,
            val_cyclo,
            val_essential,
            node
        )
