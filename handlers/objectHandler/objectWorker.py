from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import db

async def checkObjects():
    for obj in db.checkObj():
        objButtons = InlineKeyboardMarkup()
        objInfo = InlineKeyboardButton(text="Получить заявки по объекту", callback_data=f"obj_{obj[0]}")
        objButtons.add(objInfo)
        # await bot.send_photo(chat_id=message.from_user.id, photo=open(f"static/obj-{obj[0]}.jpg", 'rb'))
        message = f"*Объект*: {obj[1]}\n*Прораб*: {obj[2]}"
