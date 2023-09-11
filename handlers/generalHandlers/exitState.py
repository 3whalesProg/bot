from aiogram import types, dispatcher
from aiogram.dispatcher import FSMContext
from handlers.generalHandlers.kbByRole import takeRoleKb


async def cancel(message: types.Message, state: FSMContext):
    #функция выхода из состояния, возвращает клавиатуру в зависимости от роли
    await message.answer('Создание заявки отменено', reply_markup= await takeRoleKb(message.from_user.id))
    await state.reset_state()
    await state.finish()

def register_handerls_exitState(dp : dispatcher):
    dp.register_message_handler(cancel, state="*", commands=['❌Отменить_действие'])
