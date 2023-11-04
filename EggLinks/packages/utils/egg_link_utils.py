import pathlib
from datetime import datetime
import struct
from .constants import *

# returns formatted datetime for timestamps
def getCurrentDateTime():
    currentDateTime = datetime.now()
    currentDateTime = currentDateTime.strftime(TIMESTAMP_FORMAT)
    return currentDateTime

#TODO make this an inline func.
def truncateFloat(flt):
    return float(f'{flt:.2f}')

# function to convert byte array to float value and truncate to 2 decimal places.
def bytes_to_float(bytes: bytearray, useLittleEndian = True):
    if useLittleEndian:
        byteTuple = struct.unpack('>f', bytes)
    else:
        byteTuple = struct.unpack('f', bytes)

    # truncatedFloat = float(f'{byteTuple[0]:.2f}')
    truncatedFloat = truncateFloat(byteTuple[0])
    return truncatedFloat

def checkLogFile(logFileName):
    file = pathlib.Path(__file__).resolve().parents[1]
    logDir = file.joinpath('logs')
    if logDir.exists() == False:
        # _logger.warn("Log Directory Not found. creating 'logs' directory.")
        logDir.mkdir()
    # else:
    #     _logger.info("-- log dir exists --")

    return logDir.joinpath(logFileName)

def formatReadings(readings, numSamples=None):
    averages = Converters.calcAverage(readings)
    # print(averages)
    data = {
        "Temperature": [averages[TEMP_LABEL]],
        "Humidity": [averages[HUM_LABEL]],
        "Pressure": [averages[PRESS_LABEL]],
        "Altitude": [averages[ALT_LABEL]],
        "TemperatureSamples": [readings[TEMP_LABEL]],
        "HumiditySamples": [readings[HUM_LABEL]],
        "PressureSamples": [readings[PRESS_LABEL]],
        "AltitudeSamples": [readings[ALT_LABEL]]
    }
    # print(f"data[0]: {list(data.keys())[0]}")

    if numSamples is not None:
        updict = {"Timestamp": getCurrentDateTime(), "SampleCount": numSamples}
        newData = {**updict, **data}
        return newData
    else:
        updict = {"Timestamp": getCurrentDateTime()}
        newData = {**updict, **data}
        return newData

class Converters:


    # calculates average of all samples taken from bme sensor
    # and returns a dict containing averages of all readings
    @staticmethod
    def calcAverage(bmeDict):
        for key in bmeDict.keys():
            num = sum(bmeDict[key])
            if key == "Temperature":
                avgTemp = truncateFloat(num / 3)
            elif key == "Humidity":
                avgHum = truncateFloat(num / 3)
            elif key == "Pressure":
                avgPress = truncateFloat(num / 3)
            elif key == "Altitude":
                avgAlt = truncateFloat(num / 3)

        avgDict = {
            "Label": "Averages",
            "Temperature": avgTemp,
            "Humidity": avgHum,
            "Pressure": avgPress,
            "Altitude": avgAlt
        }

        return avgDict
