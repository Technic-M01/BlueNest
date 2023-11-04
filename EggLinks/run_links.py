from packages.links.weather_forecast import getWeatherForecast
from packages.links.sample_environment import run_sampling

from packages.utils.file_utils import EggConfig, LogHandler

# ec = EggConfig()
# conf = ec.getEggConfig(name='LEDCallback')
# ec.getEggCharacterisitc(conf, "led")

readings = run_sampling()
print(f"\nbme readings:\n{readings}")

print(f"\nlatest log entry:\n{LogHandler.getLatestLog()}")
# getWeatherForecast()