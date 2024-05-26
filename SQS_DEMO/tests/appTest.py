from app.app import TemperatureApp

import unittest
import unittest.mock as mock
from flask import json
from flask_testing import TestCase

from app.wrapper.DatabaseWrapper import DatabaseWrapper
from app.models.DatabaseModel import DBConfig


class TestTemperatureApp(TestCase):
    def setUp(self):
        # Create a mock DatabaseWrapper instance
        self.mock_db = mock.Mock(spec=DatabaseWrapper)

        # Create a TemperatureApp instance with the mock DatabaseWrapper
        self.app = TemperatureApp(username="test_user",
                                  password="test_password",
                                  api_key="test_api_key")
        self.app.db = self.mock_db

        # Set up the Flask testing environment
        self.client = self.app.app.test_client(self)

    def test_get_temperature_valid_city(self):
        # Mock the DatabaseWrapper.get_temperature_by_city method to return a valid temperature
        self.mock_db.get_temperature_by_city.return_value = 20.0

        # Make a GET request to the /temperature/<city> endpoint with a valid city name
        response = self.client.get("/temperature/London")

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the response JSON contains the correct city name and temperature
        self.assertEqual(json.loads(response.data), {"city": "London", "temperature": 20.0})

    def test_get_temperature_invalid_city(self):
        # Mock the DatabaseWrapper.get_temperature_by_city method to return None (indicating that the city is invalid)
        self.mock_db.get_temperature_by_city.return_value = None

        # Make a GET request to the /temperature/<city> endpoint with an invalid city name
        response = self.client.get("/temperature/InvalidCity")

        # Check that the response status code is 404 Not Found
        self.assertEqual(response.status_code, 404)

        # Check that the response JSON contains an error message
        self.assertEqual(json.loads(response.data), {"error": "City not found"})

    def test_get_temperature_db_error(self):
        # Mock the DatabaseWrapper.get_temperature_by_city method to raise an exception (indicating that there is a
        # database error)
        self.mock_db.get_temperature_by_city.side_effect = Exception("Database error")

        # Make a GET request to the /temperature/<city> endpoint with a valid city name
        response = self.client.get("/temperature/London")

        # Check that the response status code is 500 Internal Server Error
        self.assertEqual(response.status_code, 500)

        # Check that the response JSON contains an error message
        self.assertEqual(json.loads(response.data), {"error": "Database error"})


if __name__ == "__main__":
    unittest.main()
