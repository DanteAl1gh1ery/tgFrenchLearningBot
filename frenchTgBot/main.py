import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from aiogram import F
from dotenv import load_dotenv

load_dotenv()

# Отримуємо токен з .env файлу
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    # Якщо токен не знайдено, програма зупиниться з зрозумілим повідомленням
    raise ValueError("Токен не знайдено! Перевірте .env файл та імена змінних.")

dp =Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привіт,  {message.from_user.full_name}! Я бот створений для допомоги вивчення вакабуляру" )



async def main() -> None:
    # Ініціалізуємо бота з токеном
    bot = Bot(TOKEN)
    # Починаємо обробку апдейтів
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Налаштовуємо логування
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # Запускаємо головну функцію
    print("Бот запущений...")
    asyncio.run(main())