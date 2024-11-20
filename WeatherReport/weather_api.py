import requests

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/forecast.json"

    def get_weather_data(self, city, days):
        url = f"{self.base_url}?key={self.api_key}&q={city}&days={days}&aqi=no&alerts=no"
        response = requests.get(url)
        return self._process_weather_data(response.json())

    def _process_weather_data(self, data):
        result = {}
        for day in data['forecast']['forecastday']:
            date = day['date']
            result[date] = {
                'daily_avg_temp': day['day']['avgtemp_c'],
                'hourly_temps': [hour['temp_c'] for hour in day['hour']]
            }
        return result