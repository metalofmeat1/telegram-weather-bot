from aiogram.fsm.state import State, StatesGroup


class WeatherForm(StatesGroup):
    weather_process = State()
