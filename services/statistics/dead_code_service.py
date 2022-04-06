from typing import List

from interfaces.imaging.imaging_object import ImagingObject
from interfaces.results.dead_code_result import DeadCodeResult
from services.imaging.object_service import ObjectService


class DeadCodeService:
    """
    Dead code services
    """

    def __init__(self):
        """
        Initialize the dead code services with an application
        :param application:
        """
        self.__object_service = ObjectService()

    def get_record_by_type(self, application: str, object_type: str) -> DeadCodeResult:
        """
        Get dead code record for a type in the KB
        :param application: Name of the application
        :param object_type: Type of the Object to look for
        :return:
        """
        num_object = self.__object_service.get_object_number_by_type(application, object_type)
        num_unused_object = self.__object_service.get_unused_object_number_by_type(application, object_type)
        return DeadCodeResult(object_type, num_object, num_unused_object)

    def get_unused_objects_by_type(self, application: str, object_type: str) -> List[ImagingObject]:
        """
        Get the list of unused object by type
        :param application: Name of the application
        :param object_type: Object type to query
        :return:
        """
        node_list = self.__object_service.get_unused_object_by_type(application, object_type)
        return list(map( lambda x : self.__object_service.object_to_imaging_object(x), node_list))