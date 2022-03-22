from neo4j.graph import Node


class ApplicationUtils:
    """
    Static class listing the util functions for documents
    """

    @staticmethod
    def is_application(node: Node):
        return "Application" in node.labels

    @staticmethod
    def get_name(node: Node, default="") -> str:
        return node.get("Name", default)

    @staticmethod
    def get_schema_name(node: Node, default="") -> str:
        return node.get("SchemaName", default)
