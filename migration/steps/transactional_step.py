from typing import List

from neo4j.graph import Node

from logger import Logger
from migration.steps.asbtract_step import AbstractStep
from services.communities.communites_algorithm_service import CommunitiesAlgorithmService
from services.demeter.architecture_service import DemeterArchitectureService
from services.imaging.object_service import ObjectService
from services.imaging.transaction_service import TransactionService
from utils.configuration.default_configuration import DefaultConfiguration
from utils.configuration.migration_configuration import MigrationConfiguration


class TransactionalStep(AbstractStep):
    """
    Transactional Step flagging object not in transactions
    """

    def __init__(self):
        super().__init__()
        self.__logger = Logger.get_logger("Community Procedure")

        self.__configuration = DefaultConfiguration()
        self.__migration_configuration = MigrationConfiguration()

        self.__object_service = ObjectService()
        self.__architecture_service = DemeterArchitectureService()
        self.__communities_algorithm = CommunitiesAlgorithmService()
        self.__transactional_service = TransactionService()

        self.__application = self.__configuration.get_value("general", "application")

    def get_name(self) -> str:
        return "Transactional Step"

    def flag_object_not_in_transaction(self, architecture_name: str, to_include_type: List[str]):
        """
        Get and flag objects in Transactions
        :return:
        """
        objects = self.__transactional_service.get_objects_not_in_transaction_by_levels(self.__application,
                                                                                        to_include_type)
        for obj in objects:
            self.__architecture_service.flag_object_architecture(architecture_name, "Not in Transaction", obj)

    def flag_object_in_transaction(self, architecture_name: str, to_include_type: List[str]):
        """
        Get and flag objects in Transactions
        :return:
        """
        objects = self.__transactional_service.get_objects_in_transaction_by_levels(self.__application,
                                                                                    to_include_type)
        for obj in objects:
            self.__architecture_service.flag_object_architecture(architecture_name, "In Transaction", obj)

    def launch(self):
        """
        Launch th
        :return:
        """
        step_name = "Step2_Transaction Investigation"
        levels = self.__migration_configuration.get_migration_levels()
        self.__architecture_service.delete_architecture_if_exists(self.__application, step_name)

        # Flag object
        self.flag_object_not_in_transaction(step_name, levels)
        self.flag_object_in_transaction(step_name, levels)

        # Migration
        self.__architecture_service.group_architecture(self.__application)
