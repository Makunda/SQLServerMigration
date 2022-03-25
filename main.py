from logger import Logger
from migration.orchestrator import Orchestrator


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
    main()
