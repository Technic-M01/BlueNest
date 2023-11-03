
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

from ..link_utils import log_utils
from ..devTests import csv_test
from ..link_utils.Device_Utils import DeviceInformation, parseEnvironmentReading, JsonHelper

class SampleEnvironment():
    
    def __init__(self):
        self.devInfo = DeviceInformation()
        self.charBme = self.devInfo.MyCharacteristics.BME_CHARACTERISTIC
        self.charLed = self.devInfo.MyCharacteristics.LED_CHARACTERISTIC
        self.bmeReadings = {
            "Temperature": [],
            "Humidity": [],
            "Pressure": [],
            "Altitude": []
        }
        self.samplesTaken = 0


    def __notification_handler(self, characterisitc: BleakGATTCharacteristic, data: bytearray):
        print(f"BME Notification: {characterisitc.descriptors}, data: {data}")

        envReading = parseEnvironmentReading(data, self.bmeReadings)
        print(envReading)
        self.samplesTaken += 1

    async def __wait_for_samples(self):
        keepAlive = True
        while keepAlive:
            if self.samplesTaken >= 3:
                print(f">>> Took {self.samplesTaken} samples <<<")
                keepAlive = False
            await asyncio.sleep(1.0)

    async def connect_and_sample(self):
        # devInfo.showDetails()
        print(f"Scanning for device: {self.devInfo.ADDRESS}")

        device = await BleakScanner.find_device_by_address(self.devInfo.ADDRESS)

        if device is None:
            print(f"Could not find device with address: {self.devInfo.ADDRESS}")
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
                    if char.uuid == self.devInfo.getCharacteristicUuid(self.charBme):
                        print("BME characterisitc found")

                        if "notify" in char.properties:
                            try:
                                value = await client.read_gatt_char(char.uuid)
                                print(f"[BME Char] {char} - {char.properties}, Value: {value}")
                                await client.start_notify(char, self.__notification_handler)
                                notifyChar = char
                            except Exception as e:
                                print(f"[BME Char] {char} - {char.properties}, ERROR: {e}")


            await self.__wait_for_samples()

            await client.stop_notify(notifyChar)
            print(f"Disconnecting from device: {device.name} - {device.address}")

        # csv_test.printEnvReadings(bmeReadings)
        # printEnvReadings(bmeReadings)
        log_utils.writeData(self.samplesTaken, self.bmeReadings)

def run_sampling():
    asyncio.run(SampleEnvironment().connect_and_sample())