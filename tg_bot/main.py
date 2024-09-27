import os
import sys
import asyncio
import logging

from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, Router, types
from tg_bot.handlers.common import start_command, faq_command, ask_question_command


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv(".env")

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
dp.message(Command("start"))(start_command)


async def on_startup(dp):
    pass


async def main() -> None:
    await on_startup(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())