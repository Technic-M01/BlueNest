import pandas as pd
import json
import pathlib

from .egg_link_utils import getCurrentDateTime
from .egg_link_utils import Log, Converters

TEMP_LABEL = "Temperature"
HUM_LABEL = "Humidity"
PRESS_LABEL = "Pressure"
ALT_LABEL = "Altitude"

ENV_LOG_FILE_NAME = "envreadings.csv"

class EggConfig():
    def __init__(self):
        pass

    def getConfigFilePath(self):
        file = pathlib.Path(__file__).resolve().parents[1]
        config = file.joinpath('egg_configs.json')
        return config

    def checkConfigFile(self):
        config = self.getConfigFilePath()
        return config.exists()
    
    def getEggConfig(self, name=None, address=None):
        fileOk = self.checkConfigFile()

        if fileOk == False:
            print("no config file found")
            return
        else:
            config = self.getConfigFilePath()
            with open(config, 'r') as file:
                data = json.load(file)
                for key in data: # data var is list of devices
                    device = data[key]
                    # print(f"key: {key} value: {data[key]}")
                    if name is not None and name == device.get('name'):
                        print(f"device from name {name}: {device}")
                        return device
                    elif address is not None and address == device.get('address'):
                        print(f"device from address {address}: {device}")
                        return device
                
                print("No device found matching provided parameters")
            file.close()

    # eggConfig is a dict of a device returned from getEggConfig
    def getEggCharacterisitc(self, eggConfig, characteristicName):
        char = eggConfig["characteristics"].get(characteristicName)
        print(f"char name: {characteristicName} uuid: {char}")
        return char

class LogHandler():

    def __init__(self):
        pass

    def checkLogFile(self):
        file = pathlib.Path(__file__).resolve().parents[1]
        logDir = file.joinpath('logs')
        if logDir.exists() == False:
            print("--- Log Directory Not found. creating 'logs' directory. ---")
            logDir.mkdir()
        else:
            print("-- log dir exists --")

        return logDir.joinpath(ENV_LOG_FILE_NAME)


    def writeLog(self, numSamples, readings):

        averages = Converters.calcAverage(readings)

        print(readings[TEMP_LABEL])
        print(averages)

        data = {
            "Timestamp": getCurrentDateTime(),
            "SampleCount": numSamples,
            "Temperature": [averages[TEMP_LABEL]],
            "Humidity": [averages[HUM_LABEL]],
            "Pressure": [averages[PRESS_LABEL]],
            "Altitude": [averages[ALT_LABEL]],
            "TemperatureSamples": [readings[TEMP_LABEL]],
            "HumiditySamples": [readings[HUM_LABEL]],
            "PressureSamples": [readings[PRESS_LABEL]],
            "AltitudeSamples": [readings[ALT_LABEL]]
        }

        df = pd.DataFrame(data)

        print(df.to_string())
        
        logFile = Log.checkLogFile() 
        print(f"log file: {logFile}")
        if logFile.exists():
            print(f"log file: {ENV_LOG_FILE_NAME} exists.")
            df.to_csv(logFile, header=False, mode='a')
        else:
            logFile.touch()
            print(f"log file: {ENV_LOG_FILE_NAME} doesnt exist.")
            df.to_csv(logFile)

        new_df = pd.read_csv(logFile)
        print(f" --- read from csv ---\n{new_df.to_string()}")
