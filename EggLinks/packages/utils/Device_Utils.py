from enum import Enum
from datetime import datetime
import struct
import json
import os

_JSON_FILENAME = "samplejson.json"

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