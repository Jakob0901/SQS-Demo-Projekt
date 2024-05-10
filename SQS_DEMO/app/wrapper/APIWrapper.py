import requests


class Weather:
    def __init__(self, api_key):
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.api_key = api_key

    def get_weather_by_city(self, city):
        """
        Get the current weather for a specified city.

        :param city: The name of the city.
        :return: A dictionary containing the weather data.
        """
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise an exception if the request failed
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the weather data for {city}: {e}")
            return None
