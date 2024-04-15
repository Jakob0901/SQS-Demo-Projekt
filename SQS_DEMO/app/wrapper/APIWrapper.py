import requests
import os


class Weather:
    def __init__(self):
        self.base_url = "https://api.weatherapi.com/v1/current.json"

        self.api_key = self.__get_api_key()

    def get_weather_by_city(self, city):
        """
        Get the current weather for a specified city.

        :param city: The name of the city.
        :return: A dictionary containing the weather data.
        """
        params = {
            'q': city,
        }

        if self.api_key != "":
            params['key'] = self.api_key

        response = requests.get(self.base_url, params=params)
        response.raise_for_status()  # Raise an exception if the request failed
        return response.json()

    @staticmethod
    def __get_api_key():
        """
        Get the API Key

        :return: String of the API Key.
        """
        for i in range(3):
            current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..' * i))
            key_file = os.path.join(current_dir, 'key.env')
            if os.path.isfile(key_file):
                with open(key_file, 'r') as f:
                    return f.read()
        return ""
