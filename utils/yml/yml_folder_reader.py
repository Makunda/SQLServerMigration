import os
from typing import List, Any, Dict

import yaml

from definitions import ROOT_DIR
from logger import Logger
from utils.folder.folder_utils import FolderUtils


class YMLFolderReader:

    def __init__(self, file_path: str):
        # Verify the path
        if not FolderUtils.exists(file_path):
            raise FileNotFoundError("Cannot instantiate the YML Folder reader on a non-existent folder")

        self.__logger = Logger.get_logger("YAML Folder reader")
        self.__query_folder = os.path.join(ROOT_DIR, file_path)

        self.__content = dict()

    def __list_file(self) -> List[str]:
        """
            List yml files
            :return: the list of files containing queries
        """
        return FolderUtils.list_folder(self.__query_folder, True, ".yml")

    def __get_yml_content(self, file_path: str):
        """
        Get the content of the YAML Files
        :param file_path: File path to treat
        :return:
        """
        # Verify yml
        if not file_path.endswith(".yml"):
            raise FileNotFoundError("Cannot process non-yml files.")

        # open the file and get the configuration
        yml_conf: Any = None
        with open(file_path, "r") as stream:
            try:
                yml_conf = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                self.__logger.error(
                    "Failed to process query configuration file at '{0}'. File ignored.".format(file_path), e)

        # If file is empty
        if yml_conf is None:
            self.__logger.error("Query file at '{0}' is empty.".format(file_path))

        return yml_conf

    def __merge_content(self, yaml_content):
        """
        Merge the content
        :param yaml_content:
        :return:
        """
        if not yaml_content:  # If the yaml_content is empty  / none
            return

        loaded_sections = 0
        # Parse the configuration and build the list
        for section_name in yaml_content.keys():
            try:
                # Load the section
                # if section is empty remove
                if len(yaml_content[section_name]) == 0:
                    self.__logger.warning("Sections {0} is empty.".format(section_name))
                    continue

                # Else process the section
                if section_name not in self.__content.keys():
                    self.__content[section_name] = dict()
                else:
                    self.__logger.warning("Sections {0} already exist and will be overloaded.".format(section_name))

                self.__content[section_name].update(yaml_content[section_name])
                loaded_sections += 1

            except Exception as e:
                self.__logger.error("Sections {0} has been ignored.".format(section_name), e)

        self.__logger.info("Sections {0} has been discovered.".format(loaded_sections))

    def get_full_content(self) -> Any:
        """
        List the content of the repository selected
        :return:
        """
        # List all the files
        files = self.__list_file()
        self.__logger.info("{} files discovered at '{}'.".format(len(files), self.__query_folder))

        # List all content
        for f in files:
            # Get content
            yaml_content = self.__get_yml_content(f)

            if not yaml_content:  # If the yaml_content is empty  / none
                self.__logger.warning("File '{0}' is empty.".format(f))

            self.__merge_content(yaml_content)

        return self.__content
