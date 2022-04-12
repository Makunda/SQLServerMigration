import asyncio

from api.webserver import run_webserver
from logger import Logger
from migration.orchestrator import Orchestrator
from utils.configuration.port_configuration import PortConfiguration

configuration = PortConfiguration()

HOST = "0.0.0.0"
PORT_WEB = configuration.get_rest_api_port()
PORT_WEBSOCKETS = configuration.get_websockets_port()


async def main():
    """
    Main function
    :return: None
    """
    # Logger
    logger = Logger.get_logger("Main Logic")
    logger.info("Starting program...")

    # Launch demons
    orchestrator = Orchestrator()
    # orchestrator.launch()

    # Launch web servers
    run_webserver(HOST, PORT_WEB)


if __name__ == '__main__':
    asyncio.run(main())
