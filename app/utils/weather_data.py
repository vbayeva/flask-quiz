class WeatherData:
    def __init__(self, night_temperature, day_temperature, description, icon):
        self.night_temperature = night_temperature
        self.day_temperature = day_temperature
        self.description = description
        self.icon = icon

    def __repr__(self):
        return '<Description {}>'.format(self.description)