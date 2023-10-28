import csv
import pandas as pd
from datetime import datetime


from egg_link_utils import setUtilPackagePath
setUtilPackagePath()
from utils.Device_Utils import calcAverage


def writeToFile():
    labels = ["SN", "Movie", "Protagonist"]
    entry1 = [1, "LOTR", "Frodo Baggins"]
    entry2 = [2, "HP", "Harry Potter"]

    with open('testcsv.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        data = []
        data.append(labels)
        data.append(entry1)
        data.append(entry2)

        writer.writerows(data)
        file.close()


def readFile():
    with open('testcsv.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
    file.close()

def readIntoDict():
    with open('testcsv.csv', 'r') as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
            print(dict(row))
    file.close()

def writeDataframe():
    # df = pd.DataFrame([['Jack', 24], ['Rose', 22]], columns = ['Name', 'Age'])
    # df.to_csv('person.csv')

    data = {
        "calories": [420, 380, 390],
        "duration": [50, 40, 45]
        }
    df = pd.DataFrame(data)

    print(df.loc[[0, 1]])

def readDataframe():
    df = pd.read_csv('data.csv')
    print(df.to_string())

    # print(df.head(10))
    # print(df.tail())
    # print(df.info())

    # print(df.loc[df["Calories"] == 215.2, "Pulse"].values)
    # print(df.loc[df[0] == 15, "Pulse"].values)
    indicies = df.loc[df["Pulse"] == 98]
    print(indicies.index.tolist())
    list(map(lambda x: print(df.iloc[x]), indicies.index.tolist()))
    print(f"--\n{df.iloc[0]}")

# get list of indexes where date is >= a given date
    # highest = df.loc[df["Calories"] ]
    highests = df.loc[df["Calories"] >= 900]
    hIndicies = highests.index.tolist()
    # hIndicies.sort()
    print(highests)
# get highest index (most recent date)
    print(max(hIndicies))
    # print(min(hIndicies))

# do same with the oldest log date,
#  and use the lowest index to return df between lowest index and highest

    b = df.query('Calories >= 400 & Calories <= 1000')
    print(f"b = \n{b}")

def readJson():
    df = pd.read_json('samplejson.json')
    print(df.to_string())

# returns formatted datetime for timestamps
def getCurrentDateTime():
    currentDateTime = datetime.now()
    currentDateTime = currentDateTime.strftime("%m/%d/%Y-%H:%M:%S")
    return currentDateTime

def printEnvReadings(data):

    samplesDict = {"time_stamp": getCurrentDateTime(), 
                   "readings": []}
    
    readingDict = {"Label": "bme-samples", "samples_taken": 3}
    readingDict.update(data)
    samplesDict["readings"].append(readingDict)

    avg = calcAverage(data)

    samplesDict["readings"].append(avg)


    df = pd.DataFrame(samplesDict)
    print(df.to_string())


# writeToFile()
# readFile()
# readIntoDict()

# writeDataframe()
# readDataframe()
# readJson()