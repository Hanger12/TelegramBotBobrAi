import unittest
from weather.weather_service import get_weather, WeatherAPIError


class TestWeatherAPI(unittest.TestCase):

    def test_get_weather(self):
        """Тест для функции получения погоды."""
        city = "Moscow"
        weather_data = get_weather(city)
        self.assertIn("temp", weather_data)
        self.assertIn("feels_like", weather_data)
        self.assertIn("description", weather_data)

    def test_get_weather_invalid_city(self):
        """Тест для обработки ошибки при неверном названии города."""
        with self.assertRaises(WeatherAPIError):
            get_weather("InvalidCityName")

    def test_get_weather_empty_city(self):
        """Тест для обработки пустого имени города."""
        with self.assertRaises(WeatherAPIError):
            get_weather("")

    def test_get_weather_case_insensitivity(self):
        """Тест для проверки регистронезависимости имени города."""
        weather_data_upper = get_weather("Moscow")
        weather_data_lower = get_weather("moscow")
        self.assertEqual(weather_data_upper, weather_data_lower)  # предполагается, что данные должны быть одинаковыми


if __name__ == "__main__":
    unittest.main()
