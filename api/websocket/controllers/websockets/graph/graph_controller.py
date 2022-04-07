from api.flask_app import socket_io

# Get graph service

@socket_io.on('graph_request', namespace='/graph')
def get_graph(data):
    """
    Get and send the graph
    :param data: Data containing the name of the graph
    :return: None
    """
    # Get the objects and links

    # Form the graph

    # Send the response
