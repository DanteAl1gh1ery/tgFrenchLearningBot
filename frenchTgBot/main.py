from aiogram import Bot, Dispathcer, types
from aiogram.types import Message
from aiogram.utils import executor
from dotenv import load_dotenv
import os

#donwload .env
load_dotenv ()
BOT_TOKEN = os.getenv("BOT_TOKEN")
dp = Dispathcer(Bot)

#start
@dp.message_handler(commands=[' start '])
async def start(message: Message) :
    await message.answer("Hi! Я допоможу тобі!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)