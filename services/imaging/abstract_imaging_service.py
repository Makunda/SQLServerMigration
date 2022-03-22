from abc import ABC

from db.neo4j.neo4j_al import Neo4jAl
from utils.query_loader import QueryLoader


class AbstractImagingService(ABC):

    def __init__(self):
        """
        Declare common variables for all services
        """
        self._neo4j_al = Neo4jAl()
        self._query_service = QueryLoader()
