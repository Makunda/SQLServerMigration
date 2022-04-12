from abc import ABC, abstractmethod

from flask_socketio import SocketIO


class WebSocketController(ABC):

    def __init__(self, application: SocketIO):
        """
        Declare and attach a Socket IO application to the controller
        :param application: Socket IO application to attach
        """
        self.application = application

    def get_namespace(self):
        """
        Get the default namespace of the controller
        :return:
        """
        return ""

    @abstractmethod
    def register(self):
        pass  # To implement
