from utils.json.JsonUtils import JSONUtils


class ApiResponse:
    """
    API Response to send
    """

    def __init__(self, message: str, data = None, errors=None):
        """
        Initialize an Api response
        :param message: Message to send ( as String )
        :param data: Data to pass ( as Any )
        :param errors: Errors of the server ( as String array )
        """
        if errors is None:
            errors = []

        self.__message = message
        self.__data = data
        self.__errors = errors

    def repr_json(self) -> dict:
        """
        Serialize the Api response into in a dictionary
        :return:
        """
        return dict(
            message=self.__message,
            data=self.__data,
            errors=self.__errors
        )

