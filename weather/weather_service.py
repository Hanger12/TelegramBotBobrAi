import requests
from config import Config

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherAPIError(Exception):
    pass


def get_weather(city: str) -> dict:
    """Получает данные о погоде для указанного города."""
    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": Config.OPENWEATHERMAP_API_KEY, "units": "metric"})
        response.raise_for_status()
        data = response.json()
        return {
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except requests.HTTPError as http_err:
        raise WeatherAPIError(f"HTTP error occurred: {http_err}") from http_err
    except Exception as err:
        raise WeatherAPIError(f"An error occurred: {err}") from err
