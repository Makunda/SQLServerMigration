import uuid
from typing import List

from neo4j.graph import Node

from services.imaging.abstract_imaging_service import AbstractImagingService
from services.imaging.abstract_named_service import AbstractNamedImagingService
from utils.configuration.client_configuration import ClientConfiguration
from utils.configuration.tag_configuration import TagConfiguration


class DocumentItUnnamedService(AbstractImagingService):
    """
    Handles the Document creation/ management in CAST Imaging
    """

    def __init__(self):
        super(DocumentItUnnamedService, self).__init__()
        self.__tag_configuration = TagConfiguration()
        self.__client_configuration = ClientConfiguration()

    def get_document_objects(self, document: Node) -> List[Node]:
        """
        Get the list of objects attached to the document
        :param document: Document node to query
        :return:
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("documents", "get_objects")

        # Declare parameters
        parameters = {
            "document_id": document.id
        }

        # Execute
        return self._neo4j_al.execute(query, parameters)

    def get_documents_to_upload(self) -> List[Node]:
        """
        Get a list of the documents to upload. Document prefixed and not uploaded
        """

        # Get the query to link an aip object
        query = self._query_service.get_query("documents", "get_unuploaded")

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