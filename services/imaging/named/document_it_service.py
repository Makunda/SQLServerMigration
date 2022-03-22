import uuid
from typing import List

from neo4j.graph import Node

from services.imaging.abstract_named_service import AbstractNamedImagingService
from utils.configuration.client_configuration import ClientConfiguration
from utils.configuration.tag_configuration import TagConfiguration


class DocumentItImagingService(AbstractNamedImagingService):
    """
    Handles the Document creation/ management in CAST Imaging
    """

    def __init__(self, application: str):
        super(DocumentItImagingService, self).__init__(application)

        self.__tag_configuration = TagConfiguration()
        self.__client_configuration = ClientConfiguration()

    def create_document(self, title: str, description: str) -> Node:
        """
        Create a document and assign a Title and a description
        If the document already exists with same name and description it will be merged
        :param title: Title of the document
        :param description:  Description of the document
        :return: The document node
        """
        # Get the query to create a document
        query = self._query_service.get_query("documents", "document_creation")
        query.replace_anchors({"APPLICATION": self._application})

        # Declare parameters
        parameters = {
            "title": title,
            "description": description,
            "id": str(uuid.uuid4())
        }

        # Execute
        result = self._neo4j_al.execute(query, parameters)
        if len(result) == 0:
            raise RuntimeError("Query {0} returned no results. At least one row is expected.")

        return result[0]

    def link_document_to_object_aip(self, document, aipId: str):
        """
        Link a document node to the node with specified node id
        :param document:  Document as a node ( see: @create_document to generate it )
        :param aipId: AIP Id of the node
        :return: Nothing
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("documents", "document_link_to_aip_object")
        query.replace_anchors({"APPLICATION": self._application})

        # Declare parameters
        parameters = {
            "document_id": document.id,
            "node_aipId": aipId
        }

        # Execute
        self._neo4j_al.execute(query, parameters)

    def link_document_to_object(self, document, node_id: int):
        """
        Link a document node to the node with specified node id
        :param node_id: Id of the node
        :param document:  Document as a node ( see: @create_document to generate it )
        :return: Nothing
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("documents", "document_link_to_object")
        query.replace_anchors({"APPLICATION": self._application})

        # Declare parameters
        parameters = {
            "document_id": document.id,
            "node_id": node_id
        }

        # Execute
        self._neo4j_al.execute(query, parameters)

    def link_document_to_object(self, document, node_id: int):
        """
        Link a document node to the node with specified node id
        :param node_id: Id of the node
        :param document:  Document as a node ( see: @create_document to generate it )
        :return: Nothing
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("documents", "document_link_to_object")
        query.replace_anchors({"APPLICATION": self._application})

        # Declare parameters
        parameters = {
            "document_id": document.id,
            "node_id": node_id
        }

        # Execute
        self._neo4j_al.execute(query, parameters)

    def get_document_objects(self, document: Node):
        """
        Get the list of objects attached to the document
        :param document: Document node to query
        :return:
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("documents", "get_objects")
        query.replace_anchors({"APPLICATION": self._application})

        # Declare parameters
        parameters = {
            "document_id": document.id
        }

        # Execute
        return self._neo4j_al.execute(query, parameters)

    def get_prefixed_documents(self) -> List[Node]:
        """
        Get the list of documents prefixed with tag in configuration
        :return:
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("documents", "get_title_starts_with")
        query.replace_anchors({"APPLICATION": self._application})

        # Declare parameters
        parameters = {
            "prefix": self.__tag_configuration.get_document_prefix()
        }

        # Execute
        return self._neo4j_al.execute(query, parameters)

    def get_unuploaded(self) -> List[Node]:
        """
        Get the list of not uploaded documents
        :return: The list of not uploaded documents
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("documents", "get_unuploaded")
        query.replace_anchors({"APPLICATION": self._application})

        params = {
            "title_prefix": self.__tag_configuration.get_document_prefix(),
            "uploaded_tag": self.__tag_configuration.get_uploaded_tag_prefix()
        }

        # Execute
        return self._neo4j_al.execute(query, params)

    def set_document_uploaded(self, document: Node):
        """
        Flag a document as uploaded
        :param document:
        :return:
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("documents", "set_uploaded")

        # Declare parameters
        parameters = {
            "document_id": document.id,
            "upload_tag": self.__tag_configuration.get_uploaded_tag_prefix(),
            "uploaded_prefix": self.__tag_configuration.get_uploaded_document_prefix(),
            "upload_prefix": self.__tag_configuration.get_document_prefix()
        }

        # Execute
        return self._neo4j_al.execute(query, parameters)

    def is_document_uploaded(self, document: Node):
        """
        Verify is a document has been uploaded or not
        :param document: Document to verify
        :return:
        """
        tag_list = document.get("Tags", [])
        return self.__tag_configuration.get_uploaded_tag_prefix() in tag_list
