import os

from wrapper.DatabaseWrapper import DatabaseWrapper
from models.DatabaseModel import DBConfig

from flask import Flask, jsonify
from flask_wtf.csrf import CSRFProtect
from flask import Flask, jsonify, render_template, request


class TemperatureApp:
    def __init__(self, username, password, api_key):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.urandom(24)

        self.csrf = CSRFProtect()
        self.csrf.init_app(self.app)

        config = DBConfig(username=username,
                          password=password,
                          hostname="localhost",
                          port=5432,
                          database_name="SQS_Weather_DB")

        self.db = DatabaseWrapper(config=config, api_key=api_key)

        @self.app.route("/temperature/<city>")
        def get_temperature(city):
            temperature = self.db.get_temperature_by_city(city)
            return jsonify({"city": city, "temperature": temperature})

    def run(self):
        self.app.run()


if __name__ == "__main__":
    app = TemperatureApp(os.getenv("postgres_username"),
                         password=os.getenv("postgres_password"),
                         api_key=os.getenv("weather_api_key"))
    app.run()
