import requests

class WeatherAPIError(Exception):
	"""Custom exception for weather API errors"""
	pass

class WeatherAPI:
	def __init__(self, api_key):
		self.api_key = api_key
		self.base_url = "http://api.weatherapi.com/v1/forecast.json"

	def get_weather_data(self, city, days):
		url = f"{self.base_url}?key={self.api_key}&q={city}&days={days}&aqi=no&alerts=no"
		try:
			response = requests.get(url)
			response.raise_for_status()  # Raises an HTTPError for bad responses
			return self._process_weather_data(response.json())
		except requests.exceptions.HTTPError as http_err:
			if response.status_code == 401:
				raise WeatherAPIError("Invalid API key. Please check your credentials.")
			elif response.status_code == 400:
				raise WeatherAPIError(f"Invalid city name: {city}")
			else:
				raise WeatherAPIError(f"HTTP error occurred: {http_err}")
		except requests.exceptions.RequestException as err:
			raise WeatherAPIError(f"Error fetching weather data: {err}")
		except KeyError as err:
			raise WeatherAPIError(f"Error processing weather data: Unexpected API response format")

	def _process_weather_data(self, data):
		result = {}
		for day in data['forecast']['forecastday']:
			date = day['date']
			result[date] = {
				'daily_avg_temp': day['day']['avgtemp_c'],
				'hourly_temps': [hour['temp_c'] for hour in day['hour']]
			}
		return result