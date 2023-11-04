import pathlib
import sys
from datetime import datetime
import struct
from .constants import *

def setUtilPackagePath():
    file = pathlib.Path(__file__).resolve().parents[1]
    sys.path.append(str(file))

# returns formatted datetime for timestamps
def getCurrentDateTime():
    currentDateTime = datetime.now()
    currentDateTime = currentDateTime.strftime("%m/%d/%Y-%H:%M:%S")
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

# returns a dict of environment readings from BME sensor
def parseEnvironmentReading(data: bytearray, dict):
    tempReading = bytearray()
    humReading = bytearray()
    pressReading = bytearray()
    altReading = bytearray()

    iterator = 0

    # set individual sensor reading data into 4 seperate byte arrays
    for val in data:
        if iterator <= 3:
            tempReading.append(val)
        elif iterator > 3 and iterator <= 7:
            humReading.append(val)
        elif iterator > 7 and iterator <= 11:
            pressReading.append(val)
        elif iterator > 11 and iterator <= 15:
            altReading.append(val)
        
        iterator += 1

    environmentSampleDict = {"Temperature": bytes_to_float(tempReading),
                             "Humidity": bytes_to_float(humReading),
                             "Pressure": bytes_to_float(pressReading),
                             "Altitude": bytes_to_float(altReading)}

    for key in environmentSampleDict.keys():
        dict[key].append(environmentSampleDict[key])

    tempReading.clear()
    humReading.clear()
    pressReading.clear()
    altReading.clear()

    return environmentSampleDict

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
        updict = {"SampleCount": numSamples}
        newData = {**updict, **data}
        return newData
    else:
        return data

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



class Log:

    @staticmethod
    def checkLogFile():
        file = pathlib.Path(__file__).resolve().parents[1]
        logDir = file.joinpath('logs')
        if logDir.exists() == False:
            print("--- Log Directory Not found. creating 'logs' directory. ---")
            logDir.mkdir()
        else:
            print("-- log dir exists --")

        return logDir.joinpath(ENV_LOG_FILE_NAME)
