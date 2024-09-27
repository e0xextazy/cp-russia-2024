from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu():
    item1 = InlineKeyboardButton(
        text="'FAQ'", callback_data="FAQ"
    )
    item2 = InlineKeyboardButton(
        text="Задать вопрос", callback_data="question"
    )

    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[[item1], [item2]])

    return keyboard_markup
