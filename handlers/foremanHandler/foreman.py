from aiogram import types, dispatcher
from handlers.supplierHandler import supplier_kb
from handlers.adminHandler.adminTools import adminCreateUser
from handlers.objectHandler.objectGenerativeKb import objButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import db
from bot_create import dp, bot

async def command_foreman(message:types.Message):
    if message.text == '/Объекты':
        for obj in db.checkObjForeman(message.from_user.id):
            # await bot.send_photo(chat_id=message.from_user.id, photo=open(f"static/obj-{obj[0]}.jpg", 'rb'))
            await bot.send_message(message.from_user.id, f"*Объект*: {obj[1]}", parse_mode="Markdown", reply_markup= objButton(obj[0]))
    if message.text == '/✉️Мои_заявки':
        for Application in db.checkApplicationsByForemanId(message.from_user.id):
            fullInfo = InlineKeyboardMarkup()
            fullInfoBut = InlineKeyboardButton(text="Получить полную информацию по заявке",
                                               callback_data=f"app_{Application[0]}_info")
            fullInfoChange = InlineKeyboardButton(text="Добавить пункт в заявку",
                                                  callback_data=f"app_{Application[0]}_add")
            appDelete = InlineKeyboardButton(text="Удалить заявку", callback_data=f"app_{Application[0]}_delete")
            fullInfo.add(fullInfoBut).add(fullInfoChange).add(appDelete)
            await message.answer(f"*Заявка-{Application[0]}*\n"
                                          f"*Создана: {Application[3]}*", parse_mode="Markdown", reply_markup=fullInfo)
    if message.text == '/✅Создать_заявку':
        db.makeNewApp(message.from_user.id)
        await message.reply('заявка создана!')
    if message.text == '/◀️Назад_снабжение':
        await message.reply('Меню', reply_markup= supplier_kb.supplier)

def register_handerls_foreman(dp : dispatcher):
    dp.register_message_handler(command_foreman, commands=['✉️Мои_заявки','✅Создать_заявку', '◀️Назад_прораб', 'Объекты' ])