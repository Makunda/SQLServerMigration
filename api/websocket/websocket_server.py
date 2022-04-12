from flask import Flask
from flask_socketio import SocketIO

from api.websocket.controllers.websockets.graph.graph_controller import GraphController
from api.websocket.controllers.websockets.healthcheck.status_controller import StatusController
from logger import Logger
from api.rest.flask_app import flask_application

logger = Logger.get_logger("WebSocket Server")
websockets_server = SocketIO(flask_application, cors_allowed_origins="*")


def run_websockets_server(host: str, port: int) -> None:
    """
    Run websocket
    :param host:  Host of the webserver
    :param port: Port to use
    :return:
    """
    logger.info("Launching the Flask Web Socket on {0}:{1}".format(host, port))

    # Declare and register controllers
    StatusController(websockets_server).register()
    GraphController(websockets_server).register()

    websockets_server.run(app=flask_application, host=host, port=port)
