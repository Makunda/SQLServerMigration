from typing import List


class DeadCodeResult:

    def __init__(self, object_type: str, total_object: int, total_unused: int):
        """
        Initialize the Dead code results
        :param object_type: Object type to process
        :param total_object: Total number of object for this type
        :param total_unused: Total number of not used object
        """
        self.__object_type = object_type
        self.__total_object = total_object
        self.__total_unused = total_unused

        if self.__total_object == 0:
            self.__ratio = 0
        elif self.__total_unused == 0:
            self.__ratio = 100
        else:
            self.__ratio = 100 * (self.__total_unused / self.__total_object)

    def set_total_object(self, num_object: int):
        """
        Set the total number of object
        :param num_object:
        :return:
        """
        self.__total_object = num_object

    def set_total_unused(self, num_object: int):
        """
        Set the total number of unused object
        :param num_object:
        :return:
        """
        self.__total_unused = num_object

    @staticmethod
    def get_headers() -> List[str]:
        return [
            "Object Type",
            "Total Object",
            "Total Unused Object",
            "Ratio"
        ]

    def get_values(self):
        return [
            self.__object_type,
            self.__total_object,
            self.__total_unused,
            self.__ratio,

        ]
