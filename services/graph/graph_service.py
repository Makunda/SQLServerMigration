from db.neo4j.neo4j_al import Neo4jAl
from utils.query.query_loader import QueryLoader


class GraphService:
    """
    Graph Service wrapping GDS Graph creation
    """

    def __init__(self):
        self.__neo4j_al = Neo4jAl()
        self.__query_service = QueryLoader()

    def delete_graph(self, graph_name: str, fail_if_missing: bool = False) -> None:
        """
        Delete the graph on the database
        :param graph_name: Name of the graph
        :param fail_if_missing: If True, hrow an error if the graph is missing
        :return:
        """
        # Get the query to link an aip object
        query = self.__query_service.get_query("gds_graph", "drop_graph")

        parameters = {
            "graphName": graph_name,
            "failIfMissing": fail_if_missing
        }

        # Execute
        self.__neo4j_al.execute(query, parameters)

    def create_graph_by_property(self, application: str, graph_name: str, object_property: str, value: str) -> None:
        """
        Create a graph with a specific name
        :param application: Name of the application
        :param object_property: Property to get
        :param value: Value of this property
        :param graph_name: Name of the graph
        :return:
        """
        # Get the query to link an aip object
        query = self.__query_service.get_query("gds_graph", "create_graph_by_property")
        query.replace_anchors({"APPLICATION": application, "PROPERTY_NAME": object_property})

        parameters = {
            "propValue": '"' + value + '"',
            "graphName": graph_name
        }

        # Execute
        self.__neo4j_al.execute(query, parameters)
