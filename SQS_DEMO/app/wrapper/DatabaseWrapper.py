from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    last_update = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<WeatherData(city={self.city}, temperature={self.temperature}, last_update={self.last_update})>"


class Database:
    def __init__(self, db_path):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_weather_data(self, city, temperature):
        """
        Add new weather data to the database.

        :param city: The name of the city.
        :param temperature: The temperature in the city.
        """
        session = self.Session()
        new_data = WeatherData(city=city, temperature=temperature)
        session.add(new_data)
        session.commit()
        session.close()

    def get_weather_data(self, city):
        """
        Get the most recent weather data for a specified city.

        :param city: The name of the city.
        :return: A WeatherData object containing the most recent weather data for the city, or None if no data is found.
        """
        session = self.Session()
        data = session.query(WeatherData).filter_by(city=city).order_by(WeatherData.last_update.desc()).first()
        session.close()
        return data
