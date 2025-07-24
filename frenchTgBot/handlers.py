
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F , Router, types
from dotenv import load_dotenv
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import create_connection, user_exists, create_user
router = Router()
DATABASE = "mydatabase.db"


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    conn = create_connection(DATABASE)
    if conn is None:
        await message.answer("Виникла помилка при підключенні до бази даних.")
        return
    try:
        user_id = message.from_user.id
        username = message.from_user.username

        if not user_exists(conn, user_id):
            create_user(conn, user_id, username)
            await message.answer (f"Привіт,  {username}! Радий тебе бачити. Що ти хочеш зробити?")
        else:
            await message.answer(f"Вітаю знову, {username}! Що ти хочеш зробити?")
    finally:
        # Цей блок виконається завжди, навіть якщо у 'try' виникне помилка
        if conn:
            conn.close()
    #Buttons 
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="📚 Почати нову мову",
        callback_data="start_new_language"
    ))
    builder.add(types.InlineKeyboardButton(
        text="🔄 Повторити попередню",
        callback_data="repeat_language"
    ))
    builder.adjust(1)

    await message.answer(
        "Почнемо з вивчення мови чи з повторення?",
        reply_markup=builder.as_markup()
    )

#Hendlers
@router.callback_query(F.data.in_(["start_new_language", "repeat_language"]))
async def process_language_choise(callback: CallbackQuery):
    if callback.data == "start_new_language":
        response_text = "Чудово почнемо вивчення нової мови!"
    elif callback.data == "repeat_language":
        response_text = "Добре, давай повторимо!"
    else:
        response_text = "Невідомий вибір." # Про всяк випадок

    await callback.message.edit_text(response_text)
    await callback.answer()
