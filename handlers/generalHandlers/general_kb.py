from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

app_cancel = KeyboardButton('/❌Отменить_действие')
app = ReplyKeyboardMarkup(resize_keyboard=True)
app.add(app_cancel)