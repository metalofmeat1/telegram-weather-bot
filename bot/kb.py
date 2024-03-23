from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

kb = [
    [
        KeyboardButton(text="Kyiv"),
        KeyboardButton(text="Odesa"),
        KeyboardButton(text="Lviv"),
        KeyboardButton(text="Chernivtsi"),
        KeyboardButton(text="Kharkiv"),
        KeyboardButton(text="Vinnytsia"),
        KeyboardButton(text="Zaporizhzhya"),
        KeyboardButton(text="Chernihiv"),
        KeyboardButton(text="Dnipro"),
        KeyboardButton(text="Sumy"),
        KeyboardButton(text="Kherson"),
    ],
]
keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)