from api.websocket.controllers.websockets.websocket_controller import WebSocketController
from api.websocket.interfaces.graph.responses.get_graph_by_name import GetGraphByName
from api.websocket.interfaces.websocket_response import WebSocketResponse


class StatusController(WebSocketController):

    def get_namespace(self):
        return "/graph"

    def get_graph(self, data: GetGraphByName):
        """
        Get the status of the Web Socket server
        :return:
        """

        return WebSocketResponse("status", True, []).repr_json(), 200

    def register(self):
        self.application.on_event("get_graph", self.get_graph, self.get_namespace())