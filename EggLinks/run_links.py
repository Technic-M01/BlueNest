from packages.links.weather_forecast import getWeatherForecast
from packages.links.sample_environment import run_sampling, SampleEnvironment

from packages.utils.file_utils import EggConfig, LogHandler

import asyncio

async def sample_and_forecast():
    await SampleEnvironment().connect_and_sample()
    print("\n\ndone awaiting")


if __name__ == "__main__":
    # ec = EggConfig()
    # conf = ec.getEggConfig(name='LEDCallback')
    # ec.getEggCharacterisitc(conf, "led")

    # readings = run_sampling()
    # print(f"\nbme readings:\n{readings}")

    # print(f"\nlatest log entry:\n{LogHandler.getLatestLog()}")
    # getWeatherForecast()

    asyncio.run(sample_and_forecast())
