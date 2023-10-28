
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

from egg_link_utils import setUtilPackagePath
setUtilPackagePath()
from utils.Device_Utils import DeviceInformation, parseEnvironmentReading, JsonHelper, storeData

from csv_test import printEnvReadings
from log_utils import writeData

devInfo = DeviceInformation()
charBme = devInfo.MyCharacteristics.BME_CHARACTERISTIC
charLed = devInfo.MyCharacteristics.LED_CHARACTERISTIC

jHelper = JsonHelper()
samplesTaken = 0

# jHelper.showTimestampEntries()

bmeReadings = {
    "Temperature": [],
    "Humidity": [],
    "Pressure": [],
    "Altitude": []
}

def notification_handler(characterisitc: BleakGATTCharacteristic, data: bytearray):
    print(f"BME Notification: {characterisitc.descriptors}, data: {data}")

    envReading = parseEnvironmentReading(data, bmeReadings)
    print(envReading)

    global samplesTaken
    samplesTaken += 1

async def wait_for_samples():
    keepAlive = True
    while keepAlive:
        global samplesTaken
        if samplesTaken >= 3:
            print(f">>> Took {samplesTaken} samples <<<")
            keepAlive = False
        await asyncio.sleep(1.0)


async def main():
    # devInfo.showDetails()
    print(f"Scanning for device: {devInfo.ADDRESS}")

    device = await BleakScanner.find_device_by_address(devInfo.ADDRESS)

    if device is None:
        print(f"Could not find device with address: {devInfo.ADDRESS}")
        return
    else:
        print(f"Connecting to device: {device.name} - {device.address}")

    # Connect to the Bluetooth device
    async with BleakClient(device) as client:
        # Read, write, or do something with the connection

        notifyChar = BleakGATTCharacteristic

        if client.is_connected:
            print("device connected.")
            # print(device.details)
        else:
            print("device NOT connected.")

        for service in client.services:
            for char in service.characteristics:
                if char.uuid == devInfo.getCharacteristicUuid(charBme):
                    print("BME characterisitc found")

                    if "notify" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            print(f"[BME Char] {char} - {char.properties}, Value: {value}")
                            await client.start_notify(char, notification_handler)
                            notifyChar = char
                        except Exception as e:
                            print(f"[BME Char] {char} - {char.properties}, ERROR: {e}")


        await wait_for_samples()

        await client.stop_notify(notifyChar)
        print(f"Disconnecting from device: {device.name} - {device.address}")

    # storeData(samplesTaken, bmeReadings)
    # printEnvReadings(bmeReadings)
    writeData(samplesTaken, bmeReadings)

asyncio.run(main())