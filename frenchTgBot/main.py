# main.py
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Імпортуємо наш роутер з хендлерами
from handlers import router as main_router
import database
async def main():
    database.init_db()
    # Завантажуємо змінні середовища
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")

    # Ініціалізуємо бота та диспетчер
    bot = Bot(token=bot_token)
    # MemoryStorage - простий спосіб зберігати стани FSM в оперативній пам'яті
    dp = Dispatcher(storage=MemoryStorage()) 

    # Підключаємо роутер до диспетчера
    dp.include_router(main_router)

    # Видаляємо старий вебхук, щоб уникнути конфліктів
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаємо бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот зупинений.")