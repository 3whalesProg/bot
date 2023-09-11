from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, dispatcher
from bot_create import bot
import db
class adminRegisterForm(StatesGroup):
    id = State()
    first_name = State()
    second_name = State()
    role = State()
    phone = State()
    mail = State()

async def adminInputId(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['id'] = message.text
    await adminRegisterForm.next()
    await message.reply("Имя пользователя")
# @dp.message_handler(state=registerForm.first_name)
async def adminInputFirstName(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['first_name'] = message.text.capitalize()
    await adminRegisterForm.next()
    await message.reply("Фамилия пользователя")

# @dp.message_handler(state=registerForm.second_name)
async def adminInputSecondName(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['second_name'] = message.text.capitalize()
    await adminRegisterForm.next()
    await message.reply("Роль пользователя: снабженец, логист, директор, бухгалтер, инженерпто, прораб")

# @dp.message_handler(state=registerForm.role)
async def adminInputRole(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['role'] = message.text.lower()
    await adminRegisterForm.next()
    await message.reply("Введите свой номер телефона")

# @dp.message_handler(state=registerForm.phone)
async def adminInputPhone(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['phone'] = message.text
    await adminRegisterForm.next()
    await message.reply("Введите email пользователя")

# @dp.message_handler(state=registerForm.first_name)
async def adminInputMail(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['mail'] = message.text
        await message.reply(
                            f"Созданный Профиль:\n"
                            f"*id*: {info['id']}\n"
                            f"*Фамилия и имя*: {info['second_name']} {info['first_name']}\n"
                            f"*Роль*: {info['role']}\n"
                            f"*Номер телефона*: {info['phone']}\n"
                            f"*email*: {info['mail']}", parse_mode="Markdown")
        db.register(info)
        print(info['id'] + "is a new user!")
        try:
            await bot.send_message(int(info['id']), 'вы успешно зарегистрированы!')
        except: print('Не удалось отправить сообщение пользователю')
    await state.finish()
def register_handerls_adminCreateUser(dp: dispatcher):
    dp.register_message_handler(adminInputId, state=adminRegisterForm.id)
    dp.register_message_handler(adminInputFirstName, state=adminRegisterForm.first_name)
    dp.register_message_handler(adminInputSecondName, state=adminRegisterForm.second_name)
    dp.register_message_handler(adminInputRole, state=adminRegisterForm.role)
    dp.register_message_handler(adminInputPhone, state=adminRegisterForm.phone)
    dp.register_message_handler(adminInputMail, state=adminRegisterForm.mail)
