import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv
import db

#donwload .env
load_dotenv ()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

#start
@dp.message(lambda msg: msg.text == "/start")
async def start_heandler(message: Message) :
    await message.answer(f"{hbold("HI")} я поможу тобі вивч слова", parse_mode=ParseMode.HTML )

async def main():
    await dp.start_polling(bot)

# Add words
@dp.message(lambda msg: msg.text.startswith("/addtoday"))
async def add_word(message: Message):
    try:
        parts = message.text.split( " ", 3 )
        if len(parts) < 4:
            await message.answer("Форимат: /addtoday слово переклад транскрипція")
            return
        
        word, translation, transcription = parts[1], parts[2], parts[3]
        user_id = message.from_user.id

        conn = sqlite3.connect("words.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO words (user_id, word, translation, transcription) VALUES (?, ?, ?, ?) ",
           (user_id, word, translation, transcription))
        conn.commit()
        conn.close()

        await message.answer(f"✅ Додано: {word} — {translation} [{transcription}]")

    except Exception as e:
        await message.answer(f"❌ Помилка: {e}")

if __name__ == '__main__':
    asyncio.run(main())