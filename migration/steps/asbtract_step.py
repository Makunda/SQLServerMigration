from abc import ABC, abstractmethod
from typing import List

from logger import Logger
from reports.report_generator import ReportGenerator
from services.demeter.architecture_service import DemeterArchitectureService
from utils.configuration.default_configuration import DefaultConfiguration
from utils.folder.folder_utils import FolderUtils
from utils.folder.workspace_utils import WorkspaceUtils


class AbstractStep(ABC):

    def __init__(self):
        """
        Abstract class step
        """
        self.__logger = Logger.get_logger("Abstract Step")
        self.__configuration = DefaultConfiguration()
        self.__application = self.__configuration.get_value("general", "application")

        self.workspace_util = WorkspaceUtils()

        self.__architecture_service = DemeterArchitectureService()

    def generate_excel(self, title: str, folder_path: str, headers: List[str], rows: List[List]):
        """
        Generate the excel report base on the passed rows
        :param title: Title of the report
        :param folder_path: Folder of the report
        :param headers: Headers of the records
        :param rows: Rows to insert
        :return:
        """
        # Append the CSV extension and create the extension
        FolderUtils.merge_file(folder_path)

        report = None
        try:
            report = ReportGenerator().set_path(folder_path) \
                .set_file_name(title).set_headers(headers).build()

            for i, rec in enumerate(rows):
                if i % 100 == 0:
                    self.__logger.info("Wrote {} of {} to '{}'.".format(i, len(rows), report.get_file_name()))
                report.write(rec)  # Write row
        except Exception as e:
            self.__logger.error("Failed to generate the report.", e)
        finally:
            # Report close
            if report is not None:
                report.close()


    def get_application(self):
        """
        Get the application name
        :return:
        """
        return self.__application

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the step
        :return: The name
        """
        pass

    @abstractmethod
    def launch(self):
        pass