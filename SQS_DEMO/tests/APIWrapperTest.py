import unittest
import unittest.mock as mock

from app.wrapper.APIWrapper import Weather


class TestWeather(unittest.TestCase):
    def setUp(self):
        self.weather = Weather("api_key")

    @mock.patch("requests.get")
    def test_get_weather_by_city(self, mock_get):
        # Test that the correct URL is used to make the API request
        city = "London"
        expected_url = "https://api.openweathermap.org/data/2.5/weather?q=London&appid=api_key&units=metric"
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"test": "data"}

        result = self.weather.get_weather_by_city(city)

        mock_get.assert_called_with(expected_url)
        self.assertEqual(result, {"test": "data"})

    @mock.patch("requests.get")
    def test_handle_response(self, mock_get):
        # Test that the correct data is returned for different HTTP status codes
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"test": "data"}
        result = self.weather._handle_response(mock_get.return_value)
        self.assertEqual(result, {"test": "data"})

        mock_get.return_value.status_code = 400
        result = self.weather._handle_response(mock_get.return_value)
        self.assertIsNone(result)

        mock_get.return_value.status_code = 401
        result = self.weather._handle_response(mock_get.return_value)
        self.assertIsNone(result)

        mock_get.return_value.status_code = 403
        result = self.weather._handle_response(mock_get.return_value)
        self.assertIsNone(result)

        mock_get.return_value.status_code = 404
        result = self.weather._handle_response(mock_get.return_value)
        self.assertIsNone(result)

        mock_get.return_value.status_code = 500
        result = self.weather._handle_response(mock_get.return_value)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
