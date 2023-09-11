from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

supplier_profile = KeyboardButton('/🙋Профиль')
supplier_obj = KeyboardButton('/🏡Объекты')

supplier = ReplyKeyboardMarkup(resize_keyboard= True)
supplier.add(supplier_profile).add(supplier_obj)


obj_takeAll = KeyboardButton('/🏢Все_объекты')
obj_newReq = KeyboardButton('/❗️Новые_заявки')
obj_back = KeyboardButton('/◀️Назад_снабжение')


obj = ReplyKeyboardMarkup(resize_keyboard=True)
obj.add(obj_takeAll).add(obj_back)