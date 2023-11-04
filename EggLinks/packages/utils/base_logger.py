import logging
from .egg_link_utils import checkLogFile
from .constants import LOGGING_FILE_NAME

#TODO make this better.
# make one msg method that all other msg methods can inherit from
class Logger(object):

    _initialized = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    #TODO figure out why init is called more than once
    def __init__(self):
        if self._initialized == False:

            file = checkLogFile(LOGGING_FILE_NAME)

            self.log = logging.getLogger(__name__)
            self.log.setLevel(logging.INFO)

            handler = logging.FileHandler(file)
            handler.setLevel(logging.INFO)
            format = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            handler.setFormatter(format)
            
            stream = logging.StreamHandler()
            stream.setLevel(logging.INFO)
            streamFormat = logging.Formatter("%(levelname)s %(message)s")
            stream.setFormatter(streamFormat)

            self.log.addHandler(handler)
            self.log.addHandler(stream)

            self.log.info(f"----- STARTING LOG SESSION -----")
            self._initialized = True

    def debug(self, msg: str):
        self.log.debug(msg)

    def info(self, msg: str):
        self.log.info(msg)

    def error(self, msg: str):
        self.log.error(msg)

    def critical(self, msg: str):
        self.log.critical(msg)