import logging


def setup_logger() -> None:
    """
    Configures our basic logger for running scripts

    """
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    logger.propagate = True

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    else:
        for handler in logger.handlers:
            handler.setFormatter(formatter)


setup_logger()
