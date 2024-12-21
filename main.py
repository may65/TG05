import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from datetime import datetime, timedelta

from config import TOKEN, THE_CAT_API_KEY, NASA_API_KEY

# Создаем экземпляр бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения случайного изображения кота
async def get_random_cat():
    headers = {'x-api-key': THE_CAT_API_KEY}
    response = requests.get('https://api.thecatapi.com/v1/images/search', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data[0]['url']
    else:
        return None

# Функция для получения изображения дня от NASA
async def get_nasa_apod():
    params = {'api_key': NASA_API_KEY}
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    if response.status_code == 200:
        data = response.json()
        return data['url'], data['title'], data['explanation']
    else:
        return None, None, None

# Хэндлер для команды /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Я бот, который может показать тебе случайного котика или астрономическое изображение дня от NASA. Используй команды /cat и /nasa.")

# Хэндлер для команды /cat
@dp.message(Command(commands=['cat']))
async def cat_command(message: Message):
    cat_image_url = await get_random_cat()
    if cat_image_url:
        await message.answer_photo(cat_image_url, caption="Вот тебе котик!")
    else:
        await message.answer("Не удалось получить изображение кота.")

# Хэндлер для команды /nasa
@dp.message(Command(commands=['nasa']))
async def nasa_command(message: Message):
    nasa_image_url, title, explanation = await get_nasa_apod()
    if nasa_image_url:
        await message.answer_photo(nasa_image_url, caption=f"{title}\n\n{explanation}")
    else:
        await message.answer("Не удалось получить изображение от NASA.")

# Хэндлер для команды /help
@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer("Доступные команды:\n/start - начать работу с ботом\n/cat - получить изображение котика\n/nasa - получить астрономическое изображение дня от NASA")

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())