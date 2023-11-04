
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

from ..utils.file_utils import LogHandler, EggConfig
from ..utils.egg_link_utils import parseEnvironmentReading, formatReadings

class SampleEnvironment():
    
    def __init__(self):
        conf = EggConfig()

        self.eggConfig = conf.getEggConfig(name="LEDCallback")
        self.charBme = conf.getEggCharacterisitc(self.eggConfig, 'bme')
        self.charLed = conf.getEggCharacterisitc(self.eggConfig, 'led')

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
        print(f"Scanning for device: {self.eggConfig.get('address')}")

        device = await BleakScanner.find_device_by_address(self.eggConfig.get('address'))

        if device is None:
            print(f"Could not find device with address: {self.eggConfig.get('address')}")
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
                    if char.uuid == self.charBme:
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

        r = formatReadings(self.bmeReadings, self.samplesTaken)
        # print(f"\n--formatted data--\n{r}")
        return r

        # LogHandler().writeLog(self.samplesTaken, self.bmeReadings)
        # return self.bmeReadings

def run_sampling():
    return asyncio.run(SampleEnvironment().connect_and_sample())