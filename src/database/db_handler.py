from sqlalchemy import create_engine, Column, Float, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List
from .weather_data import WeatherData  # Assuming WeatherData is defined in this module

Base = declarative_base()

class WeatherRecord(Base):
    __tablename__ = 'weather_records'  # Fixed tablename to __tablename__
    
    id = Column(Integer, primary_key=True)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    precipitation = Column(Float)
    location = Column(String)
    timestamp = Column(DateTime)

class DatabaseHandler:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def store_weather_data(self, weather_data: List[WeatherData]):
        session = self.Session()
        try:
            for data in weather_data:
                record = WeatherRecord(
                    temperature=data.temperature,
                    humidity=data.humidity,
                    wind_speed=data.wind_speed,
                    precipitation=data.precipitation,
                    location=data.location,
                    timestamp=datetime.fromisoformat(data.timestamp)
                )
                session.add(record)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()