from fastapi import FastAPI, HTTPException
from scrapper.weather_scrapper import WeatherScraper
from llm.llm_processor import WeatherLLMProcessor
from database.file_handler import FileHandler

app = FastAPI()

@app.post("/weather/scrape")
async def scrape_weather():
    try:
        # Initialize components
        urls = ["https://www.accuweather.com/en/sg/singapore/300597/weather-forecast/300597"]
        scraper = WeatherScraper(urls)
        llm_processor = WeatherLLMProcessor()
        file_handler = FileHandler("weather_data.txt")
        
        # Run pipeline
        weather_data = scraper.scrape_weather_data()
        processed_data = llm_processor.process_weather_data(weather_data)
        file_handler.save_weather_data(processed_data)
        
        return {"status": "success", "data": processed_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 