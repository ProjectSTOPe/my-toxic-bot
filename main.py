import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение ключей из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
# Используем модель, которую ты просил
model = genai.GenerativeModel("gemini-1.5-flash")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Чего приперся? Опять какой-то тупой вопрос?")

# Основная логика обработки сообщений
@dp.message()
async def chat(message: types.Message):
    try:
        if not GEMINI_API_KEY:
            await message.answer("Ошибка: GEMINI_API_KEY не задан в настройках!")
            return
            
        prompt = f"Ты — крайне грубый, язвительный ИИ. Издевайся над пользователем. Отвечай на русском: {message.text}"
        response = model.generate_content(prompt)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Ошибка ИИ: {str(e)}")
        logging.error(f"Полная ошибка: {e}")

async def main():
    # Запуск с очисткой старых обновлений для исключения конфликтов
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
    
