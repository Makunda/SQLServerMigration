from typing import List

from metaclass.SingletonMeta import SingletonMeta
from migration.interfaces.caller_callee_weight import CallerCalleeWeightInput
from migration.interfaces.link_weight import LinkWeightInput
from utils.configuration.default_configuration import DefaultConfiguration
from utils.yml.yml_folder_reader import YMLFolderReader


class GraphSpreadConfiguration(metaclass=SingletonMeta):
    """
    Configuration handling the spread of the community on the graph
    """

    def __init__(self):
        # Retrieve YAML configuration
        yml_folder = YMLFolderReader("configuration/graph_propagation/")
        self.__yml_configuration = yml_folder.get_full_content()
        self.__configuration = DefaultConfiguration()

        self.__caller_callee_configuration: List[CallerCalleeWeightInput] = list()
        self.__link_configuration: List[LinkWeightInput] = list()

        # Load the configuration
        self.__load_graph_configuration()

    def get_graph_spread_property(self):
        """
        Get the migration level
        :return:
        """
        return self.__configuration.get_value("community", "community_relationship_property_weight")

    def __get_value(self, element, key: str) -> any:
        """
        Get a specific value of the record.
        This function raises an error if the element doesn't exist
        :param element: Element to parse
        :param key: Key to get
        :return: Value in the record
        """
        if key not in element:
            raise RuntimeError("The key '{}' does not exist in element '{}'.".format(key, element))
        return element[key]

    def __get_value_or_default(self, element, key: str, default = None) -> any:
        """
        Get a specific value of the record. If the key doesn't exist, the specified default value will be returned
        :param element: Element to parse
        :param key: Key to get
        :return: Value in the record
        """
        if key not in element:
            return default

        return element[key]

    def __load_link_weight(self):
        """
        Load the link weights to the configuration
        :return: None
        """
        records = self.__yml_configuration["link_weight"]
        for title in records:
            elem = records[title]
            try:
                formatted_rec = LinkWeightInput(
                    str(self.__get_value(elem, "rel_name")),
                    float(self.__get_value(elem, "value")),
                    str(self.__get_value_or_default(elem, "regex")),
                )
            except Exception as e:
                raise RuntimeError("Failed to deserialize as a 'Link Weight' : [{}] {}.".format(title, elem))

            self.__link_configuration.append(formatted_rec)

    def __load_caller_callee_weight(self):
        """
        Load the caller and callee weight to the configuration
        :return: None
        """
        records = self.__yml_configuration["caller_callee_weight"]
        for title in records.keys():
            print(title)
            elem = records[title]
            print(elem)
            try:
                formatted_rec = CallerCalleeWeightInput(
                    str(self.__get_value(elem, "src_type")),
                    str(self.__get_value(elem, "end_type")),
                    float(self.__get_value(elem, "value")),
                    str(self.__get_value_or_default(elem, "rel_name")),
                    str(self.__get_value_or_default(elem, "regex")),
                )

                self.__caller_callee_configuration.append(formatted_rec)
            except Exception as e:
                raise RuntimeError("Failed to deserialize as a 'Caller Callee Weight' : [{}] {}.".format(title, elem))

    def __load_graph_configuration(self):
        # Parse links
        self.__load_caller_callee_weight()
        self.__load_link_weight()

    def get_relationships_by_name(self, rel_type: str) -> List[LinkWeightInput]:
        """
        Get the list of relationship matching the name
        :param rel_type: Type of the relationship
        :return: List of matching relationships
        """
        return [x for x in self.__link_configuration if x.rel_name == rel_type]
