import requests

from .weather_data import WeatherData

class WeatherApiHandler:
    def __init__(self):
        self._current_temperature = 0
        self._weather_forecast = []

    def __get_weather_data(self, city_name):
        url = 'http://api.weatherapi.com/v1/forecast.json?key=21c4a5c69f08458e857143821232112&q={}&days=3&aqi=no&alerts=no'
        response = requests.get(url.format(city_name)).json()

        for i in range(3):
            description = response['forecast']['forecastday'][i]['day']['condition']['text']
            night_temperature = response['forecast']['forecastday'][i]['day']['mintemp_c']
            day_temperature = response['forecast']['forecastday'][i]['day']['maxtemp_c']
            icon = response['forecast']['forecastday'][i]['day']['condition']['icon']
            self._weather_forecast.append(WeatherData(night_temperature, day_temperature, description, icon))

        self._current_temperature = response['current']['temp_c']

    def get_current_temperature(self, city_name):
        if not self._current_temperature:
            self.__get_weather_data(city_name)
        
        return self._current_temperature

    def get_weather_forecast(self, city_name):
        if not self._weather_forecast:
            self.__get_weather_data(city_name)
        
        return self._weather_forecast







