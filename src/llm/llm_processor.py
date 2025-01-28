from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from typing import Dict, List
import json
from datetime import datetime
import logging

class WeatherLLMProcessor:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        self.logger = logging.getLogger(__name__)
        self.clean_data_prompt = PromptTemplate(
            input_variables=["weather_data"],
            template="""
            Clean and standardize the following weather data:
            {weather_data}
            Return a JSON object with standardized values and additional insights.
            """
        )

    def process_weather_data(self, weather_data: List[Dict]) -> Dict:
        try:
            # Convert WeatherData objects to dicts
            weather_dict_list = [data.to_dict() for data in weather_data]
            
            prompt = self.clean_data_prompt.format(
                weather_data=json.dumps(weather_dict_list, indent=2)
            )
            response = self.llm(prompt)
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "original_data": weather_dict_list,
                    "processed_at": datetime.now().isoformat(),
                    "status": "raw_data_only"
                }
            
        except Exception as e:
            self.logger.error(f"Error processing data: {str(e)}")
            return {
                "error": str(e),
                "original_data": [d.to_dict() for d in weather_data],
                "processed_at": datetime.now().isoformat(),
                "status": "error"
            }