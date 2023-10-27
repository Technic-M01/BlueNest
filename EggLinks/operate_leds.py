# connect.py

import struct
import asyncio
from aioconsole import ainput
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from Device_Utils import DeviceInformation, parseEnvironmentReading

devInfo = DeviceInformation()
charBme = devInfo.MyCharacteristics.BME_CHARACTERISTIC
charLed = devInfo.MyCharacteristics.LED_CHARACTERISTIC

bmeChar = BleakGATTCharacteristic

tempReading = bytearray()
humReading = bytearray()
pressReading = bytearray()
altReading = bytearray()

async def get_input():
    print("enter 1 to disconnect")

    response = await ainput("> ")

    response = int(response.strip())

    return response

async def set_led():
    print("enter 1 to turn on led, 0 to turn off")
    response = await ainput("> ")

    response = int(response.strip())

    return response

def notification_handler(characterisitc: BleakGATTCharacteristic, data: bytearray):
    print(f"BME Notification: {characterisitc.descriptors}, data: {data}")

    envReading = parseEnvironmentReading(data)
    print(envReading)

async def main():
    devInfo.showDetails()

    # Connect to the Bluetooth device
    async with BleakClient(devInfo.ADDRESS) as client:
        # Read, write, or do something with the connection
        ...
        print(client.is_connected) # prints True or False

        for service in client.services:
            for char in service.characteristics:
                if char.uuid == devInfo.getCharacteristicUuid(charBme):
                    print("BME characterisitc found")

                    if "notify" in char.properties:
                        try:
                            value = await client.read_gatt_char(char.uuid)
                            print(f"[BME Char] {char} - {char.properties}, Value: {value}")
                            await client.start_notify(char, notification_handler)
                            bmeChar = char
                        except Exception as e:
                            print(f"[BME Char] {char} - {char.properties}, ERROR: {e}")


        keep_alive = True
        while keep_alive:
            toggle = await set_led()

            val = toggle.to_bytes(1, 'big')
            print(val)
            await client.write_gatt_char(devInfo.getCharacteristicUuid(charLed), val)
            await asyncio.sleep(1.0)

            res = await get_input()
            if res == 1:
                keep_alive = False
                await client.stop_notify(bmeChar)
                print("Disconnecting...")
            else:
                print("Staying connected.")


asyncio.run(main())