from neo4j.graph import Node


class DocumentUtils:
    """
    Static class listing the util functions for documents
    """

    @staticmethod
    def is_document(node: Node):
        return "Document" in node.labels

    @staticmethod
    def get_title(node: Node, default="") -> str:
        return node.get("Title", default)

    @staticmethod
    def get_application_label(node: Node) -> str or None:
        """
        Get the application label
        :param node: Node to process
        :return:
        """
        filtered = [x for x in node.labels if x != "Document"]
        if len(filtered) >= 1:
            return filtered[0]
        else:
            return None

    @staticmethod
    def get_description(node: Node, default="") -> str:
        return node.get("Description", default)
