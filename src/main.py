import platform
import sys

def check_platform():
    if platform.system() not in ['Linux', 'Darwin']:  # Darwin is macOS
        print("ERROR: This script is intended to run on Linux or macOS only.")
        sys.exit(1)

from scrapper.weather_scrapper import WeatherScraper
from database.file_handler import FileHandler
from llm.llm_processor import WeatherLLMProcessor

def main():
    check_platform()
    
    # File configuration
    output_file = "weather_data.txt"
    
    # Initialize components
    urls = [
        "https://www.accuweather.com/en/sg/singapore/300597/weather-forecast/300597"
    ]
    
    scraper = WeatherScraper(urls)
    db_handler = FileHandler(output_file)
    llm_processor = WeatherLLMProcessor()
    
    # Run the pipeline
    weather_data = scraper.scrape_weather_data()
    processed_data = llm_processor.process_weather_data(weather_data)
    db_handler.save_weather_data(processed_data)

if __name__ == "__main__":
    main() 