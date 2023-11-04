import logging
from .egg_link_utils import getCurrentDateTime

#TODO make this better.
# make one msg method that all other msg methods can inherit from
class Logger(object):

    _initialized = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            print("creating new logger class")
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        #TODO add stuff for getting filename
        logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

        if self._initialized == False:
            logging.info(f"STARTING LOG FOR SESSION {getCurrentDateTime()}")
            self._initialized = True

    def debug(self, msg: str):
        logging.debug(msg)

    def info(self, msg: str):
        logging.info(msg)

    def error(self, msg: str):
        logging.error(msg)

    def critical(self, msg: str):
        logging.critical(msg)