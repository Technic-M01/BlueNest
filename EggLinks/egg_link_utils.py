import pathlib
import sys
from datetime import datetime

ENV_LOG_FILE_NAME = "envreadings.csv"


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
