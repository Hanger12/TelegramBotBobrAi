from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers import weather, start, set_favorite_city
from config import Config


def run_bot():
    """Запускает бота."""
    app = ApplicationBuilder().token(Config.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('setcity', set_favorite_city))
    app.run_polling()
