from aiogram import types
from tg_bot.keyboards.inline import main_menu
from tg_bot.services.faq import get_faq


async def start_command(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие:", reply_markup=main_menu())


async def faq_command(message: types.Message):
    faq = get_faq()
    faq_text = "\n\n".join([f"Q: {q['question']}\nA: {q['answer']}" for q in faq])
    await message.answer(f"FAQ:\n\n{faq_text}")


async def ask_question_command(message: types.Message):
    await message.answer("Введите ваш вопрос, и я отвечу на него!")
