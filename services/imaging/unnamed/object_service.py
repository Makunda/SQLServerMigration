from neo4j.graph import Node

from com.imaging_object import ImagingObject
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
        query = self._query_service.get_query("objects", "get_object_complexity")

        # Declare parameters
        parameters = {
            "id": node.id,
            "complexity": complexity
        }

        # Execute
        return self._neo4j_al.execute(query, parameters)

    def get_object_property(self, node: Node, object_property: str) -> str:
        """
        Get the complexity of an object in the KB
        :param node: Object to get
        :param object_property: Property to get
        :return: The Property as a string
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("objects", "get_object_property")

        # Declare parameters
        parameters = {
            "id": node.id,
            "property": object_property
        }

        # Execute
        res = self._neo4j_al.execute(query, parameters)
        if len(res) > 0:
            return res[0]
        else:
            return ""

    def object_to_imaging_object(self, node: Node) -> ImagingObject:
        """
        Convert the object to the JSON
        :param node: Node to convert
        :return: a JSON text
        """
        cyclomatic_complexity = self.get_object_complexity(node, "Cyclomatic Complexity")
        essential_complexity = self.get_object_complexity(node, "Essential Complexity")
        file_path = self.get_object_property(node, "File")

        val_cyclo = cyclomatic_complexity[0] if len(cyclomatic_complexity) >= 1 else 0
        val_essential = essential_complexity[0] if len(essential_complexity) >= 1 else 0

        return ImagingObject(
            str(node.get("Name", "")),
            str(node.get("FullName", "")),
            str(node.get("Type", "")),
            str(node.get("InternalType", "")),
            str(node.get("Level", "")),
            str(file_path),
            val_cyclo,
            val_essential
        )
