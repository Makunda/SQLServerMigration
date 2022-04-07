from api.flask_app import flask_application
from logger import Logger
from migration.orchestrator import Orchestrator
from utils.configuration.port_configuration import PortConfiguration

configuration = PortConfiguration()

def main():
    """
    Main function
    :return: None
    """
    # Logger
    logger = Logger.get_logger("Main Logic")
    logger.info("Starting program...")

    orchestrator = Orchestrator()
    orchestrator.launch()


if __name__ == '__main__':
    flask_application.run(host="0.0.0.0", port=configuration.get_rest_api_port())
    #main()
