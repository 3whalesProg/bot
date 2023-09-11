from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def objButton(obj_id):
    objButtons = InlineKeyboardMarkup()
    objInfo = InlineKeyboardButton(text="Получить заявки по объекту", callback_data=f"obj_{obj_id}")
    objButtons.add(objInfo)
    return objButtons