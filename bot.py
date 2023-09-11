from aiogram.utils import executor
from bot_create import dp
from handlers import client
from handlers.foremanHandler import foreman
from  handlers.supplierHandler import supplier
#--------------------------ADMIN-IMPORT------------------------------
from handlers.adminHandler import admin
from handlers.adminHandler.adminTools import adminCreateUser
from handlers.generalHandlers import exitState, isNotCommand


exitState.register_handerls_exitState(dp) #выход из State обязательно должен стоять выше всех остальных. Возвращает клавиатуру в зависимости от роли
client.register_handerls_client(dp)
foreman.register_handerls_foreman(dp)
admin.register_handerls_admin(dp)
adminCreateUser.register_handerls_adminCreateUser(dp)
supplier.register_handerls_supplier(dp)
isNotCommand.register_handerls_emptyCommand(dp) #срабатывает, если введёной команды не существует. ОБЯЗАТЕЛЬНО ДОЛЖЕН РЕГИСТРИРОВАТЬСЯ В КОНЦЕ. Возвращает клавиатуру в зависимости от роли



executor.start_polling(dp, skip_updates=True)