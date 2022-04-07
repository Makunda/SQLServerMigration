from typing import List

from neo4j.graph import Node

from interfaces.imaging.imaging_transaction import ImagingTransaction
from services.imaging.abstract_imaging_service import AbstractImagingService


class TransactionService(AbstractImagingService):
    """
    Transaction services
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

        # Execute
        return self.neo4j_al.execute(query, {"TypesToInclude": types})

    def get_all_transactions(self, application: str) -> List[Node]:
        """
        Get all transactions in a particular application
        :param application: Name of the application
        :return:
        """
        query = self.query_service.get_query("transactions", "get_all_transaction")
        query.replace_anchors({"APPLICATION": application})

        # Execute
        return self.neo4j_al.execute(query)

    def get_all_transactions_with_minimum_object(self, application: str, min_size: int) -> List[Node]:
            """
            Get all transactions in a particular application
            :param application: Name of the application
            :return:
            """
            query = self.query_service.get_query("transactions", "get_all_transaction_with_min_objects")
            query.replace_anchors({"APPLICATION": application})

            # Execute
            return self.neo4j_al.execute(query, {"minSize": min_size})

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

    def get_transaction_including_objects_with_property(self, application: str, property_name: str,
                                                        property_value: any) -> List[Node]:
        """
        Get the objects not in Transaction by type
        :param application: Name of the application
        :param property_name: Name of the property on the Object
        :param property_value:  Value of the property specified
        :return: The list of objects in transactions with the type
        """
        query = self.query_service.get_query("transactions", "get_transaction_including_objects_with_property")
        query.replace_anchors({"APPLICATION": application, "PROPERTY_NAME": property_name})

        # Execute
        return self.neo4j_al.execute(query, {"property_value": property_value})

    def get_prop_value_list_in_transaction(self, node: Node, property_name: str) -> List[any]:
        """
        Get the list of property value in a specific transaction
        :param property_name: Name of the property
        :param node: Transaction node
        :return: The list of value
        """
        if node is None:
            raise RuntimeError("Cannot get the property value list of a 'None' node.")

        query = self.query_service.get_query("transactions", "get_prop_value_list_in_transaction")
        query.replace_anchors({"PROPERTY_NAME": property_name})

        # Execute
        return self.neo4j_al.execute(query, {"TransactionId": node.id})

    def get_transaction_object_count(self, node: Node) -> int:
        """
        Get the number of objects / sub objects in a transaction
        :param node Transaction node to process
        :return: The count of object in transaction
        """
        if node is None:
            raise RuntimeError("Cannot get the number of linked object of a 'None' node.")

        query = self.query_service.get_query("transactions", "get_object_count")

        # Execute
        return self.neo4j_al.execute(query, {"IdTransaction": node.id})

    def get_transaction_complexity(self, node: Node, complexity_type: str) -> int:
        """
        Get the number of objects / sub objects in a transaction
        :param complexity_type: Complexity to get ['Cyclomatic Complexity', 'Integration Complexity', 'Essential Complexity']
        :param node Transaction node to process
        :return: The count of object in transaction
        """
        if node is None:
            raise RuntimeError("Cannot get the complexity of linked object of a 'None' node.")

        query = self.query_service.get_query("transactions", "get_transaction_complexity")

        # Execute
        return self.neo4j_al.execute(query, {"TransactionId": node.id, "ToGrabComplexity": complexity_type})

    def get_transaction_starting_point(self, node: Node) -> str:
        """
        Get the entry point type of the transaction
        :param node Transaction node to process
        :return: The type of the entry point
        """
        if node is None:
            raise RuntimeError("Cannot get the starting point of a 'None' node.")

        query = self.query_service.get_query("transactions", "get_transaction_starting_point")

        # Execute
        return self.neo4j_al.execute(query, {"TransactionId": node.id})

    def get_transaction_end_points(self, node: Node) -> List[str]:
        """
        Get the end point type of the transaction
        :param node Transaction node to process
        :return: The list of endpoint type
        """
        if node is None:
            raise RuntimeError("Cannot get the starting point of a 'None' node.")

        query = self.query_service.get_query("transactions", "get_transaction_end_points")

        # Execute
        return self.neo4j_al.execute(query, {"TransactionId": node.id})

    def node_to_imaging_transaction(self, node: Node) -> ImagingTransaction:
        """
        Transform a node into a Transaction structure
        :param node: Node to transform
        :return: Node converted to an Imaging transaction
        """

        name = node.get("Name", "")
        full_name = node.get("FullName", "")

        object_number = self.get_transaction_object_count(node)

        starting_point = self.get_transaction_starting_point(node)
        end_points = self.get_transaction_end_points(node)

        cyclomatic_complexity = self.get_transaction_complexity(node, "Cyclomatic Complexity")
        integration_complexity = self.get_transaction_complexity(node, "Integration Complexity")
        essential_complexity = self.get_transaction_complexity(node, "Essential Complexity")

        return ImagingTransaction(
            name,
            full_name,
            object_number,
            starting_point,
            end_points,
            cyclomatic_complexity,
            integration_complexity,
            essential_complexity,
            node
        )
