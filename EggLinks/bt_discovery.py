import argparse
import asyncio

from bleak import BleakScanner

whitelist=["98:DA:60:04:CC:13", "CA:9D:96:4B:3A:96", "CE:D1:62:42:A4:0D", "8E:D1:62:42:A4:0D"]

async def main(args: argparse.Namespace):
    print("Whitelisted devices:")
    for w in whitelist:
        print(w)

    print("\nscanning for 5 seconds, please wait...")

    devices = await BleakScanner.discover(
        return_adv=True, cb=dict(use_bdaddr=args.macos_use_bdaddr)
    )

    for d, a in devices.values():
        # print(type(d))
        print("  --- Device ---\n" + str(d))
        print("-" * len(str(d)))
        if d.address in whitelist:
            print()
            # print(type(a))
            print(a)
            md = a.manufacturer_data
            # print(str(type(md)) + " -> " + str(md))
            for m in md:
                # print(str(m) + " -> " + str(md[m]))
                decoded = md[m].hex()
                decoded = "0x" + str(decoded)
                print("manufacturer data: " + decoded)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    args = parser.parse_args()

    asyncio.run(main(args))