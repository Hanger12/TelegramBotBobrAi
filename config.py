import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
    DATABASE_URL = (f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
