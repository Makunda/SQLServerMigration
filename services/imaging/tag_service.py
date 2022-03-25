from neo4j.graph import Node

from services.imaging.abstract_imaging_service import AbstractImagingService


class ImagingTagService(AbstractImagingService):

    def __init__(self):
        super(ImagingTagService, self).__init__()

    def create_tag_by_aipId(self, application: str, aipId: str, tag: str) -> None:
        """
        Create a Tag on an object in cast Imaging
        :param application: Name of the application
        :param aipId: AIP Id of the object to tag
        :param tag: Tag to apply on the object
        :return: Void
        """
        # Get the query
        query = self.query_service.get_query("tags", "create_by_aipid")
        query.replace_anchors({"APPLICATION": application})

        # Declare parameters
        parameters = {
            "tag": tag,
            "aipId": aipId
        }

        # Execute
        self.neo4j_al.execute(query, parameters)

    def create_tag(self, node: Node, tag: str) -> None:
        """
        Create a Tag on an object in cast Imaging
        :param node: Node
        :param tag: Tag to apply on the object
        :return: Void
        """
        self.create_tag_by_id(node.id, tag)

    def create_tag_by_id(self, id: int, tag: str) -> None:
        """
        Create a Tag on an object in cast Imaging
        :param id: Id of the object to tag
        :param tag: Tag to apply on the object
        :return: Void
        """
        # Get the query
        query = self.query_service.get_query("tags", "create_by_id")

        # Declare parameters
        parameters = {
            "tag": tag,
            "id": id
        }

        # Execute
        self.neo4j_al.execute(query, parameters)

    def get_objects(self, application: str, tag: str):
        """
        Get Objects to upload per tags
        :return: Linked objects
        """
        # Get the query to link an aip object
        query = self.query_service.get_query("tags", "get_tagged_object")
        query = query.replace_anchors("APPLICATION", application)

        params = {
            "tag": tag
        }

        # Execute
        return self.neo4j_al.execute(query, params)