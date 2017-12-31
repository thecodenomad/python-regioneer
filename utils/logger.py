import logging

LOG_LOCATION = "/tmp/regioneer.log"
REGIONEER = "REGIONEER"


def get_logger(logger=REGIONEER):
    """ Get the Regioneer Logger """

    log = logging.getLogger(name=logger)
    log.setLevel(logging.DEBUG)

    if not log.handlers:
        handler = logging.FileHandler(LOG_LOCATION)
        formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)

    log.info("Logging established.")

    return log

