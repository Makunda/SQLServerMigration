from services.imaging.abstract_named_service import AbstractNamedImagingService


class TagImagingService(AbstractNamedImagingService):

    def __init__(self, application: str):
        super(TagImagingService, self).__init__(application)

    def create_tag_by_aipId(self, aipId: str, tag: str) -> None:
        """
        Create a Tag on an object in cast Imaging
        :param aipId: AIP Id of the object to tag
        :param tag: Tag to apply on the object
        :return: Void
        """
        # Get the query
        query = self._query_service.get_query("tags", "create_by_aipid")
        query.replace_anchors({"APPLICATION": self._application})

        # Declare parameters
        parameters = {
            "tag": tag,
            "aipId": aipId
        }

        # Execute
        self._neo4j_al.execute(query, parameters)

    def create_tag_by_id(self, id: int, tag: str) -> None:
            """
            Create a Tag on an object in cast Imaging
            :param id: Id of the object to tag
            :param tag: Tag to apply on the object
            :return: Void
            """
            # Get the query
            query = self._query_service.get_query("tags", "create_by_id")
            query.replace_anchors({"APPLICATION": self._application})

            # Declare parameters
            parameters = {
                "tag": tag,
                "id": id
            }

            # Execute
            self._neo4j_al.execute(query, parameters)
