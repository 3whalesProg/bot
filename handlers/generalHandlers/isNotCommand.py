from aiogram import types, dispatcher
from handlers.generalHandlers.kbByRole import takeRoleKb

async def empty(message: types.Message):
    #активируется, если введенной команды не существует. Вернет клавиатуру в зависимости от роли
    await message.answer('Нет такой команды', reply_markup= await takeRoleKb(message.from_user.id))

def register_handerls_emptyCommand(dp : dispatcher):
    dp.register_message_handler(empty)