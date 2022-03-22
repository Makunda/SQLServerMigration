import os
import glob
import logging
import checksumdir

from typing import List


class FolderUtils:
    """
    Static class managing the folders
    """

    @staticmethod
    def merge_folder(path: str):
        """
        Check a folder and create it if necessary
        :param path Path of the folder to create
        :return:
        """
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(path)
            logging.info("New folder created at: {0}.".format(path))

    @staticmethod
    def get_folder_checksum(path: str):
        """
        Calculate and return the checksum of a directory
        :param path: Path of the directory to hash
        :return: The checksum
        """
        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:
            raise FileNotFoundError("Cannot calculate the checksum of a nonexistent folder. Path: {}".format(path))
        return checksumdir.dirhash(path)

    @staticmethod
    def list_folder(path: str, recursive=False, extension=None) -> List[str]:
        """
        List all the files in the folder
        :param path: Path of the folder
        :param recursive: Activate the recursively
        :param extension: Extension of files to discover
        :return:
        """
        if extension is not None:
            path = os.path.join(path, "**/*" + str(extension))
        return glob.glob(path, recursive=recursive)

    @staticmethod
    def exists(path: str) -> bool:
        """
        Verify that the path exists
        :param path: path to verify
        :return: Boolean value
        """
        return os.path.exists(path)
