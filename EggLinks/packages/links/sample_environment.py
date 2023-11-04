
import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

from ..utils.file_utils import LogHandler, EggConfig
from ..utils.egg_link_utils import parseEnvironmentReading, formatReadings
from ..utils.constants import *

from ..utils.base_logger import Logger

_logger = Logger()

class SampleEnvironment():
    
    def __init__(self):
        conf = EggConfig()

        self.eggConfig = conf.getEggConfig(name="LEDCallback")
        self.charBme = conf.getEggCharacterisitc(self.eggConfig, 'bme')
        self.charLed = conf.getEggCharacterisitc(self.eggConfig, 'led')

        # self.logger = Logger()

        self.bmeReadings = {
            "Temperature": [],
            "Humidity": [],
            "Pressure": [],
            "Altitude": []
        }
        self.samplesTaken = 0


    def __notification_handler(self, characterisitc: BleakGATTCharacteristic, data: bytearray):
        # print(f"BME Notification: data: {data}")

        envReading = parseEnvironmentReading(data, self.bmeReadings)
        _logger.info(f"BME Notification\n\tdata: {data} - parsed data: {envReading}")

        # _logger.info(envReading)
        self.samplesTaken += 1

    async def __wait_for_samples(self):
        keepAlive = True
        while keepAlive:
            if self.samplesTaken >= 3:
                _logger.info(f"Sampling complete. Took {self.samplesTaken} samples.")
                keepAlive = False
            await asyncio.sleep(1.0)

    async def connect_and_sample(self):
        # devInfo.showDetails()
        _logger.info(f"Scanning for device: {self.eggConfig.get('address')}")

        device = await BleakScanner.find_device_by_address(self.eggConfig.get('address'))

        if device is None:
            _logger.warn(f"Could not find device with address: {self.eggConfig.get('address')}")
            return
        else:
            _logger.info(f"Connecting to device: {device.name} - {device.address}")

        # Connect to the Bluetooth device
        async with BleakClient(device) as client:
            # Read, write, or do something with the connection

            notifyChar = BleakGATTCharacteristic

            if client.is_connected:
                _logger.info("device connected.")
                # print(device.details)
            else:
                _logger.warn("device NOT connected.")

            for service in client.services:
                for char in service.characteristics:
                    if char.uuid == self.charBme:
                        _logger.info("BME characterisitc found")

                        if "notify" in char.properties:
                            try:
                                value = await client.read_gatt_char(char.uuid)
                                _logger.info(f"[BME Char] {char} - {char.properties}, Value: {value}")
                                await client.start_notify(char, self.__notification_handler)
                                notifyChar = char
                            except Exception as e:
                                _logger.error(f"[BME Char] {char} - {char.properties}, ERROR: {e}")


            await self.__wait_for_samples()

            await client.stop_notify(notifyChar)
            _logger.info(f"Disconnecting from device: {device.name} - {device.address}")

        # printEnvReadings(bmeReadings)

        LogHandler().writeLogFile(formatReadings(self.bmeReadings, self.samplesTaken), ENV_LOG_FILE_NAME)