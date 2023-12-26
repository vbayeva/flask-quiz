import requests

from .weather_data import WeatherData

class WeatherApiHandler:
    def __init__(self):
        self._current_temperature = 0
        self._weather_forecast = []
        self._is_request_ok = True

    def __get_weather_data(self, city_name):
        url = 'http://api.weatherapi.com/v1/forecast.json?key=21c4a5c69f08458e857143821232112&q={}&days=3&aqi=no&alerts=no'
        response = requests.get(url.format(city_name))
        response_josn = response.json()

        self._is_request_ok = response.ok

        if not self._is_request_ok: 
            print("Not ok")
            return

        print("Ok")
        for i in range(3):
            description = response_josn['forecast']['forecastday'][i]['day']['condition']['text']
            night_temperature = response_josn['forecast']['forecastday'][i]['day']['mintemp_c']
            day_temperature = response_josn['forecast']['forecastday'][i]['day']['maxtemp_c']
            icon = response_josn['forecast']['forecastday'][i]['day']['condition']['icon']
            self._weather_forecast.append(WeatherData(night_temperature, day_temperature, description, icon))

        self._current_temperature = response_josn['current']['temp_c']

    def is_ok(self, city_name):
        if not self._current_temperature:
            self.__get_weather_data(city_name)

        return self._is_request_ok

    def get_current_temperature(self, city_name):
        if not self._current_temperature:
            self.__get_weather_data(city_name)
        
        return self._current_temperature

    def get_weather_forecast(self, city_name):
        if not self._weather_forecast:
            self.__get_weather_data(city_name)
        
        return self._weather_forecast







