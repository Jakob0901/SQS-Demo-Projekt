import requests


class Weather:
    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def _handle_response(response):
        """
        A private method to handle the API response.
        This method can be mocked in the tests.
        """
        match response.status_code:
            case 200:
                return response.json()
            case requests.codes.bad_request:
                print(f"Bad request: {response.text}")
                return None
            case requests.codes.unauthorized:
                print(f"Unauthorized: {response.text}")
                return None
            case requests.codes.forbidden:
                print(f"Forbidden: {response.text}")
                return None
            case requests.codes.not_found:
                print(f"City not found: {response.text}")
                return None
            case _:
                print(f"An error occurred while fetching the weather data: {response.text}")
                return None

    def _make_request(self, url):
        """
        A private method to make the API request.
        This method can be mocked in the tests.
        """
        try:
            response = requests.get(url)
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the weather data: {e}")
            return None

    def get_weather_by_city(self, city):
        """
        Get the current weather for a specified city.
        This method is responsible for formatting the URL and delegates the API request to _make_request.
        """
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])

        return self._make_request(url)
