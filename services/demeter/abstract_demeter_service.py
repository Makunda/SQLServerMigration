from services.imaging.abstract_imaging_service import AbstractImagingService


class AbstractDemeterService(AbstractImagingService):
    """
        Abstract services for demeter
    """

    def __init__(self):
        super().__init__()

        # Verify if the demeter extension is installed
        if not self.health_check():
            raise RuntimeError("Demeter extension is not installed on this ")

    def health_check(self) -> bool:
        """
        Return if the extension has been installed or not
        :return:  True if Demeter is installed, false otherwise
        """
        try:
            query = self.query_service.get_query("demeter", "health_check")
            self.neo4j_al.execute(query)
            return True
        except:
            return False
