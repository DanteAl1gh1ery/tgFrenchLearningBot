import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv


#Роутер з файлу handlers.py
from handlers import router as handlers_router

async def main() -> None:
    load_dotenv()  # Start bot
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        logging.critical ("Token not found! Chek file .env")
        return
    
    #initial bot and DP
    bot = Bot(TOKEN)
    dp = Dispatcher()

    #Add router with hendlers to main DP
    dp.include_router(handlers_router)

    #Chek updates
    await dp.start_polling(bot)


if __name__ == "__main__":
    # Налаштовуємо логування для отримання інформації про роботу бота
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Бот запущений...")
    
    # Запускаємо головну функцію
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Роботу бота зупинено вручну.")