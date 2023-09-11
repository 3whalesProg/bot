from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

foreman_newApp = KeyboardButton('/✅Создать_заявку')
foreman_takeApp = KeyboardButton('/Объекты')

foreman = ReplyKeyboardMarkup(resize_keyboard= True)
foreman.add(foreman_takeApp).add(foreman_newApp)