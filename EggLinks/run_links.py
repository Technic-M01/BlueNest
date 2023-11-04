from packages.links.weather_forecast import WeatherForecast
from packages.links.sample_environment import SampleEnvironment


import asyncio

async def sample_and_forecast():
    await SampleEnvironment().connect_and_sample()

    await WeatherForecast().getForecast()


if __name__ == "__main__":
    asyncio.run(sample_and_forecast())
