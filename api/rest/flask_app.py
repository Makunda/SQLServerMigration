
from flask import Flask
from flask_cors import CORS, cross_origin

# Create a new Application
from api.rest.controllers.api_controller import api_controller
from logger import Logger

logger = Logger.get_logger("Flask Application")

flask_application = Flask(__name__)
flask_application.debug = True

# Apply a non restrictive policy
cors = CORS(flask_application, resources={r"/*": {"origins": "*"}})

# Register the Blueprints / Controllers
flask_application.register_blueprint(api_controller)


def run_webserver(host: str, port: int) -> None:
    """
    Run websocket
    :param host:  Host of the webserver
    :param port: Port to use
    :return:
    """
    logger.info("Launching the Flask WebServer on {0}:{1}".format(host, port))
    flask_application.run(host=host, port=port)