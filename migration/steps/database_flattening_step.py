from typing import List

from logger import Logger
from migration.steps.asbtract_step import AbstractStep
from services.demeter.architecture_service import DemeterArchitectureService
from services.imaging.object_service import ObjectService
from utils.configuration.default_configuration import DefaultConfiguration
from utils.configuration.migration_configuration import MigrationConfiguration


class DatabaseFlatteningStep(AbstractStep):
    """
        Create an architecture view with all the objects in the database
    """

    def get_name(self) -> str:
        return "Database Flattening Step"

    def __init__(self):
        super(DatabaseFlatteningStep, self).__init__()

        self.__logger = Logger.get_logger("Database flattening step")

        self.__configuration = DefaultConfiguration()
        self.__migration_configuration = MigrationConfiguration()

        self.__object_service = ObjectService()
        self.__architecture_service = DemeterArchitectureService()

    def create_singleton_architecture(self, architecture_name: str, levels: List[str]) -> None:
        """
        Create an architecture with a single subset
        :param architecture_name: Name of the architecture
        :param levels: Levels to extract
        :return: None
        """
        objects = self.__object_service.get_object_by_levels(self.get_application(), levels)

        for obj in objects:
            self.__architecture_service.flag_object_architecture(architecture_name, "Database Monolith", obj)

    def launch(self):
        """
        Launch the flattening step
        :return:
        """
        self.__logger.info("Database flattening step launched..")
        step_name = "Step3_Full Database"
        levels = self.__migration_configuration.get_migration_levels()

        # Delete old architecture
        self.__logger.info("Deleting old architecture.")
        self.__architecture_service.delete_architecture_if_exists(self.get_application(), step_name)

        # Find db object and create architecture
        self.__logger.info("Creating new flattened view.")
        self.create_singleton_architecture(step_name, levels)
        self.__architecture_service.group_architecture(self.get_application())
