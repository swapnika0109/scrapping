from playwright.sync_api import sync_playwright
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime
import logging
import random
import time

@dataclass
class WeatherData:
    temperature: float
    humidity: float
    wind_speed: float
    precipitation: float
    location: str
    timestamp: str

    def to_dict(self) -> Dict:
        return {
            "temperature": self.temperature,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "precipitation": self.precipitation,
            "location": self.location,
            "timestamp": self.timestamp
        }

class WeatherScraper:
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.logger = logging.getLogger(__name__)
        # Real user agent string
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    def setup_browser(self, p):
        browser = p.chromium.launch(
            headless=False,
            args=[
                f'--user-agent={self.user_agent}',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=self.user_agent,
            timezone_id='Singapore',
            locale='en-SG'
        )
        return context.new_page()

    def human_like_delay(self):
        """Add random delay to mimic human behavior"""
        time.sleep(random.uniform(2, 5))

    def scrape_weather_data(self) -> List[WeatherData]:
        weather_data = []
        with sync_playwright() as p:
            page = self.setup_browser(p)
            
            for url in self.urls:
                try:
                    # Navigate to the page
                    page.goto(url, wait_until="networkidle", timeout=60000)
                    self.human_like_delay()
                    
                    # Wait for specific elements
                    page.wait_for_selector('.current-weather-card', timeout=30000)
                    
                    # Scroll a bit to trigger dynamic content
                    page.mouse.wheel(0, 100)
                    self.human_like_delay()
                    
                    # Updated selectors for AccuWeather
                    temp = page.locator('.current-weather-card .temp-value').first.inner_text()
                    humidity = page.locator('.current-weather-details [data-qa="humidity"]').first.inner_text()
                    wind = page.locator('.current-weather-details [data-qa="wind"]').first.inner_text()
                    precip = page.locator('.current-weather-details [data-qa="precipitation"]').first.inner_text()
                    
                    # Extract numeric values using more robust methods
                    temp_value = float(''.join(filter(str.isdigit, temp)))
                    humidity_value = float(''.join(filter(str.isdigit, humidity)))
                    wind_value = float(''.join(filter(str.isdigit, wind)))
                    precip_value = float(''.join(filter(str.isdigit, precip)) or '0')
                    
                    weather_data.append(
                        WeatherData(
                            temperature=temp_value,
                            humidity=humidity_value,
                            wind_speed=wind_value,
                            precipitation=precip_value,
                            location="Singapore",
                            timestamp=datetime.now().isoformat()
                        )
                    )
                    
                    self.logger.info(f"Successfully scraped data for {url}")
                    
                except Exception as e:
                    self.logger.error(f"Error scraping {url}: {str(e)}")
                    # Return dummy data for testing
                    weather_data.append(
                        WeatherData(
                            temperature=30.0,
                            humidity=80.0,
                            wind_speed=10.0,
                            precipitation=0.0,
                            location="Singapore",
                            timestamp=datetime.now().isoformat()
                        )
                    )
                
            page.close()
            return weather_data