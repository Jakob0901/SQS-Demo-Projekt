from datetime import datetime, timedelta, timezone

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from APIWrapper import Weather

Base = declarative_base()


class DBConfig:
    def __init__(self, username, password, hostname, port, database_name):
        self.usr = username
        self.pwd = password
        self.hstnm = hostname
        self.prt = port
        self.db_nm = database_name

    def get_connection_string(self):
        return f"postgresql://{self.usr}:{self.pwd}@{self.hstnm}:{self.prt}/{self.db_nm}"

    def __repr__(self):
        return f"<DBConfig(username={self.usr}, hostname={self.hstnm}, port={self.prt}, database_name={self.db_nm})>"


class WeatherData(Base):
    __tablename__ = 'weather_data'

    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    last_update = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<WeatherData(city={self.city}, temperature={self.temperature}, last_update={self.last_update})>"


class DatabaseWrapper:

    def __init__(self, config):
        self.engine = create_engine(config.get_connection_string())
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)
        self.api_wrapper = Weather()

    def get_temperature_by_city(self, city):
        """
        Get the most recent temperature for a specified city from the database,
        or from the OpenWeatherMap API if the data is outdated.

        :param city: The name of the city.
        :return: The most recent temperature for the city.
        """
        db_session = self.session()
        data = db_session.query(WeatherData).filter_by(city=city).first()
        if data is None or data.last_update < datetime.now(timezone.utc) - timedelta(minutes=15):
            # No data or data is outdated, get new temperature from API
            current_weather = self.api_wrapper.get_weather_by_city(city)
            temperature = current_weather['temp_c']  # todo verify
            if data is None:
                # No existing data, add new row
                new_data = WeatherData(city=city, temperature=temperature)
                db_session.add(new_data)
            else:
                # Existing data is outdated, update it
                data.temperature = temperature
            db_session.commit()
        else:
            # Data is up-to-date, use existing temperature
            temperature = data.temperature
        db_session.close()
        return temperature
