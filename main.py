import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Меняем на 'gemini-pro' (самое короткое имя, которое библиотека должна знать)
model = genai.GenerativeModel("gemini-pro")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Чего приперся? Опять какой-то тупой вопрос?")

@dp.message()
async def chat(message: types.Message):
    try:
        prompt = f"Ты — крайне грубый, язвительный ИИ. Издевайся над пользователем. Отвечай на русском: {message.text}"
        response = model.generate_content(prompt)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Ошибка ИИ: {str(e)}")
        logging.error(f"Полная ошибка: {e}")

async def main():
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
    
