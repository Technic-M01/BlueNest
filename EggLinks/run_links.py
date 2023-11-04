from packages.links.weather_forecast import getWeatherForecast, WeatherForecast
from packages.links.sample_environment import run_sampling, SampleEnvironment

from packages.utils.file_utils import EggConfig, LogHandler
from packages.utils.egg_link_utils import getCurrentDateTime

import asyncio

async def sample_and_forecast():
    await SampleEnvironment().connect_and_sample()

    await WeatherForecast().getForecast()

    #TODO flatten the weather forecast dict so it fits a data frame

if __name__ == "__main__":
    # ec = EggConfig()
    # conf = ec.getEggConfig(name='LEDCallback')
    # ec.getEggCharacterisitc(conf, "led")

    # getWeatherForecast()
    # WeatherForecast().getForecast()

    asyncio.run(sample_and_forecast())
