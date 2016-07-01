from pyowm import *

API_key = "06082e1a23147515f393e65b8d9e300c"
owm = OWM(API_key, language="es")

observation = owm.weather_at_coords(10.067668, -84.305400)

weatherObj = observation.get_weather()

weather = weatherObj.get_detailed_status()

print(weather)