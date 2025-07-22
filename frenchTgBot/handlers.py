# handlers.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Імпортуємо наші модулі
import keyboards
import database

# Створюємо роутер, до якого будемо прив'язувати всі хендлери
router = Router()

# Створюємо клас для станів FSM
class AddWord(StatesGroup):
    waiting_for_word = State()
    waiting_for_translation = State()
    waiting_for_transcription = State()

# Хендлер для команди /start
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Привіт, {message.from_user.full_name}! Я допоможу тобі вивчити слова.",
        reply_markup=keyboards.get_main_menu()
    )

# Хендлер для натискання на кнопку "Додати нове слово"
@router.callback_query(F.data == "add_word")
async def start_add_word(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Будь ласка, введіть слово, яке хочете додати:")
    # Встановлюємо стан очікування слова
    await state.set_state(AddWord.waiting_for_word)
    await callback.answer()

# Хендлер, що ловить слово і просить ввести переклад
@router.message(AddWord.waiting_for_word)
async def word_entered(message: Message, state: FSMContext):
    # Зберігаємо введене слово в пам'ять стану
    await state.update_data(word=message.text)
    await message.answer("Чудово! Тепер введіть переклад:")
    # Переводимо на наступний стан
    await state.set_state(AddWord.waiting_for_translation)

# Хендлер, що ловить переклад і просить транскрипцію
@router.message(AddWord.waiting_for_translation)
async def translation_entered(message: Message, state: FSMContext):
    await state.update_data(translation=message.text)
    await message.answer("Майже готово! Тепер введіть транскрипцію:")
    await state.set_state(AddWord.waiting_for_transcription)

# Хендлер, що ловить транскрипцію, зберігає все в БД і завершує діалог
@router.message(AddWord.waiting_for_transcription)
async def transcription_entered(message: Message, state: FSMContext):
    await state.update_data(transcription=message.text)
    
    # Отримуємо всі збережені дані
    user_data = await state.get_data()
    user_id = message.from_user.id
    
    # Викликаємо нашу функцію з файлу database.py
    database.add_word(
        user_id=user_id,
        word=user_data['word'],
        translation=user_data['translation'],
        transcription=message.text  # можна взяти з message.text або user_data
    )
    
    await message.answer(
        f"✅ Слово '{user_data['word']}' успішно додано!",
        reply_markup=keyboards.get_main_menu() # Показуємо меню знову
    )
    
    # Завершуємо стан
    await state.clear()