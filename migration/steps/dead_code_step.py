import os
from typing import List

from interfaces.imaging.imaging_object import ImagingObject
from interfaces.results.dead_code_result import DeadCodeResult
from logger import Logger
from migration.steps.asbtract_step import AbstractStep
from reports.report_generator import ReportGenerator
from services.imaging.tag_service import ImagingTagService
from services.statistics.dead_code_service import DeadCodeService

from utils.configuration.migration_configuration import MigrationConfiguration
from utils.folder.folder_utils import FolderUtils
from utils.folder.workspace_utils import WorkspaceUtils


class DeadCodeStep(AbstractStep):
    """
    Step to extract the volume of dead code as well as the objects
    """

    def get_name(self) -> str:
        return "Dead code setup"

    def __init__(self):
        """
        Initialize the dead code step
        :return:
        """
        super().__init__()
        self.__logger = Logger.get_logger("Dead Code Setup")

        # Services
        self.__dead_code = DeadCodeService()
        self.__tag_service = ImagingTagService()

        self.__migration_configuration = MigrationConfiguration()
        self.__object_type = self.__migration_configuration.get_migration_levels()

        self.__file_dir = self.workspace_util.merge_file("Dead Code/")

    def generate_global_report(self):
        """
        Generate the Global report
        :return:
        """
        # Generate the full report of records for the types
        record_list = [self.__dead_code.get_record_by_type(self.get_application(), x).get_values() for x in
                       self.__object_type]

        self.generate_excel("Dead_code_report", self.__file_dir, DeadCodeResult.get_headers(), record_list)

    def generate_single_reports(self):
        """
        Generate  a list of report for all the types
        :return:
        """

        for obj_type in self.__object_type:
            record_list = self.__dead_code.get_unused_objects_by_type(self.get_application(), obj_type)
            self.generate_excel("Dead_code_details_{}".format(obj_type.replace(" ", "_")), self.__file_dir,
                                ImagingObject.get_headers(), [x.get_values() for x in record_list])

    def tag_unused_objects(self):
        for obj_type in self.__object_type:
            record_list = self.__dead_code.get_unused_objects_by_type(self.get_application(), obj_type)
            for rec in record_list:
                self.__tag_service.create_tag(rec.get_node(), "Dead Code")



    def launch(self):
        """
        Launch the export step
        :return:
        """
        # Generate Global report
        self.generate_global_report()

        # Generate single reports
        self.generate_single_reports()

        # Tag objects
        self.tag_unused_objects()
