from weather_api import WeatherAPI, WeatherAPIError
from pdf_generator import PDFReportGenerator

def main():
	print("Welcome to the Weather Report Generator!")

	while True:
		try:
			api_key = input("Enter your API key (www.weatherapi.com): ")
			city = input("Enter the city: ")
			days = 7

			weather_api = WeatherAPI(api_key)
			pdf_generator = PDFReportGenerator()

			weather_data = weather_api.get_weather_data(city, days)
			pdf_generator.create_report(weather_data, city)
			print(f"PDF report has been generated: {pdf_generator.filename}")
			break
			
		except WeatherAPIError as e:
			print(f"Error: {e}")
			retry = input("Would you like to try again? (y/n): ")
			if retry.lower() != 'y':
				print("Exiting program.")
				break
		except Exception as e:
			print(f"An unexpected error occurred: {e}")
			print("Exiting program.")
			break

if __name__ == "__main__":
	main()