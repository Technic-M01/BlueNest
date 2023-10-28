import pandas as pd
from datetime import datetime
from egg_link_utils import setUtilPackagePath
setUtilPackagePath()
from utils.Device_Utils import calcAverage

import pathlib

# returns formatted datetime for timestamps
def getCurrentDateTime():
    currentDateTime = datetime.now()
    currentDateTime = currentDateTime.strftime("%m/%d/%Y-%H:%M:%S")
    return currentDateTime

TEMP_LABEL = "Temperature"
HUM_LABEL = "Humidity"
PRESS_LABEL = "Pressure"
ALT_LABEL = "Altitude"

ENV_LOG_FILE_NAME = "envreadings.csv"

def checkLogFile():
    file = pathlib.Path(__file__).resolve().parents[1]
    logDir = file.joinpath('logs')
    if logDir.exists() == False:
        print("--- Log Directory Not found. creating 'logs' directory. ---")
        logDir.mkdir()
    else:
        print("-- log dir exists --")

    return logDir.joinpath(ENV_LOG_FILE_NAME)


def writeData(numSamples, readings):

    averages = calcAverage(readings)

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
    
    logFile = checkLogFile() 
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
