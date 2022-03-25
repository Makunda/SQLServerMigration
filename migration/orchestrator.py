from typing import List

from logger import Logger
from migration.steps.asbtract_step import AbstractStep
from migration.steps.community_creation_step import CommunityCreationStep
from migration.steps.dead_code_step import DeadCodeStep


class Orchestrator:
    """
    Orchestrator of the modernization steps
    """

    def __init__(self):
        """
        Orchestrator
        """
        self.__logger = Logger.get_logger("Orchestrator")
        self.__steps:List[AbstractStep] = [DeadCodeStep(), CommunityCreationStep()]

    def launch(self):
        """
        Launch the Orchestrator
        :return:
        """
        for i in self.__steps:
            try:
                i.launch()
            except Exception as e:
                self.__logger.error("Failed on step with name : {}".format(i.get_name()), e)
                raise RuntimeError("Process failed on step {}".format(i.get_name()))