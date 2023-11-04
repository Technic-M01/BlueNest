import pandas as pd
import json
import pathlib

from .constants import *
from .base_logger import Logger
from .egg_link_utils import checkLogFile

_logger = Logger()

class EggConfig():
    def __init__(self):
        pass

    def getConfigFilePath(self):
        file = pathlib.Path(__file__).resolve().parents[2]
        config = file.joinpath('egg_configs.json')
        return config

    def checkConfigFile(self):
        config = self.getConfigFilePath()
        return config.exists()
    
    def getEggConfig(self, name=None, address=None):
        fileOk = self.checkConfigFile()

        if fileOk == False:
            _logger.error("no config file found")
            return
        else:
            config = self.getConfigFilePath()
            with open(config, 'r') as file:
                data = json.load(file)
                for key in data: # data var is list of devices
                    device = data[key]
                    # print(f"key: {key} value: {data[key]}")
                    if name is not None and name == device.get('name'):
                        _logger.info(f"device from name {name}: {device}")
                        return device
                    elif address is not None and address == device.get('address'):
                        _logger.info(f"device from address {address}: {device}")
                        return device
                
                _logger.error("No device found matching provided parameters")
            file.close()

    # eggConfig is a dict of a device returned from getEggConfig
    def getEggCharacterisitc(self, eggConfig, characteristicName):
        char = eggConfig["characteristics"].get(characteristicName)
        _logger.info(f"char name: {characteristicName} uuid: {char}")
        return char

#TODO make into a singleton
class LogHandler():

    def __init__(self):
        pass

    def writeLogFile(self, data, logFileName):
        df = pd.DataFrame(data)

        #path to log file
        logFile = checkLogFile(logFileName) 
        _logger.info(f"log file path: {logFile}")
        if logFile.exists():
            df.to_csv(logFile, header=False, mode='a')
        else:
            logFile.touch()
            df.to_csv(logFile)

        _logger.info(f"entry written to {logFileName} :\n{df.to_string()}")

        # new_df = pd.read_csv(logFile)
        # _logger.info(f" --- read from csv ---\n{new_df.to_string()}")

    # #TODO add handling for if file doesn't exist
    # @staticmethod
    # def getLatestLog():
    #         logFile = Log.checkLogFile()

    #         df = pd.read_csv(logFile)
    #         latest = df.iloc[-1]
    #         logDict = latest.to_dict()
    #         #pop the log number item passed in by the dataframe
    #         logDict.pop(list(logDict.keys())[0])
    #         return logDict 
