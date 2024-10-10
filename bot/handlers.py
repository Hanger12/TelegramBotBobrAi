import logging
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from db.repository import save_user_settings, get_user_settings, log_request
from weather.weather_service import get_weather

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Добро пожаловать в бота для проверки погоды! Этот бот создан в качестве теста "
                                    "для компании BobrAi., воспользуйтесь командами /weather <город> для отображения "
                                    "погоды по указанному городу, /setcity <город> для сохранения города по умолчанию")


async def weather(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /weather для получения погоды в указанном городе."""
    user_id = update.effective_user.id

    if len(context.args) == 0:
        # Проверка, установлен ли любимый город
        favorite_city = get_user_settings(user_id)
        if favorite_city:
            city = favorite_city
            await update.message.reply_text(f"Используем ваш сохраненный город: {city}.")
        else:
            await update.message.reply_text("Пожалуйста, укажите город.")
            return
    else:
        city = " ".join(context.args)

    try:
        logging.info("Получен запрос на погоду для города: %s", city)
        weather_data = get_weather(city)
        response = (
            f"Погода в {city}:\n"
            f"Температура: {weather_data['temp']}°C\n"
            f"Ощущаемая температура: {weather_data['feels_like']}°C\n"
            f"Описание: {weather_data['description']}\n"
            f"Влажность: {weather_data['humidity']}%\n"
            f"Скорость ветра: {weather_data['wind_speed']} м/с"
        )
        await update.message.reply_text(response)
        log_request(user_id, f"/weather {city}", response)
    except Exception as e:
        logging.error("Ошибка получения погоды для %s: %s", city, e)
        await update.message.reply_text("Не удалось получить данные о погоде. Попробуйте снова.")


async def set_favorite_city(update: Update, context: CallbackContext) -> None:
    """Команда для установки любимого города."""
    user_id = update.effective_user.id
    if len(context.args) == 0:
        await update.message.reply_text("Пожалуйста, укажите город для сохранения.")
        return

    city = " ".join(context.args)
    save_user_settings(user_id, city)
    await update.message.reply_text(f"Ваш любимый город '{city}' успешно сохранен!")
