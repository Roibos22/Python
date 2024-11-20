
from weather_api import WeatherAPI
from pdf_generator import PDFReportGenerator

def main():
    api_key = 'c8ac459c908541218de153203242011'
    city = "Berlin"
    days = 7

    weather_api = WeatherAPI(api_key)
    pdf_generator = PDFReportGenerator()

    weather_data = weather_api.get_weather_data(city, days)
    pdf_generator.create_report(weather_data, city)
    print(f"PDF report has been generated: {pdf_generator.filename}")

if __name__ == "__main__":
    main()