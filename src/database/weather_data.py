from dataclasses import dataclass
from datetime import datetime

@dataclass
class WeatherData:
    temperature: float
    humidity: float
    wind_speed: float
    precipitation: float
    location: str
    timestamp: str = datetime.now().isoformat() 