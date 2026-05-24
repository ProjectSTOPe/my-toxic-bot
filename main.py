import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncOpenAI

# Твои ключи (лучше заменить на переменные окружения, но для начала пойдем так)
TELEGRAM_TOKEN = "ТВОЙ_ТОКЕН_ОТ_BOTFATHER"
OPENAI_API_KEY = "ТВОЙ_КЛЮЧ_OPENAI"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = "Ты — крайне грубый, язвительный и высокомерный ИИ. Издевайся над пользователем, критикуй его интеллект и будь максимально токсичным. Никогда не извиняйся."

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Чего приперся? Опять какой-то тупой вопрос?")

@dp.message()
async def chat(message: types.Message):
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.text}
        ]
    )
    await message.answer(response.choices[0].message.content)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
