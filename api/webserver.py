from api.websocket.websocket_server import websockets_server, run_websockets_server


def run_webserver(host: str, port: int):
    """
    Launch the web server
    :param host: Host of the sever
    :param port: Port of the server
    :return:
    """
    run_websockets_server(host, port)
