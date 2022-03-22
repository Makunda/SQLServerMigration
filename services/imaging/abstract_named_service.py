from abc import ABC

from db.neo4j.neo4j_al import Neo4jAl
from services.imaging.abstract_imaging_service import AbstractImagingService
from utils.query_loader import QueryLoader


class AbstractNamedImagingService(AbstractImagingService):

    def __init__(self, application: str):
        """
        Declare common variables for all services
        """
        super().__init__()
        self._neo4j_al = Neo4jAl()
        self._query_service = QueryLoader()
        self._application = application
