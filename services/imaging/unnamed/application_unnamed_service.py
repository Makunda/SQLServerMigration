from typing import List

from neo4j.graph import Node

from services.imaging.abstract_imaging_service import AbstractImagingService
from utils.logger import Logger


class ApplicationUnnamedService(AbstractImagingService):

    def __init__(self):
        """
        Initialize the application service
        """
        super(ApplicationUnnamedService, self).__init__()
        self.__logger = Logger.get_logger("Application Unnamed Service")

    def get_application_list(self) -> List[str]:
        """
        Get the list of Application name in the database
        :return: The list of application name
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("applications", "application_list")

        # Execute
        return self._neo4j_al.execute(query)

    def get_application_node(self, name: str) -> Node or None:
        """
        Get an application node by its name.
        :return: The application node, return None if not found
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("applications", "get_by_name")
        params = {
            "application_name": name
        }

        # Execute
        res = self._neo4j_al.execute(query, params)
        if len(res) >= 1:
            return res[0]
        else:
            self.__logger.warn("Failed to get the application node for application with name {}".format(name))
            return None
