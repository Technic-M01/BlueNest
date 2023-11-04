import typer
from typing_extensions import Annotated
import argparse
import asyncio
import logging

from bleak import BleakClient, BleakScanner

# logger = logging.getLogger(__name__)



def main(device_name: Annotated[str, typer.Option("--name")]):
    print(f"device: {device_name}")

    asyncio.run(async_main(device_name))

async def async_main(dev_name: str):
    # logger.info("starting scan...")
    print("starting scan...")

    if dev_name is None:
        print("No device found with that name")
        return
    else:
        device = await BleakScanner.find_device_by_name(dev_name)
        if device is None:
            print(f"could not find device with name: {dev_name}")
            return

    print("connecting to device...")

    async with BleakClient(device) as client:
        print("connected")

        for service in client.services:
            print(f"[Service] {service}")

            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        print(f"  [Characteristic] {char} - {char.properties}, Value: {value}")
                        # check if the value is in the format of bytes or a bytestring
                        if "\\x" in str(value):
                            decoded_val = int.from_bytes(value, "big")
                        else:
                            decoded_val = value.decode()
                        print(f"   Decoded value: {decoded_val}")

                    except Exception as e:
                        print(f"  [Characteristic] {char} - {char.properties}, ERROR: {e}")

                else:
                    print(f"  [Characteristic] {char} - {char.properties}")

                for descriptor in char.descriptors:
                    try:
                        value = await client.read_gatt_descriptor(descriptor.handle)
                        print(f"    [Descriptor] {descriptor}, Value: {value}")
                    except Exception as e:
                        print(f"    [Descriptor] {descriptor}, ERROR: {e}")

        print("disconnecting...")

    print("disconnected")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()

#     device_group = parser.add_mutually_exclusive_group(required=True)

#     device_group.add_argument(
#         "--name",
#         metavar="<name>",
#         help="the name of the bluetooth device to connect to",
#     )
#     device_group.add_argument(
#         "--address",
#         metavar="<address>",
#         help="the address of the bluetooth device to connect to",
#     )

#     parser.add_argument(
#         "--macos-use-bdaddr",
#         action="store_true",
#         help="when true use Bluetooth address instead of UUID on macOS",
#     )

#     parser.add_argument(
#         "--services",
#         nargs="+",
#         metavar="<uuid>",
#         help="if provided, only enumerate matching service(s)",
#     )

#     parser.add_argument(
#         "-d",
#         "--debug",
#         action="store_true",
#         help="sets the log level to debug",
#     )

#     args = parser.parse_args()

#     log_level = logging.DEBUG if args.debug else logging.INFO
#     logging.basicConfig(
#         level=log_level,
#         format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
#     )

    # asyncio.run(main(args))

if __name__ == "__main__":
    typer.run(main)