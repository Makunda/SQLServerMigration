from utils.json.JsonUtils import JSONUtils


class WebSocketResponse:
    """
    Web Socket Response to send
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

    def get_data(self):
        return self.__data

    def get_message(self):
        return self.__message

    def get_errors(self):
        return self.__errors

    def repr_json(self) -> dict:
        """
        Serialize the Api response into in a dictionary
        :return:
        """
        data = self.__data
        if hasattr(self.__data, 'repr_json'):
            data = self.__data.repr_json()

        return dict(
            message=self.__message,
            data=data,
            errors=self.__errors
        )

    @staticmethod
    def convert_dict(data: dict):
        if "message" not in data.keys():
            raise ValueError("Missing Message key in Web socket response.")
        message = data["message"]

        response_data = None
        if "data" in data.keys():
            response_data = data["data"]

        errors = []
        if "errors" in data.keys():
            errors = data["errors"]

        return WebSocketResponse(message, response_data, errors)

