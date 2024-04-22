import unittest
from unittest.mock import patch
import requests
from app.wrapper.APIWrapper import Weather


class TestWeather(unittest.TestCase):
    def setUp(self):
        self.weather = Weather()

    @patch('requests.get')
    def test_get_weather_by_city(self, mock_get):
        # Mock response data
        mock_response = {
            'location': {
                'name': 'London',
                'region': 'City of London, Greater London',
                'country': 'United Kingdom',
            },
            'current': {
                'temp_c': 15.5,
                'condition': {
                    'text': 'Partly cloudy'
                }
            }
        }

        # Set up the mock response
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        # Call the method with a test city
        weather_data = self.weather.get_weather_by_city('London')

        # Check if the method was called with the correct parameters
        mock_get.assert_called_once_with('https://api.weatherapi.com/v1/current.json',
                                         params={'q': 'London', 'key': self.weather.api_key})

        # Check if the returned data matches the mock response
        self.assertEqual(weather_data, mock_response)

    @patch('requests.get')
    def test_get_weather_by_city_api_error(self, mock_get):
        # Set up the mock response with an error status code
        mock_get.return_value.status_code = 400

        # Call the method with a test city
        with self.assertRaises(requests.exceptions.HTTPError):
            self.weather.get_weather_by_city('InvalidCity')

        # Check if the method was called with the correct parameters
        mock_get.assert_called_once_with('https://api.weatherapi.com/v1/current.json',
                                         params={'q': 'InvalidCity', 'key': self.weather.api_key})


if __name__ == '__main__':
    unittest.main()
