![logo](/docs/images/bluenest-logo-v1.png)

# Overview
BlueNest is a multi-platform home automation project for monitoring and controlling your living space, and the surrounding area outside your home.

## Structure
The BlueNest ecosystem is comprised of a central device, the "nest"; peripheral devices, the "eggs"; and a mobile app, "Nest Link".


### Eggs
The "eggs" are connected via Bluetooth to the "nest" where the nest will receive data, parse it, log it locally on the device, and upload the values to an AWS DynamoDb table to be retrieved later from the mobile app.

![eggdiagram](/docs/images/egg-diagram-v1.png)


A cronjob will run once an hour (or whatever interval desired) to trigger the nest to create Bluetooth connections to the eggs as client devices. Once a connection is establish, the eggs sensors will begin whatever operation they're designed for. 

For example, a BME280 egg will begin sampling the environment, average the results, and populate the Bluetooth characteristic notifying the device thats acting as the Bluetooth server.

Once the data has been received by the server (nest), the Bluetooth connection will be terminated. Data received by the server will be parsed, logged locally on the device, then uploaded to the DynamoDb table for later retrieval. 

![systemdiagram](/docs/images/system-diagram-v1.png)

The code for the eggs is designed with the intention of it being as modular as possible, with the hope of any new eggs only needing to upload data to the notification characteristic to trigger the rest of the processes on the server(nest) side.

# Setup
## Cloning the repository
The BlueNest repository contains the repositories for the Eggs and Android app as submodules.
Cloning the repository should be ran with `git clone <url> --recurse-submodules` to retrieve the submodules.

## Python setup
most of the nest code is written in python, and needs a virtual environment to run.
All of the necessary libraries should be installed from requirements.txt

I used python3.8> to develop and test this, so I'd reccomend using 3.8 at minimum.


# Continuing Development
This project is still heavily in development as im actively developing it, and when I have a release candidate ready, I'll post it as soon as I can.

## Features in Development
- [ ] Fully implemented nest link to AWS for authentication and data storage.

- [ ] Android app functionality with AWS services.

- [ ] Abstracting more of the "Egg" soure code for modularity.

- [ ] Implementation of more types of Eggs.

## Assorted 'ToDos'
- [ ] Adding more documentation to help setup Bluetooth on a linux machine.
(im developing with a Jetson Nano acting as my central device / nest, and it was a bit of a pain getting Bluetooth to behave)

- [ ] Adding documentation and wiring diagrams / circuit design of the Eggs.

- [ ] Implementing running all the "nest" process inside a docker container instead of using a cron job.

- [ ] more documentation in general.