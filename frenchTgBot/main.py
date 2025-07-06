import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv


#donwload .env
load_dotenv ()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

#start
@dp.message(commands=[' start '])
async def start_heandler(message: Message) :
    await message.answer(f"{hbold("HI")} я поможу тобі вивч слова", parse_mode=ParseMode.HTML )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())