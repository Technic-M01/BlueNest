from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

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

    # observation = mgr.weather_at_place('Dallas,USA')
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

    uvmgr = owm.uvindex_manager()
    uvi = uvmgr.uvindex_around_coords(lat, lon)
    # print(type(uvi))
    # print(f"uv index: {uvi}")
    print(f"uv index: {uvi.value}")

    # forecast = mgr.forecast_at_coords(lat, lon, 'daily')
    # forecast = mgr.forecast_at_place('Dallas,US', 'daily')
    # answer = forecast.will_be_clear_at(timestamps.tomorrow())

# getWeatherForecast()