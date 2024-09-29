import logging
import httpx
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from logger import file_handler, console_handler
from bot_init import bot, dp


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

API_URL = 'http://localhost:8975'


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.reply('Привет!\n'
                        'Я - NATASHA, '
                        'интеллектуальный помощник оператора службы поддержки RUTUBE.\n'
                        'Пиши мне любой вопрос и я найду на него ответ!')


@dp.message()
async def answer_for_all_question(message: types.Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        text = message.text
        logger.info(f'Q: {text}')

        if text.startswith('/'):
            await message.reply('Я знаю только команду /start. '
                                'Можешь задавать мне вопросы сразу!')
            return

        data = {'question': text}

        async with httpx.AsyncClient() as client:
            response = await client.post(API_URL + '/predict', json=data, timeout=300)
            response_data = response.json()

        answer = response_data['answer']
        if answer == "":
            answer = "Не могу ответить на данный вопрос."
        logger.info(f'A: {answer}')

        keyboard_markup = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text='👍', callback_data='feedback_good'),
                InlineKeyboardButton(text='👎', callback_data='feedback_bad'),
            ]]
        )
        await message.reply(answer, reply_markup=keyboard_markup)


@dp.callback_query(lambda c: c.data and c.data.startswith("feedback"))
async def save_feedback(callback_query: types.CallbackQuery):
    logger.info(f'Callback: {callback_query.data}')

    answer_text = 'Спасибо за отзыв!'
    match callback_query.data:
        case 'feedback_good':
            answer_text += ' Рада помочь!'
        case 'feedback_bad':
            answer_text += ' Буду становиться лучше!'

    await callback_query.answer(answer_text)
    await callback_query.message.edit_reply_markup(None)
