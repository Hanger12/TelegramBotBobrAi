import threading
from multiprocessing import Process
import asyncio

from api.log_route import app
from bot.bot import run_bot

if __name__ == "__main__":
    asyncio.run(run_bot())
