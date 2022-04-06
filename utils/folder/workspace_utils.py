import os

from definitions import ROOT_DIR
from metaclass.SingletonMeta import SingletonMeta
from utils.configuration.default_configuration import DefaultConfiguration
from utils.folder.folder_utils import FolderUtils


class WorkspaceUtils(metaclass=SingletonMeta):
    """
    Workspace manager setting up the folder if necessary
    """

    def __init__(self):
        """
        Initialize the workspace
        """
        self.__configuration = DefaultConfiguration()
        workspace_path = self.__configuration.get_value("folders", "workspace")
        application = self.__configuration.get_value("general", "application")

        # Check Workspace
        if os.path.isabs(workspace_path):
            self.__workspace_folder = workspace_path
        else:
            relative_path = os.path.join(ROOT_DIR, workspace_path)
            self.__workspace_folder = relative_path

        # Add current application name
        self.__workspace_folder = os.path.join(self.__workspace_folder, application)
        FolderUtils.merge_folder(self.__workspace_folder)

    def get_workspace(self) -> str:
        """
        Get workspace path
        :return:
        """
        return self.__workspace_folder

    def merge_entry(self, folder: str) -> str:
        """
        Create the entry in the workspace if necessary
        :param folder: Name of the folder to create in the workspace
        :return: The absolute path of the new folder
        """
        entry_path = os.path.join(self.get_workspace(), folder)
        FolderUtils.merge_folder(entry_path)
        return entry_path

    def merge_file(self, file_path: str) -> str:
        """
        Merge a file in the workspace folder
        :param file_path: File path to create
        :return: The path of the file created
        """
        if os.path.isabs(file_path):
            raise RuntimeError("Cannot create the file from an absolute path")

        entry_path = os.path.join(self.get_workspace(), file_path)
        FolderUtils.merge_file(entry_path)
        return entry_path
