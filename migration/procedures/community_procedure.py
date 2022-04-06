import random
import time
from threading import Timer
from typing import List, Dict

from neo4j.graph import Node

from interfaces.imaging.imaging_object import ImagingObject
from logger import Logger
from migration.services.community_service import CommunityService
from migration.services.graph_weight_service import GraphWeightService
from services.communities.communites_algorithm_service import CommunitiesAlgorithmService
from services.demeter.architecture_service import DemeterArchitectureService
from services.graph.graph_service import GraphService
from services.imaging.object_service import ObjectService
from services.imaging.property_service import ImagingPropertyService
from services.imaging.tag_service import ImagingTagService
from services.imaging.transaction_service import TransactionService
from utils.configuration.default_configuration import DefaultConfiguration
from utils.configuration.migration_configuration import MigrationConfiguration


class CommunityProcedure:
    """
    Manage and create communities from a group of objects
    """

    def __init__(self):
        """
        Initialize the Community services
        """
        self.__logger = Logger.get_logger("Community Procedure")
        self.__tag_service = ImagingTagService()
        self.__property_service = ImagingPropertyService()

        # Community related
        self.__communities_algorithm = CommunitiesAlgorithmService()
        self.__community_service = CommunityService()
        self.__graph_service = GraphService()

        # Imaging services
        self.__object_service = ObjectService()
        self.__architecture_service = DemeterArchitectureService()
        self.__transaction_service = TransactionService()
        self.__graph_weight_service = GraphWeightService()

        self.__configuration = DefaultConfiguration()
        self.__migration_configuration = MigrationConfiguration()

        self.__application = self.__configuration.get_value("general", "application")
        self.__community_property = self.__configuration.get_value("community", "community_property")
        self.__community_object_property = self.__configuration.get_value("community", "community_object_property")

        self.__community_name = "sql_community"

    def flag_objects(self) -> None:
        # Clean old links
        self.__property_service.remove_property_with_value(self.__application, self.__community_property,
                                                           self.__community_name)

        # Get objects type to flag
        object_type = self.__migration_configuration.get_migration_levels()
        self.__property_service.add_property_by_types(self.__application, object_type, self.__community_property,
                                                      self.__community_name)

    def get_community_property(self) -> str:
        return self.__community_object_property

    def get_object_community(self, node: Node) -> None or str:
        """
        Get the community of the object or None if the property does not exist
        :return: The community property
        """
        return node.get(self.__community_object_property, None)

    def colorize_node(self) -> None:
        """
        Colorize the nodes based on their communities
        :return: None
        """
        # Get node list
        nodes = self.get_all_nodes()

        # Random colors
        r = lambda: random.randint(0, 255)

        # Build map name
        map_name = {}
        for n in nodes:
            community = n.get(self.__community_object_property, None)
            if community not in map_name.keys():
                map_name[community] = '#%02X%02X%02X' % (r(), r(), r())

        for n in nodes:
            # Parse the node, get the community property or skip
            community = n.get(self.__community_object_property, None)
            self.__property_service.add_property(n, "Color", map_name[community])

    def delete_architecture_if_exists(self, architecture_name: str) -> None:
        """
        Delete the architecture view
        :param architecture_name: Name of the architecture
        :return: None
        """
        # Get the architecture node
        architecture_node = self.__architecture_service.get_architecture_by_name(self.__application, architecture_name)

        # Delete the architecture node by id if found
        if architecture_node is None:
            return
        elif type(architecture_node) is Node:
            self.__architecture_service.delete_architecture(self.__application, architecture_node)
        elif type(architecture_node) is List:
            for n in architecture_node:
                self.__architecture_service.delete_architecture(self.__application, n)

    def get_transactions_by_single_community(self, community_id: any) -> List[Node]:
        """
        Get the list of transaction accessing a particular community
        :param community_id: Id of the community
        :return: The list of associated transactions
        """
        return self.__transaction_service.get_transaction_including_objects_with_property(
            self.__application,
            self.__community_property,
            community_id)

    def get_transactions_by_communities(self) -> Dict[Node, List[any]]:
        """
        Get the list of transaction in the application grouped by the value of the communities inside
        :return: Dictionary of transactions grouped by silo
        """
        # Map declaration
        transaction_nodes = self.__transaction_service.get_all_transactions_with_minimum_object(self.__application, 50)
        community_map: Dict[Node, List[any]] = dict()

        # For each group in the list of communities
        for tn in transaction_nodes:
            community_map[tn] = self.__transaction_service.get_prop_value_list_in_transaction(tn,
                                                                                              self.__community_property)

        return community_map

    def get_incoming_communities(self, community_id: any) -> List:
        """
        Get the Id of incoming communities
        :param community_id: Id of the communities
        :return:
        """
        return self.__community_service.get_incoming_communities(self.__application,
                                                                 self.__community_object_property,
                                                                 community_id)

    def get_outgoing_communities(self, community_id: any) -> List:
        """
        Get the Id of outgoing communities
        :param community_id: Id of the communities
        :return:
        """
        return self.__community_service.get_outgoing_communities(self.__application,
                                                                 self.__community_object_property,
                                                                 community_id)

    def group_architecture(self):
        """
        Group the architecture in the application
        :return: The group of application
        """
        self.__architecture_service.group_architecture(self.__application)

    def delete_graph(self, graph_name: str) -> None:
        """
        Delete a graph with a specific name
        :param graph_name: Name of the graph
        :return: None
        """
        try:
            self.__graph_service.delete_graph(graph_name)
        except Exception as e:
            self.__logger.warn("Failed to delete the graph")

    def create_graph(self, graph_name: str):
        """
        Create a new graph from the object flagged
        :param graph_name: Graph name
        :return:
        """
        self.__graph_service.create_graph_by_property(self.__application, graph_name, self.__community_property,
                                                      self.__community_name)

    def apply_weight_on_graph(self, graph_name: str) -> None:
        """
        Parse all the relationships of the graph and apply the weight property
        :param graph_name: Name of the graph
        :return: None
        """
        # Get all the relationships to flag
        relationships = self.__graph_service.get_graph_relationships(self.__application, self.__community_property,
                                                                     self.__community_name)
        self.__logger.info("Applying weight property on {} relationships.".format(len(relationships)))

        start = time.time()
        for i, rel in enumerate(relationships):
            self.__graph_weight_service.process_relationship(rel)
            if i % 100 == 0:
                end = time.time()
                self.__logger.info("Processed {} on {}. Average Time per relationship: {}."
                                   .format(i, len(relationships), (end - start) / (i + 1)))

    def execute_label_propagation(self, graph_name: str):
        """
        Execute the label propagation algorithm
        :param graph_name: Name of graph
        :return:
        """
        self.__communities_algorithm.launch_label_propagation(graph_name, self.__community_object_property)

    def flag_architectures_below_50(self, architecture_name: str, subset=None):
        """
        Get Statistics
        :return:
        """
        nodes = self.__community_service.get_communities_below(self.__application, self.__community_object_property,
                                                               150)
        # Build map name
        map_name = {}
        for n in nodes:
            community = n.get(self.__community_object_property, None)
            if community not in map_name.keys():
                map_name[community] = 1
            else:
                map_name[community] = map_name[community] + 1

        map_name = {k: v for k, v in sorted(map_name.items(), key=lambda item: item[1])}

        for n in nodes:
            # Parse the node, get the community property or skip
            community = n.get(self.__community_object_property, None)
            community_name = "Fragment {}".format(list(map_name.keys()).index(community))

            if community and not subset:
                self.__architecture_service.flag_object_architecture(architecture_name, community_name, n)
            else:
                self.__architecture_service.flag_object_architecture(architecture_name, subset, n)

    def flag_architectures_above_50(self, architecture_name: str, subset=None):
        """
        Get Statistics
        :return:
        """
        nodes = self.__community_service.get_communities_above(self.__application, self.__community_property, 150)

        # Build map name
        map_name = {}

        for n in nodes:
            community = n.get(self.__community_object_property, None)
            if community not in map_name.keys():
                map_name[community] = 1
            else:
                map_name[community] = map_name[community] + 1

        map_name = {k: v for k, v in sorted(map_name.items(), key=lambda item: item[1])}

        for n in nodes:
            # Parse the node, get the community property or skip
            community = n.get(self.__community_object_property, None)
            community_name = "Monolith {}".format(list(map_name.keys()).index(community))

            if community and not subset:
                self.__architecture_service.flag_object_architecture(architecture_name, community_name, n)
            else:
                self.__architecture_service.flag_object_architecture(architecture_name, subset, n)

    def get_all_nodes(self) -> List[Node]:
        """
        Return all the nodes flagged with the community attribute
        :return: The list of node containing the community attribute
        """
        nodes = []
        nodes.extend(
            self.__community_service.get_communities_above(self.__application, self.__community_property, 50))
        nodes.extend(
            self.__community_service.get_communities_below(self.__application, self.__community_property, 50))
        return nodes

    def get_all_nodes_as_imaging_object(self) -> List[ImagingObject]:
        """
        Return all the nodes flagged with the community attribute
        :return: The list of node containing the community attribute
        """

        ret_list = []
        for n in self.get_all_nodes():
            ret_list.append(self.__object_service.object_to_imaging_object(n))
        return ret_list

    def detect(self):
        """
        Launch and flag objects for database migration
        :return:
        """
        graph_name = "SQLMigration"

        # Delete previous groups
        self.__logger.info("Deleting old graph...")
        self.delete_graph(graph_name)

        # Flagging the community to investigate
        self.__logger.info("Identification of the graph population...")
        self.flag_objects()

        # Create graph
        self.__logger.info("Creating new graph...")
        self.create_graph(graph_name)

        # Apply properties
        self.apply_weight_on_graph(graph_name)

        # Execute label propagation
        self.__logger.info("Execute the label propagation on the graph...")
        self.execute_label_propagation(graph_name)

        # Flag communities
        self.__logger.info("Flagging big communities...")
        step_name = "Step4_Database Monoliths"
        self.delete_architecture_if_exists(step_name)  # Delete the architecture
        self.flag_architectures_below_50(step_name, "Others")
        self.flag_architectures_above_50(step_name)
        self.group_architecture()

        self.__logger.info("Flagging all communities...")
        step_name = "Step5_Database Communities"
        self.delete_architecture_if_exists(step_name)  # Delete the architecture
        self.flag_architectures_below_50(step_name)
        self.flag_architectures_above_50(step_name)
        self.group_architecture()

        self.__logger.info("Changing node color by communities.")
        self.colorize_node()

        self.__logger.info("Deleting the graph.")
        self.delete_graph(graph_name)

