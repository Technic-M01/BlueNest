import json

with open("/home/mauri-v/projects/BlueNest/EggLinks/econfig.json", 'r') as file:
    data = json.load(file)

    print(data)

    for key in data:
        print(f"key: {key} value: {data[key]}")

# put json file in 'links' dir
# put methods to read it in link_utils dir
# have method to get json file retreive/check path with pathlib (like in log_utils)
# have method return a dictionary with specified device from name/address/egg specifier 