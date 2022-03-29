from metaclass.SingletonMeta import SingletonMeta
from utils.yml.yml_folder_reader import YMLFolderReader


class MigrationConfiguration(metaclass=SingletonMeta):

    def __init__(self):
        yml_folder = YMLFolderReader("configuration/migration/")
        self.__yml_configuration = yml_folder.get_full_content()

    def get_migration_levels(self):
        """
        Get the migration level
        :return:
        """
        return self.__yml_configuration["slq_migration"]["sql_level"]