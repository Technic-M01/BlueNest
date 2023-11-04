from packages.links.weather_forecast import getWeatherForecast, WeatherForecast
from packages.links.sample_environment import run_sampling, SampleEnvironment

from packages.utils.file_utils import EggConfig, LogHandler
from packages.utils.egg_link_utils import getCurrentDateTime

import asyncio

async def sample_and_forecast():
    sampleData = await SampleEnvironment().connect_and_sample()

    forecastData = await WeatherForecast().getForecast()

    print(f"\nsample data:\n{sampleData}\nforecast data:\n{forecastData}")

    combined = {**sampleData, **forecastData}

    #add timestamp to dataset
    updict = {"Timestamp": getCurrentDateTime()}

    data = {**updict, **combined}
    
    # print(data)

    LogHandler().writeCombinedLog(data)

if __name__ == "__main__":
    # ec = EggConfig()
    # conf = ec.getEggConfig(name='LEDCallback')
    # ec.getEggCharacterisitc(conf, "led")

    # readings = run_sampling()
    # print(f"\nbme readings:\n{readings}")

    # print(f"\nlatest log entry:\n{LogHandler.getLatestLog()}")

    # getWeatherForecast()
    # WeatherForecast().getForecast()

    asyncio.run(sample_and_forecast())
