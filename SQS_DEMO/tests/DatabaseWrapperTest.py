from app.wrapper.DatabaseWrapper import DatabaseWrapper, WeatherData

import unittest
import unittest.mock as mock
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MockConfig:
    def __init__(self):
        self.db_nm = "test_db"

    @staticmethod
    def get_connection_string():
        return "sqlite:///:memory:"


class TestDatabaseWrapper(unittest.TestCase):
    def setUp(self):
        # Create a mock engine and session for testing
        self.mock_engine = create_engine("sqlite:///:memory:")
        self.mock_session = sessionmaker(bind=self.mock_engine)
        base = WeatherData.__table__.metadata
        base.create_all(self.mock_engine)

        # Create a mock API wrapper
        self.mock_api_wrapper = mock.Mock()
        self.mock_api_wrapper.get_weather_by_city.return_value = {"main": {"temp": 20}}

        # Create a mock Config object
        self.mock_config = MockConfig()

        # Create a DatabaseWrapper instance with the mock engine, API wrapper, and Config object
        self.db_wrapper = DatabaseWrapper(self.mock_config, None)
        self.db_wrapper.engine = self.mock_engine
        self.db_wrapper.api_wrapper = self.mock_api_wrapper
        self.db_wrapper.session = self.mock_session

    def tearDown(self):
        # Drop the tables after each test
        base = WeatherData.__table__.metadata
        base.drop_all(self.mock_engine)

    def test_get_temperature_by_city_no_data(self):
        # Test that new data is added to the database when there is no existing data
        city = "London"
        temperature = self.db_wrapper.get_temperature_by_city(city)
        self.assertEqual(temperature, 20)

        # Check that the API was called
        self.mock_api_wrapper.get_weather_by_city.assert_called_with(city)

        # Check that the new data was added to the database
        db_session = self.mock_session()
        data = db_session.query(WeatherData).filter_by(city=city).first()
        self.assertIsNotNone(data)
        self.assertEqual(data.temperature, 20)
        db_session.close()

    def test_get_temperature_by_city_outdated_data(self):
        # Test that the API is called and the database is updated when the data is outdated
        city = "Test City"
        old_temperature = 20.0
        new_temperature = 25.0

        # Add outdated data to the database
        outdated_datetime = datetime.now() - timedelta(minutes=16)
        outdated_datetime = outdated_datetime.replace(tzinfo=timezone.utc)

        data = WeatherData(city=city, temperature=old_temperature, last_update=outdated_datetime)
        db_session = self.db_wrapper.session()
        db_session.add(data)
        db_session.commit()

        # Mock the API to return new data
        self.mock_api_wrapper.get_weather_by_city.return_value = {
            "main": {
                "temp": new_temperature
            }
        }

        # Call the method to get the temperature
        temperature = self.db_wrapper.get_temperature_by_city(city)

        # Assert that the temperature is the new temperature from the API
        self.assertEqual(temperature, new_temperature)

        # Assert that the API was called
        self.mock_api_wrapper.get_weather_by_city.assert_called_once_with(city)

        # Assert that the database was updated with the new data
        data = db_session.query(WeatherData).filter_by(city=city).one()
        self.assertEqual(data.temperature, new_temperature)
        self.assertTrue(data.last_update > outdated_datetime)

        db_session.close()

    def test_get_temperature_by_city_up_to_date_data(self):
        # Test that up-to-date data is returned from the database without calling the API
        city = "London"
        temperature = 20
        last_update = datetime.now(timezone.utc) - timedelta(minutes=5)

        # Mock the API response
        self.mock_api_wrapper.get_weather_by_city.return_value = {
            "main": {
                "temp": temperature
            }
        }

        # Add up-to-date data to the database
        db_session = self.mock_session()
        new_data = WeatherData(city=city, temperature=temperature, last_update=last_update)
        db_session.add(new_data)
        db_session.commit()
        db_session.close()

        # Get the temperature using the mock session
        temperature = self.db_wrapper.get_temperature_by_city(city, db_session=self.mock_session())
        self.assertEqual(temperature, 20)

        # Check that the API was not called
        self.mock_api_wrapper.get_weather_by_city.assert_not_called()

        # Check that the data was returned from the database
        db_session = self.mock_session()
        data = db_session.query(WeatherData).filter_by(city=city).first()
        self.assertIsNotNone(data)
        self.assertEqual(data.temperature, temperature)
        db_session.close()


if __name__ == "__main__":
    unittest.main()
