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