
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import F , Router, types
from dotenv import load_dotenv
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()



@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привіт,  {message.from_user.full_name}! Я бот створений для допомоги вивчення вакабуляру" )

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
    if callback.data == "repeat_language":
        response_text = "Добре, давай повторимо!"

    await callback.message.edit_text(response_text)
    await callback.answer()
