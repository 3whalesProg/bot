from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

#----------------------Admin-base------------------------
base_b1 = KeyboardButton('/👥Пользователи')
admin_back = KeyboardButton('/⬅️Назад')

base = ReplyKeyboardMarkup(resize_keyboard= True)

base.add(base_b1)
#----------------------Admin-base------------------------

#----------------------Admin-users------------------------

users_b1 = KeyboardButton('/заявки_на_регистрацию')
users_inline = InlineKeyboardButton(text='Зарегистрировать', callback_data='www')

usersReg = InlineKeyboardMarkup(row_width=1)
usersReg.add(users_inline)
users = ReplyKeyboardMarkup(resize_keyboard=True)

users.add(users_b1).add(admin_back)

#----------------------Admin-users------------------------