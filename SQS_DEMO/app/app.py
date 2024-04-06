from flask import Flask, jsonify
from wrapper.DatabaseWrapper import DatabaseWrapper


class TemperatureApp:
    def __init__(self, db_path):
        self.app = Flask(__name__)
        self.db = DatabaseWrapper(db_path)

        @self.app.route('/temperature/<city>')
        def get_temperature(city):
            temperature = self.db.get_temperature_by_city(city)
            return jsonify({'city': city, 'temperature': temperature})

    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = TemperatureApp('weather_data.db')
    app.run()
