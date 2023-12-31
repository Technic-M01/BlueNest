from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from ..utils.egg_link_utils import truncateFloat, getCurrentDateTime
from ..utils.file_utils import LogHandler
from ..utils.constants import *

class WeatherForecast():

    def __init__(self):
        self.owm = OWM("66cb824f42ee4f5d00be7b5a383a8ea7")
        self.manager = self.owm.weather_manager()

        self.setLocation()

    #TODO abstract this more
    def setLocation(self):
        reg = self.owm.city_id_registry()
        list_of_tuples = dallas = reg.ids_for('Dallas', country='US', state='TX', matching='exact')
        location = list_of_tuples[0]

        lon = location[-1]
        lat = location[-2]

        self.lon = lon
        self.lat = lat

    async def getForecast(self):
        observation = self.manager.weather_at_coords(self.lat, self.lon)
        w = observation.weather

        uvmgr = self.owm.uvindex_manager()
        uvi = uvmgr.uvindex_around_coords(self.lat, self.lon)

        temp_dict = w.temperature('fahrenheit')

        data = {
            "Timestamp": getCurrentDateTime(),
            "Status": w.detailed_status,
            "WindSpeed": truncateFloat(w.wind(unit='miles_hour')['speed']),
            "WindDegree": w.wind(unit='miles_hour')['deg'],
            "WindGust": truncateFloat(w.wind(unit='miles_hour')['gust']),
            "Humidity": w.humidity,
            "Temperature": temp_dict['temp'],
            "TemperatureMin": temp_dict['temp_min'],
            "TemperatureMax": temp_dict['temp_max'],
            # "Rain": w.rain,
            # "HeatIndex": w.heat_index,
            "Clouds": w.clouds,
            "Visibility": w.visibility(unit='miles'),
            "UVIndex": [uvi.value]
        }

        LogHandler().writeLogFile(data, FORECAST_LOG_FILE_NAME)

def getWeatherForecast():

    owm = OWM("66cb824f42ee4f5d00be7b5a383a8ea7")

    mgr = owm.weather_manager()

    reg = owm.city_id_registry()
    list_of_tuples = dallas = reg.ids_for('Dallas', country='US', state='TX', matching='exact')
    print(list_of_tuples)

    print(type(list_of_tuples[0]))
    location = list_of_tuples[0]

    lon = location[-1]
    lat = location[-2]

    # print(location[-1]) #longitude
    # print(location[-2]) #latitude

    # observation = mgr.weather_at_place('Dallas,US')
    observation = mgr.weather_at_coords(lat, lon)
    # observation = mgr.weather_at_place(list_of_tuples[0])
    # observation = mgr.weather_at_zip_code("75204", "USA")

    w = observation.weather

    print(f"status: {w.detailed_status}")
    #wind speed is in M/ps
    print(f"wind: {w.wind(unit='miles_hour')}")
    print(f"humidity: {w.humidity}")
    print(f"temp f: {w.temperature('fahrenheit')}")
    print(f"rain: {w.rain}")
    print(f"heat index: {w.heat_index}")
    print(f"clouds: {w.clouds}")
    print(f"visisbility: (m){w.visibility_distance} (km){w.visibility()} (mi){w.visibility(unit='miles')}")

    uvmgr = owm.uvindex_manager()
    uvi = uvmgr.uvindex_around_coords(lat, lon)
    # print(type(uvi))
    # print(f"uv index: {uvi}")
    print(f"uv index: {uvi.value}")

    # forecast = mgr.forecast_at_coords(lat, lon, 'daily')
    # forecast = mgr.forecast_at_place('Dallas,US', 'daily')
    # answer = forecast.will_be_clear_at(timestamps.tomorrow())
