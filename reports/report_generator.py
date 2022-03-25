import csv
import os
from typing import List, IO

from logger import Logger


class ReportGenerator:
    """
    Report generation
    """

    class Report:
        """
        Inner class returned by the builder
        """

        def __init__(self, file: IO, headers: List):
            # Open files and headers
            self.__file = file
            self.__headers = headers

            # Open CSV writers
            self.__csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.__csv_writer.writerow(headers)

        def get_file_name(self):
            """
            Get the full name of the file
            :return:
            """
            return self.__file.name

        def write(self, values: List):
            """
            Write a row to the report
            :param values: Values to write
            :return:
            """
            self.__csv_writer.writerow(values)

        def write_multiple(self, values: List[List]):
            """
            Write multiple row to the report
            :param values: Values to write
            :return:
            """
            for row in values:
                self.__csv_writer.writerow(row)

        def close(self):
            """
            Close the file
            :return:
            """
            if self.__file:
                self.__file.close()

        def __del__(self):
            """
            Close the file when the object is deleted
            :return:
            """
            self.close()

    def __init__(self):
        self.__logger = Logger.get_logger("Report Generator")

        self.__path = ""
        self.__file_name = ""
        self.__file_extension = ".csv"
        self.__headers = []

        self.__file = None
        pass

    @staticmethod
    def get_report_generator():
        """
        Get an instance of the report generator
        :return:
        """
        return ReportGenerator()

    def set_path(self, path: str):
        """
        Set path of the folder
        :param path:
        :return:
        """
        self.__path = path
        return self

    def set_file_name(self, name: str):
        self.__file_name = name
        return self

    def set_headers(self, headers: str):
        self.__headers = headers
        return self

    def build(self):
        """
        Build and return a report
        :return:
        """
        if self.__file_name == "":
            raise ValueError("File Name cannot be empty")

        if len(self.__headers) == 0:
            raise ValueError("Headers cannot be empty")

        if os.path.isfile(self.__path):
            raise ValueError("Path doesn't exist")

        file_name = self.__file_name
        if not file_name.endswith(self.__file_extension):
            file_name = file_name + ".csv"

        file_path = os.path.join(self.__path, file_name)
        file = None

        try:
            file = open(file_path, 'w+', newline='')
            report = self.Report(file, self.__headers)
            return report
        except Exception as e:
            if file is not None:  # Close the file if opened
                file.close()
            self.__logger.error("Failed to create the file at {0}.".format(file_path), e)
            raise FileNotFoundError("Cannot create the file at {0}.".format(file_path))
