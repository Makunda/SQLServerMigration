# Get graph service
import uuid

from flask_socketio import emit

from api.websocket.controllers.websockets.websocket_controller import WebSocketController
from api.websocket.interfaces.graph.elements.graph_node import GraphNode
from api.websocket.interfaces.graph.responses.get_graph_by_name import GetGraphByName
from api.websocket.interfaces.graph.responses.graph_charachteristics import GraphCharacteristics
from api.websocket.interfaces.graph.responses.graph_data_batch import GraphDataBatch
from api.websocket.interfaces.graph.responses.graph_listening_mode import GraphListeningMode
from api.websocket.interfaces.websocket_response import WebSocketResponse
from logger import Logger


class GraphController(WebSocketController):
    """
    Controller handling graph manipulation / gathering
    """

    logger = Logger.get_logger("Graph Controller")

    def get_namespace(self):
        return "/graph"

    def send_graph(self, response: dict):
        """
        Send a named graph to the client
        :param response: Response containing the listening mode
        :return:
        """
        formatted_response = WebSocketResponse.convert_dict(response)
        listening_mode: GraphListeningMode = GraphListeningMode.convert_dict(formatted_response.get_data())

        try:
            # Iterate over batches
            for i in range(0, 100):
                nodes = [GraphNode(i, 5, "Node num {0}".format(i), "#000000")]
                edges = []

                batch = GraphDataBatch(nodes, edges)
                emit('batch_received', WebSocketResponse("graph_batch", batch, []).repr_json())

        except Exception as e:
            self.logger.error("Failed to send the graph '{0}'.".format(listening_mode.name), e)
            return WebSocketResponse("graph_by_name", None, ["Internal error: Failed to get graph."]).repr_json()

    def get_graph(self, response: dict):
        """
        Get the status of the Web Socket server
        :return:
        """
        formatted_response = WebSocketResponse.convert_dict(response)
        graph_by_name: GetGraphByName = GetGraphByName(formatted_response.get_data())

        try:
            graph_characteristics: GraphCharacteristics = GraphCharacteristics(graph_by_name.name, "test", 100, 10000)
            return WebSocketResponse("graph_by_name", graph_characteristics, []).repr_json()
        except Exception as e:
            self.logger.error("Failed to get the graph '{0}'.".format(graph_by_name), e)
            return WebSocketResponse("graph_by_name", None, ["Internal error: Failed to get graph."]).repr_json()


    def register(self):
        self.application.on_event("get_graph", self.get_graph, self.get_namespace())
        self.application.on_event("send_graph", self.send_graph, self.get_namespace())
