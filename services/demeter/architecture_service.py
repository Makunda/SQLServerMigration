from typing import List

from neo4j.graph import Node

from services.demeter.abstract_demeter_service import AbstractDemeterService
from services.imaging.abstract_imaging_service import AbstractImagingService
from services.imaging.tag_service import ImagingTagService


class DemeterArchitectureService(AbstractDemeterService):
    """
    Architecture service
    """

    def __init__(self):
        """
        Initialization
        """
        super().__init__()
        self.__tag_service = ImagingTagService()

    def group_architecture(self, application: str):
        """
        Group all architecture in the application
        :param application: Name of the application
        :return:
        """
        # Get the query
        query = self.query_service.get_query("demeter", "group_architecture")

        # Execute
        self.neo4j_al.execute(query, {"application": application})

    def delete_architecture(self, application: str, architecture_node: Node):
        """
        Group all architecture in the application
        :param application: Name of the application
        :param architecture_node: Architecture node
        :return:
        """
        # Get the query
        query = self.query_service.get_query("demeter", "delete_architecture")

        # Execute
        self.neo4j_al.execute(query, {"application": application, "architectureId": architecture_node.id})

    def get_architecture_by_name(self, application: str, architecture_name: str) -> Node or List[Node] or None:
        """
        Get an architecture node by name
        :param application:  Name of the application
        :param architecture_name: Name of the architecture
        :return:
        """
        # Get the query
        query = self.query_service.get_query("architecture", "get_architecture_by_name")
        query.replace_anchors({"APPLICATION": application})

        # Execute
        return self.neo4j_al.execute(query, {"ArchiName": architecture_name})

    def flag_object_architecture(self, architecture_name:str, subset_name: str, node: Node) -> None:
        """
        Flag an object with the architecture tag
        :param architecture_name:  Name of the architecture
        :param subset_name: SubSet
        :param node: Node to flag
        :return: None
        """
        # Build the tag
        architecture_tag = "$a_{}${}".format(architecture_name, subset_name)

        # Get the query
        query = self.query_service.get_query("tags", "create_by_id")

        # Declare parameters
        parameters = {
            "tag": architecture_tag,
            "id": node.id
        }

        # Execute
        self.neo4j_al.execute(query, parameters)

    def flag_objects_architecture(self, architecture_name: str, subset_name: str, nodes: List[Node]) -> None:
        """
        Flag a list of objects
        :param architecture_name: Name of the architecture
        :param subset_name: Subset name
        :param nodes: List of nodes to flag
        :return: None
        """
        for node in nodes:
            self.flag_object_architecture(architecture_name, subset_name, node)

    def delete_architecture_if_exists(self, application: str,  architecture_name: str) -> None:
        """
        Delete the architecture view
        :param application: Name of the application
        :param architecture_name: Name of the architecture
        :return: None
        """
        # Get the architecture node
        architecture_node = self.get_architecture_by_name(application, architecture_name)

        # Delete the architecture node by id if found
        if architecture_node is None:
            return
        elif type(architecture_node) is Node:
            self.delete_architecture(application, architecture_node)
        elif type(architecture_node) is List:
            for n in architecture_node:
                self.delete_architecture(application, n)
