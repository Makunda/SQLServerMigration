from typing import List

from neo4j.graph import Node

from services.imaging.abstract_imaging_service import AbstractImagingService


class TransactionService(AbstractImagingService):
    """
    Transaction service
    """

    def get_objects_not_in_transaction_by_levels(self, application: str, types: List[str]) -> List[Node]:
        """
        Get the objects not in Transaction by type
        :param application: Name of the application
        :param types: Types to include
        :return: The list of objects not in transactions with the type
        """
        query = self.query_service.get_query("transactions", "get_objects_not_in_transaction_by_level")
        query.replace_anchors({"APPLICATION": application})

        debug_query = self.neo4j_al.get_debug_query(query, {"TypesToInclude": types})

        # Execute
        return self.neo4j_al.execute(query, {"TypesToInclude": types})

    def get_objects_in_transaction_by_levels(self, application: str, types: List[str]) -> List[Node]:
        """
        Get the objects not in Transaction by type
        :param application: Name of the application
        :param types: Types to include
        :return: The list of objects in transactions with the type
        """
        query = self.query_service.get_query("transactions", "get_objects_in_transaction_by_level")
        query.replace_anchors({"APPLICATION": application})

        # Execute
        return self.neo4j_al.execute(query, {"TypesToInclude": types})
