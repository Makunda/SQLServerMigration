from typing import List

from logger import Logger
from migration.steps.asbtract_step import AbstractStep
from migration.steps.community_creation_step import CommunityCreationStep
from migration.steps.database_flattening_step import DatabaseFlatteningStep
from migration.steps.dead_code_step import DeadCodeStep
from migration.steps.transactional_step import TransactionalStep


class Orchestrator:
    """
    Orchestrator of the modernization steps
    """

    def __init__(self):
        """
        Orchestrator
        """
        self.__logger = Logger.get_logger("Orchestrator")
        self.__steps: List[AbstractStep] = [DeadCodeStep(),  TransactionalStep(), DatabaseFlatteningStep(), CommunityCreationStep()]
        # self.__steps: List[AbstractStep] = [CommunityCreationStep()]

    def launch(self):
        """
        Launch the Orchestrator
        :return:
        """
        for i in self.__steps:
            try:
                self.__logger.info("Step {} launched.".format(i.get_name()))
                i.launch()
                self.__logger.info("Step {} has been completed.".format(i.get_name()))
            except Exception as e:
                self.__logger.error("Failed on step with name : {}".format(i.get_name()), e)
