import requests

def process_weather_data(data):
    result = {}
    
    for day in data['forecast']['forecastday']:
        date = day['date']
        result[date] = {
            'daily_avg_temp': day['day']['avgtemp_c'],
            'hourly_temps': [hour['temp_c'] for hour in day['hour']]
        }
    
    return result

def get_weather_data(city, api_key):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=7&aqi=no&alerts=no"
    print(url)
    response = requests.get(url)
    processed_data = process_weather_data(response.json())
    return processed_data

def main():
    api_key = 'c8ac459c908541218de153203242011'
    city = "Berlin"
    weather_data = get_weather_data(city, api_key)
    print(weather_data)

main()