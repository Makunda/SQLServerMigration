from neo4j.graph import Relationship

from services.imaging.abstract_imaging_service import AbstractImagingService


class RelationshipService(AbstractImagingService):
    """
    Service managing relationships in AIP
    """

    def __init__(self):
        super(RelationshipService, self).__init__()

    def apply_property(self, relationship: Relationship, property_name: str, property_value: any) -> Relationship:
        """
        Apply a property on a relationship
        :param relationship: Relationship to process
        :param property_name: Property name
        :param property_value: Value to apply
        :return: None
        """
        query = self.query_service.get_query("relationships", "apply_property")
        query.replace_anchors({
            "PROPERTY": property_name
        })

        return self.neo4j_al.execute(query, {
            "IdRelationship": relationship.id,
            "PropertyValue": property_value
        })

    def apply_property(self, relationship: Relationship, property_name: str, property_value: any) -> Relationship:
        """
        Apply a property on a relationship
        :param relationship: Relationship to process
        :param property_name: Property name
        :param property_value: Value to apply
        :return: None
        """
        query = self.query_service.get_query("relationships", "apply_property")
        query.replace_anchors({
            "PROPERTY": property_name
        })

        return self.neo4j_al.execute(query, {
            "IdRelationship": relationship.id,
            "PropertyValue": property_value
        })