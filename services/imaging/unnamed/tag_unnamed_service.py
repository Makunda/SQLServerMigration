from services.imaging.abstract_imaging_service import AbstractImagingService


class TagUnnamedService(AbstractImagingService):
    """
    Handle global tag handling
    """

    def get_objects(self, application: str, tag: str):
        """
        Get Objects to upload per tags
        :return: Linked objects
        """
        # Get the query to link an aip object
        query = self._query_service.get_query("tags", "get_tagged_object")
        query = query.replace_anchors("APPLICATION", application)

        params = {
            "tag": tag
        }

        # Execute
        return self._neo4j_al.execute(query, params)