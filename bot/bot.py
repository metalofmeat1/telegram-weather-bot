import requests
import asyncio
from os import getenv
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import ReplyKeyboardMarkup
from aiogram.filters import CommandStart, Command
from aiogram.types.keyboard_button import KeyboardButton
import kb
import datetime
import logging
import sys
from fsm import WeatherForm

load_dotenv()


root_router = Router()


@root_router.message(Command('weather'))
async def weather_info(message: types.Message, state: FSMContext):
    await message.answer('Оберіть місто із списку, щоб дізнатися погоду:', reply_markup=kb.keyboard)
    await state.set_state(WeatherForm.weather_process)


@root_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer('Вітаємо у нашому боті! Щоб дізнатися погоду введіть команду /weather !🌆')


@root_router.message(WeatherForm.weather_process)
async def weather_info(message: types.Message, state: FSMContext):

    weather_types = {
        'Clear': 'Ясно☀️',
        'Clouds': 'Хмарно🌥',
        'Rain': 'Дощ🌧',
        'Thunderstorm': 'Гроза⛈',
        'Snow': 'Сніг🌨',
        'Mist': 'Туман🌫'
    }

    try:
        city = message.text
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={getenv('WEATHER_TOKEN')}&units=metric"

        req = requests.get(url)

        data = req.json()

        city = data['name']
        current_weather = data['main']['temp']
        print('2')
        weather_description = data['weather'][0]['main']
        if weather_description in weather_types:
            desc = weather_types[weather_description]
        else:
            desc = 'Немає інформації'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']

        await message.reply(f'<b>🏡 Обране місто:</b> {city}\n<b>🌡 Температура:</b> {current_weather}°C, {desc}\n'
                            f'<b>💧 Вологість:</b> {humidity}%\n<b>🎚 Тиск:</b> {pressure} мм рт. ст.\n'
                            f'<b>🌬 Швидкість вітру</b>: {wind_speed}м/с\n'
                            f'\nГарного дня! 😊', parse_mode=ParseMode.HTML)
        await state.clear()

    except requests.exceptions.RequestException:
        await message.reply('Помилка мережі. Будь ласка, спробуйте ще раз пізніше.')

    except Exception as e:
        await message.reply(f'Виникла помилка: {str(e)}')


@root_router.message(Command('rating'))
async def rating(message: types.Message):
    await message.reply('Залишіть будь ласка оцінку, якщо вам сподобалося користуватися цим ботом перейшовши в канал з відгуками: https://t.me/rating_weatherbot 😊')


@root_router.message(Command('mail'))
async def mail(message: types.Message):
    await message.reply('Розсилка підключена!')
    while True:
        try:
            time = datetime.datetime.now().strftime('%H:%M')

            if time == '12:00':
                await message.reply('Не бажаєте подивитись погоду в ашому боті?')
                break
        except Exception as ex:
            await message.reply(f'error - {ex}')


@root_router.message(Command('info'))
async def start(message: types.Message):
    await message.answer("Цей бот був створений розробниками О. Кондратюком та В. Шмерігою.\nЗв'зок з нами:\n"
                         "О. Кондратюк: @lnly_77\nВ. Шмеріга: @iluniki_67")


async def main():
    bot = Bot(getenv('BOT_TOKEN'))

    dp = Dispatcher()

    dp.include_router(root_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())