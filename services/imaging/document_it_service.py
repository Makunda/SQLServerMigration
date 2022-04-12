import uuid
from typing import List

from neo4j.graph import Node

from services.imaging.abstract_imaging_service import AbstractImagingService


class DocumentItUnnamedService(AbstractImagingService):
    """
    Handles the Document creation/ management in CAST Imaging
    """

    def __init__(self):
        super(DocumentItUnnamedService, self).__init__()

    def get_document_objects(self, document: Node) -> List[Node]:
        """
        Get the list of objects attached to the document
        :param document: Document node to query
        :return:
        """
        # Get the query to link an aip object
        query = self.query_service.get_query("documents", "get_objects")

        # Declare parameters
        parameters = {
            "document_id": document.id
        }

        # Execute
        return self.neo4j_al.execute(query, parameters)

    def create_document(self, application: str, title: str, description: str) -> Node:
        """
        Create a document and assign a Title and a description
        If the document already exists with same name and description it will be merged
        :param application: Name of the application
        :param title: Title of the document
        :param description:  Description of the document
        :return: The document node
        """
        # Get the query to create a document
        query = self.query_service.get_query("documents", "document_creation")
        query.replace_anchors({"APPLICATION": application})

        # Declare parameters
        parameters = {
            "title": title,
            "description": description,
            "id": str(uuid.uuid4())
        }

        # Execute
        result = self.neo4j_al.execute(query, parameters)
        if len(result) == 0:
            raise RuntimeError("Query {0} returned no results. At least one row is expected.")

        return result[0]

    def link_document_to_object(self, application: str, document: Node, object: Node):
        """
        Link a document node to the node with specified node id
        :param application: Name of the application
        :param document:  Document as a node ( see: @create_document to generate it )
        :param object: Object to link
        :return: Nothing
        """
        # Get the query to link an aip object
        query = self.query_service.get_query("documents", "document_link_to_object")
        query.replace_anchors({"APPLICATION": application})

        # Declare parameters
        parameters = {
            "document_id": document.id,
            "node_id": object.id
        }

        # Execute
        self.neo4j_al.execute(query, parameters)
