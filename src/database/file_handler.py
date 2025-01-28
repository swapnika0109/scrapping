import json
from datetime import datetime
from typing import Dict

class FileHandler:
    def __init__(self, output_file: str):
        self.output_file = output_file

    def save_weather_data(self, data: Dict) -> None:
        """Save weather data to a text file with timestamp"""
        timestamp = datetime.now().isoformat()
        
        with open(self.output_file, 'a') as f:
            # Add timestamp to the data
            data['saved_at'] = timestamp
            
            # Write the JSON data with timestamp as a new line
            f.write(json.dumps(data) + '\n') 