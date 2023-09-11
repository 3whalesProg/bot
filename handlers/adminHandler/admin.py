from aiogram import types, dispatcher
from handlers.adminHandler import admin_kb
from handlers.adminHandler.adminTools import adminCreateUser
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import db


class changeTg(StatesGroup):
    id = State()
    tg = State()
async def command_admin(message:types.Message):
    if message.text == '/👥Пользователи':
        await message.reply('Поработаем с пользователями', reply_markup=admin_kb.users )
    if message.text == '/Изменить_тг':
        await message.reply("Введите id пользователя")
        await changeTg.id.set()
    if message.text == '/заявки_на_регистрацию':
        for user in db.checkRegRequest():
            await message.reply(f"id: {user[0]}\n"
                                f"Имя: {user[1]}\n"
                                f"Фамилия: {user[2]}\n"
                                f"Телефон: {user[3]}\n"
                                f"Почта: {user[4]}\n"
                                f"Роль: {user[5]}\n")
    if message.text == '/Зарегистрировать':
        await message.reply("Введите имя пользователя")
        await adminCreateUser.adminRegisterForm.id.set()
    if message.text == '/⬅️Назад':
        await message.reply('меню', reply_markup=admin_kb.base)


async def inputId(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    await message.reply("Введите тг айди")
    await changeTg.next()


async def inputTg(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
            data['tg'] = message.text
        db.updateTg(int(data['id']), int(data['tg']))
        await state.finish()



def register_handerls_admin(dp : dispatcher):
    dp.register_message_handler(inputId, state=changeTg.id)
    dp.register_message_handler(inputTg, state=changeTg.tg)
    dp.register_message_handler(command_admin, commands=['заявки_на_регистрацию','👥Пользователи','⬅️Назад','Зарегистрировать', 'Изменить_тг' ])