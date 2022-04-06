import re
from typing import List, Dict

from neo4j.graph import Relationship

from db.neo4j.neo4j_al import Neo4jAl
from migration.interfaces.link_weight import LinkWeightInput
from utils.configuration.default_configuration import DefaultConfiguration
from utils.configuration.graph_prop_configuration import GraphSpreadConfiguration
from utils.query.query_loader import QueryLoader


class GraphWeightService:
    """
    Service Managing the list weights in the graph
    """

    def __init__(self):
        self.__neo4j_al = Neo4jAl()
        self.__query_service = QueryLoader()

        self.__configuration = DefaultConfiguration()
        self.__graph_configuration = GraphSpreadConfiguration()

        self.__application = self.__configuration.get_value("general", "application")
        self.__buffer_link_weight_map: Dict[str, List[LinkWeightInput]] = {}

    def __apply_weight(self, relationship: Relationship, weight: float) -> None:
        """
        Apply a weight property on a relationships
        :param relationship: Relationship to process
        :param weight: Weight to apply
        :return: None
        """
        assert weight is not None
        assert relationship is not None and relationship.id is not None

        query = self.__query_service.get_query("relationships", "apply_property")
        query.replace_anchors({
            "PROPERTY": self.__graph_configuration.get_graph_spread_property()
        })

        self.__neo4j_al.execute(query, {"IdRelationship": relationship.id,
                                        "PropertyValue": weight})

    def __remove_all_weight(self) -> None:
        """
        Remove all the weights from the database
        :return: None
        """
        query = self.__query_service.get_query("relationships", "remove_property_on_all")
        query.replace_anchors({
            "APPLICATION": self.__application,
            "PROPERTY": self.__graph_configuration.get_graph_spread_property()
        })

        self.__neo4j_al.execute(query)

    def process_relationship(self, relationship: Relationship) -> None:
        """
        Process and apply a weight on the relationship based on the configuration
        :param relationship: Relationship to process
        :return: None
        """
        rel_name = relationship.type
        if rel_name not in self.__buffer_link_weight_map.keys():
            # Get and order the list
            rel_list = self.__graph_configuration.get_relationships_by_name(rel_name)
            rel_list.sort(key=lambda a: a.regex)
            self.__buffer_link_weight_map[rel_name] = rel_list

        # Parse the list of matched items
        detected_weight = 1

        for rel in self.__buffer_link_weight_map[rel_name]:

            # Process the regex
            if rel.has_regex() and relationship.get("details", []) != []:
                # Test the regex to verify if the details match
                details_list = list(relationship.get("details", []))

                # Get details list and parse them
                for line in details_list:
                    if re.search(rel.get_regex(), line):
                        detected_weight = rel.get_weight()

            else:
                # No regex / simple
                detected_weight = rel.get_weight()

        self.__apply_weight(relationship, detected_weight)
