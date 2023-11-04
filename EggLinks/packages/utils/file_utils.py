import pandas as pd
import json
import pathlib

from .constants import *
from .base_logger import Logger

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
                        # print(f"device from name {name}: {device}")
                        _logger.info(f"device from name {name}: {device}")
                        return device
                    elif address is not None and address == device.get('address'):
                        # print(f"device from address {address}: {device}")
                        _logger.info(f"device from address {address}: {device}")
                        return device
                
                _logger.error("No device found matching provided parameters")
            file.close()

    # eggConfig is a dict of a device returned from getEggConfig
    def getEggCharacterisitc(self, eggConfig, characteristicName):
        char = eggConfig["characteristics"].get(characteristicName)
        # print(f"char name: {characteristicName} uuid: {char}")
        _logger.info(f"char name: {characteristicName} uuid: {char}")
        return char

class LogHandler():

    def __init__(self):
        pass

    def checkLogFile(self, logFileName):
        file = pathlib.Path(__file__).resolve().parents[1]
        logDir = file.joinpath('logs')
        if logDir.exists() == False:
            # print("--- Log Directory Not found. creating 'logs' directory. ---")
            _logger.warn("Log Directory Not found. creating 'logs' directory.")
            logDir.mkdir()
        else:
            _logger.info("-- log dir exists --")

        return logDir.joinpath(logFileName)



    def writeLogFile(self, data, logFileName):
        df = pd.DataFrame(data)

        _logger.info(df.to_string())
        
        logFile = self.checkLogFile(logFileName) 
        # print(f"log file: {logFile}")
        _logger.info(f"log file: {logFile}")
        if logFile.exists():
            # print(f"log file: {logFileName} exists.")
            _logger.info(f"log file: {logFileName} exists.")
            df.to_csv(logFile, header=False, mode='a')
        else:
            logFile.touch()
            # print(f"log file: {logFileName} doesnt exist.")
            _logger.info(f"log file: {logFileName} doesnt exist.")
            df.to_csv(logFile)

        new_df = pd.read_csv(logFile)
        # print(f" --- read from csv ---\n{new_df.to_string()}")
        _logger.info(f" --- read from csv ---\n{new_df.to_string()}")

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
