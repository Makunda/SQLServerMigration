class CypherQuery:
    """
    Class handling cypher queries
    """

    def __init__(self, query: str, anchors: list, params: list, returns: [] or None, name: str = ""):
        self.__query = query
        self.__params = params
        self.__anchors = anchors
        self.__returns = returns

        # Optional
        self.__name = name

    def get_name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None :
        self.__name = name

    def get_return_value(self) -> [] or None:
        """
        Element returned by the query
        :return:
        """
        return self.__returns

    def get_query(self) -> str:
        """
        Get the value string of the query
        :return:  Cypher query as a string
        """
        return self.__query

    def replace_anchors(self, parameters: dict) -> str:
        """
        Replace the anchors in the SQL query
        :param parameters:  Parameters to change
        :return: New string
        """
        for key in parameters:
            to_replace = "$${0}$$".format(key)
            self.__query = self.__query.replace(to_replace, parameters[key])
        return self.__query

    def get_params(self) -> list:
        """
        Get the parameters to match
        :return: The list of parameters
        """
        return self.__params

    def verify_params(self, parameters: dict) -> bool:
        """
        Verify if all the parameters are presents
        :param parameters:  List of parameters to run the query
        :return:  True, if the inputs meet the requirements, False otherwise
        """
        for key in self.__params:
            if key not in parameters.keys():
                raise ValueError("Invalid query {0}. Missing parameter: ${1}".format(self.__query, key))

        for an in self.__anchors:
            if an in self.__query:
                raise ValueError("Invalid query {0}. Anchor not replaced: {1}".format(self.__query, an))

        return True

    def to_string(self):
        return "CypherQuery {" \
               "    query: " + self.__query + \
               "    }"
