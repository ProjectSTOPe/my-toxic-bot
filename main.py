import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# Настройка логов, чтобы мы видели ошибки
logging.basicConfig(level=logging.INFO)

# Получаем ключи
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Проверка, чтобы точно знать, есть ли ключи
if not TELEGRAM_TOKEN:
    logging.error("ОШИБКА: TELEGRAM_TOKEN не найден в настройках!")
if not GEMINI_API_KEY:
    logging.error("ОШИБКА: GEMINI_API_KEY не найден в настройках!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Чего приперся? Опять какой-то тупой вопрос?")

@dp.message()
async def chat(message: types.Message):
    try:
        response = model.generate_content(f"Ты — крайне грубый ИИ. Отвечай очень токсично: {message.text}")
        await message.answer(response.text)
    except Exception as e:
        await message.answer("Даже на это у меня нет сил отвечать.")
        logging.error(f"Ошибка ИИ: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
