import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
