from aiogram import types, dispatcher
from bot_create import bot
import db
from handlers.generalHandlers.kbByRole import takeRoleKb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.adminHandler import admin_kb
from handlers.supplierHandler import supplier_kb
from handlers.foremanHandler import foreman_kb


class registerForm(StatesGroup):
    first_name = State()
    second_name = State()
    role = State()
    phone = State()
    password = State()
    mail = State()



# @dp.message_handler()
async def command_start(message:types.Message):
    if db.isAuth(message.from_user.id):
        print('')
        await message.reply('Вы авторизованы. Начнем работу!', reply_markup= await takeRoleKb(message.from_user.id))
    else:
        print(message.from_user.id)
        await message.reply("Отправьте запрос на регистрацию")
        await registerForm.first_name.set()
        await message.reply("Напишите свое имя")



# @dp.message_handler(state=registerForm.first_name)
async def inputFirstName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text.capitalize()
    await registerForm.next()
    await message.reply("Теперь введите свою фамилию")

# @dp.message_handler(state=registerForm.second_name)
async def inputSecondName(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['second_name'] = message.text.capitalize()
    await registerForm.next()
    await message.reply("Какую роль вы хотите получить?")

# @dp.message_handler(state=registerForm.role)
async def inputRole(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['role'] = message.text.lower()
    await registerForm.next()
    await message.reply("Введите свой номер телефона")

# @dp.message_handler(state=registerForm.phone)
async def inputPhone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text
    await registerForm.next()
    await message.reply("Введите желаемый пароль длинной от 8 символов")

async def inputPassword(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text
    await registerForm.next()
    await message.reply("Введите свой email")

# @dp.message_handler(state=registerForm.first_name)
async def inputMail(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mail'] = message.text
        await message.reply(f"Заявка на регистрацию отправлена и будет рассмотрена администратором. Вам придет уведолмение, когда заявка будет принята. "
                            f"Контактный телефон по вопросам работы сервиса: 89103760570\n\n"
                            f"Ваш будущий профиль:\n"
                            f"*Фамилия и имя*: {data['second_name']} {data['first_name']}\n"
                            f"*Роль*: {data['role']}\n"
                            f"*Номер телефона*: {data['phone']}\n"
                            f"*email*: {data['mail']}\n"
                            f"Если что-то в заявке заполнено не правильно. пропишите команду /start и заполните форма заново", parse_mode="Markdown")
        await bot.send_message(1193506877, 'Пришла новая заявка!')
        db.regRequest(message.from_user.id, data)
    await state.finish()


def register_handerls_client(dp : dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(inputFirstName, state=registerForm.first_name)
    dp.register_message_handler(inputSecondName, state=registerForm.second_name)
    dp.register_message_handler(inputRole, state=registerForm.role)
    dp.register_message_handler(inputPhone, state=registerForm.phone)
    dp.register_message_handler(inputPassword, state=registerForm.password)
    dp.register_message_handler(inputMail, state=registerForm.mail)
