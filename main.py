from logger import Logger


def main():
    """
    Main function
    :return: None
    """
    # Logger
    logger = Logger.get_logger("Main Logic")
    logger.info("Starting program...")


if __name__ == '__main__':
    main()
