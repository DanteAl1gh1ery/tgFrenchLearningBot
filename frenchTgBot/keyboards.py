# keyboards.py
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_menu():
    """Створює головну інлайн-клавіатуру."""
    builder = InlineKeyboardBuilder()
    builder.button(text="✍️ Додати нове слово", callback_data="add_word")
    builder.button(text="🧠 Почати тренування", callback_data="start_training")
    builder.adjust(1)  # Кожна кнопка буде в новому рядку
    return builder.as_markup()