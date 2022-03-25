from logger import Logger
from services.communities.communites_algorithm_service import CommunitiesAlgorithmService
from services.demeter.architecture_service import DemeterArchitectureService
from services.graph.graph_service import GraphService
from services.imaging.property_service import ImagingPropertyService
from services.imaging.tag_service import ImagingTagService
from utils.configuration.default_configuration import DefaultConfiguration
from utils.configuration.migration_configuration import MigrationConfiguration


class CommunityProcedure:
    """
    Manage and create communities from a group of objects
    """

    def __init__(self):
        """
        Initialize the Community service
        """
        self.__logger = Logger.get_logger("Community Procedure")
        self.__tag_service = ImagingTagService()
        self.__property_service = ImagingPropertyService()
        self.__communities_algorithm = CommunitiesAlgorithmService()
        self.__graph_service = GraphService()
        self.__architecture_service = DemeterArchitectureService()

        self.__configuration = DefaultConfiguration()
        self.__migration_configuration = MigrationConfiguration()

        self.__application = self.__configuration.get_value("general", "application")
        self.__community_property = self.__configuration.get_value("community", "community_property")
        self.__community_object_property = self.__configuration.get_value("community", "community_object_property")

        self.__community_name = "sql_community"
        self.__architecture_name = "Step3_Communities"

    def flag_objects(self) -> None:
        # Clean old links
        self.__property_service.remove_property_with_value(self.__application, self.__community_property,
                                                           self.__community_name)

        # Get objects type to flag
        object_type = self.__migration_configuration.get_migration_levels()
        self.__property_service.add_property_by_types(self.__application, object_type, self.__community_property,
                                                      self.__community_name)

    def group_architecture(self):
        self.__architecture_service.group_architecture(self.__application)

    def delete_graph(self, graph_name: str):
        """
        Delete a graph with a specific name
        :param graph_name: Name of the graph
        :return:
        """
        self.__graph_service.delete_graph(graph_name)

    def create_graph(self, graph_name: str):
        """
        Create a new graph from the object flagged
        :param graph_name: Graph name
        :return:
        """
        self.__graph_service.create_graph_by_property(self.__application, graph_name, self.__community_property,
                                                      self.__community_name)

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
        nodes = self.__communities_algorithm.get_communities_above(self.__application, self.__community_object_property,
                                                                   50)
        for n in nodes:
            # Parse the node, get the community property or skip
            community = n.get(self.__community_object_property, None)
            if community and not subset:
                self.__architecture_service.flag_object_architecture(architecture_name, community, n)
            else:
                self.__architecture_service.flag_object_architecture(architecture_name, subset, n)

    def flag_architectures_above_50(self, architecture_name: str, subset=None):
        """
        Get Statistics
        :return:
        """
        nodes = self.__communities_algorithm.get_communities_above(self.__application, self.__community_property, 50)
        for n in nodes:
            # Parse the node, get the community property or skip
            community = n.get(self.__community_object_property, None)
            if community and not subset:
                self.__architecture_service.flag_object_architecture(architecture_name, community, n)
            else:
                self.__architecture_service.flag_object_architecture(architecture_name, subset, n)

    def detect(self):
        """
        Launch and flag objects for database migration
        :return:
        """
        graph_name = "SQLMigration"

        # Delete previous groups
        self.__logger.info("Deleting old graph...")

        # Flagging the community to investigate
        self.__logger.info("Identification of the graph population...")
        self.flag_objects()

        # Create graph
        self.__logger.info("Creating new graph...")
        self.create_graph(graph_name)

        # Execute label propagation
        self.__logger.info("Execute the label propagation on the graph...")
        self.execute_label_propagation(graph_name)

        # Flag communities
        self.__logger.info("Flagging big communities...")
        self.flag_architectures_below_50("Step3_FirstSegmentation", "Garbage")
        self.flag_architectures_above_50("Step3_FirstSegmentation")
        self.group_architecture()

        self.__logger.info("Flagging all communities...")
        self.flag_architectures_below_50("Step4_FistSegmentation")
        self.flag_architectures_above_50("Step4_FistSegmentation")
        self.group_architecture()
