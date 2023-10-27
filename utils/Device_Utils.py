from enum import Enum
from datetime import datetime
import struct
import json
import os
import pathlib

_JSON_FILENAME = "samplejson.json"

class DeviceInformation:
    ADDRESS = "8E:D1:62:42:A4:0D"

    class MyCharacteristics(Enum):
        LED_CHARACTERISTIC = "19b10001-e8f2-537e-4f6c-d104768a1214"
        BME_CHARACTERISTIC = "19b10005-e8f2-537e-4f6c-d104768a1214"

    def showDetails(self):
        for c in self.MyCharacteristics:
            print(f"Characteristic: {c.name} - {c.value}")        

    def getCharacteristicUuid(self, characteristic: MyCharacteristics):
        return characteristic.value

def getRootPackagePath():
    return pathlib.Path(__file__).resolve().parents[1]


def logDirExists():
    file = pathlib.Path(__file__).resolve().parents[1]
    logDir = file.joinpath('logs')
    if logDir.exists() == False:
        print("--- Log Directory Not found. creating 'logs' directory. ---")
        logDir.mkdir()
        return False
    else:
        return True


#TODO make this an inline func.
def truncateFloat(flt):
    return float(f'{flt:.2f}')

# returns formatted datetime for timestamps
def getCurrentDateTime():
    currentDateTime = datetime.now()
    currentDateTime = currentDateTime.strftime("%m/%d/%Y-%H:%M:%S")
    return currentDateTime

#TODO refactor JsonHelper class so writeDataToFile is static method
def storeData(numSamples, bmeDict):
    samplesDict = {"time_stamp": getCurrentDateTime(), 
                   "readings": []}
    
    readingDict = {"Label": "bme-samples", "samples_taken": numSamples}
    readingDict.update(bmeDict)
    samplesDict["readings"].append(readingDict)

    jHelper = JsonHelper()

    jHelper.writeDataToFile(samplesDict, bmeDict)



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

# calculates average of all samples taken from bme sensor
# and returns a dict containing averages of all readings
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

class JsonHelper:

    def __init__(self):
        self.filename = _JSON_FILENAME
        
        pass

    @staticmethod
    def searchJson(key):

        with open("samplejson.json", 'r') as file:
            data = json.load(file)

        if key in data:
            print(f"key: {key} is present")
            print(data[key])
            return True
        else:
            print(f"key: {key} is NOT in data")
            return False
        


    def writeDataToFile(self, samples, bmeDict):
        averages = calcAverage(bmeDict)
        samples["readings"].append(averages)

        logDirFound = logDirExists()
        logFile = getRootPackagePath().joinpath('logs', self.filename)

        # if os.path.isfile(self.filename):
        if logFile.exists():
            print("file exists")
            with open(logFile, 'r') as r:
                data = json.load(r)

            data["samples"].append(samples)
        else:
            logFile.touch()
            print("file doesnt exist")
            newRootDict = {"samples": []}
            newRootDict["samples"].append(samples)
            data = newRootDict


        with open(logFile, "w") as outfile:
            outfile.write(json.dumps(data, indent = 4))
        outfile.close()

    def showTimestampEntries(self):
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as r:
                data = json.load(r)
            r.close()

            for member in data["samples"]:
                print(member)
                for label in member:
                    if label == "time_stamp":
                        print(f"time_stamp: {member[label]}")

    # if only first log is provided, only get entries for that date
    def getLogsFromTimestamp(self, firstLog, lastLog = None):
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as r:
                data = json.load(r)
            r.close()

            # iterate through data
            # use the last log and match to most recent log
            # keep iterating until date matches last log
            logs = []
            firstLogFound = False

            for member in data["samples"]:
                # print(member)
                for label in member:
                    # print(label)
                    if label == "time_stamp":

                        if lastLog is not None:
                            #add log to list
                            dateMatches = lastLog in str(member[label])
                            print(f"{member[label]} dateMatches: {dateMatches}")


                        # break loop if first log is retrieved

                        # will overwrite log entries if log date is the same
                        dateMatches = firstLog in str(member[label])
                        print(f"{member[label]} dateMatches: {dateMatches}")
                        if dateMatches:
                            firstLogFound = True
                            logs.append(member)
                            print(f"updated log: {logs}")
                        
                        if firstLogFound:
                            # break loop, dont need to iterate over earlier logs
                            print("earliest log found")
                            break
                
                if firstLogFound:
                    break


            print(f"Logs Retrieved:\n{logs}")
            

            for member in data["samples"]:
                # print(member)
                for label in member:
                    if label == "time_stamp":
                        print(f"time_stamp: {member[label]}")