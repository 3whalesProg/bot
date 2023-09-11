from aiogram import types, dispatcher
from handlers.supplierHandler import supplier_kb
from handlers.objectHandler.objectGenerativeKb import objButton
from handlers.objectHandler import objectWorker
from handlers.foremanHandler import foreman_kb
from handlers.generalHandlers.kbByRole import takeRoleKb
from handlers.adminHandler.adminTools import adminCreateUser
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from handlers.generalHandlers import general_kb
import db
from bot_create import dp, bot

class addItem(StatesGroup):
    application_id = State()
    title = State()
    quantity = State()
    cancel = State()

class changePerfom(StatesGroup):
    quan = State()

async def command_supplier(message:types.Message):
    if message.text == '/🙋Профиль':
        for user in db.userInfo(message.from_user.id):
            await message.answer(f"*Ваш профиль:*\n"
                                 f"*id*: {user[0]}\n"
                                 f"*Имя*: {user[1]}\n"
                                 f"*Фамилия*: {user[2]}\n"
                                 f"*Роль*: {user[3]}\n"
                                 f"*Телефон*: {user[4]}\n"
                                 f"*Почта*: {user[5]}", parse_mode="Markdown")
    if message.text == '/🏡Объекты':
        await message.reply('Поработаем с объектами', reply_markup=supplier_kb.obj)
    if message.text == '/🏢Все_объекты':
        for obj in db.checkObj():
            # await bot.send_photo(chat_id=message.from_user.id, photo=open(f"static/obj-{obj[0]}.jpg", 'rb'))
            await bot.send_message(message.from_user.id, f"*Объект*: {obj[1]}\n*Прораб*: {obj[2]}", parse_mode="Markdown", reply_markup= objButton(obj[0]))
    if message.text == '/◀️Назад_снабжение':
        await message.reply('Меню', reply_markup= supplier_kb.supplier)


@dp.callback_query_handler()
async def takeApplications(callback: types.CallbackQuery):
    # Обрабатывает callback с inline кнопок. ПЕРЕПИСАТЬ.
    #
    # callback строится по принципу obj/app/item_id_action
    # obj работает с объектами. в id Передается id объекта. Без третьего параметра. Присылает все объекты.
    # app работает с заявками. в id передается id заявки. Примеры третьего параметра: info(Присылает все объекты), add(добавляет пункт в заявку), delete(удалить заявку)
    # item работает с пунктами. В id передается id заявки. Примеры третьего параметра: changeStatus(Изменить пункт заявки), delete(удалить пункт заявки) и т.д
    if callback.data.split('_')[0] == 'obj':
        obj_id = int(callback.data.split('_')[1])
        if len(db.checkApplications(obj_id)) > 0:
            await callback.message.answer(f"---------------Объект-{obj_id}--------------")
            for Application in db.checkApplications(obj_id):
                fullInfo = InlineKeyboardMarkup()
                fullInfoBut = InlineKeyboardButton(text= "Получить полную информацию по заявке", callback_data=f"app_{Application[0]}_info")
                fullInfoChange = InlineKeyboardButton(text= "Добавить пункт в заявку", callback_data=f"app_{Application[0]}_add")
                appDelete = InlineKeyboardButton(text="Удалить заявку",callback_data=f"app_{Application[0]}_delete")
                fullInfo.add(fullInfoBut).add(fullInfoChange).add(appDelete)
                await callback.message.answer(f"*Заявка-{Application[0]}*\n"
                                      f"*Создана: {Application[3]}*", parse_mode="Markdown", reply_markup=fullInfo)
                await callback.answer()
            await callback.message.answer(f"----------------Объект-{obj_id}-------------")
        else: await callback.message.reply('Нет заявок.')

    if callback.data.split('_')[0] == 'app':
        app_id = int(callback.data.split('_')[1])
        if callback.data.split('_')[2] == "info":
            await callback.message.answer(f"------------Заявка-{app_id}--------------")
            for item in db.checkItems(app_id):
                itemAction = InlineKeyboardMarkup()
                itemChange = InlineKeyboardButton(text = 'Изменить заявку', callback_data=f"item_{item[0]}_change")
                itemAction.add(itemChange)
                await callback.message.answer(f"Название:    *{item[1]}*\n"
                                              f"Кол-во:          *{item[6]}*\n"
                                              f"Статус:           *{item[2]}*\n" , parse_mode="Markdown", reply_markup=itemAction)
            await callback.message.answer("-----------------------------------------")
            await callback.answer()
        if callback.data.split('_')[2] == "add":
            #Нажата кнопка "Добавить пункт в заявку". Создает пункт в заявке
            await callback.message.answer(f'Уникальный номер вашей заявки {app_id}. Продублируйте его в сообщении ниже', parse_mode="Markdown", reply_markup=general_kb.app)
            await addItem.application_id.set()
            await callback.answer()
        if callback.data.split('_')[2] == "delete":
            #Нажата кнопка "Удалить заявку". Удаляет заявку
            await callback.message.edit_text('Удалено')
            db.appDelete(app_id)


    if callback.data.split('_')[0] == 'item':
        item_id = int(callback.data.split('_')[1])
        if callback.data.split('_')[2] == 'change':
            #Нажата кнопка "Изменить заявку". Передает inline кнопки для редактирования пункта заявки
            ItemChange_kb = InlineKeyboardMarkup()
            ItemChange_status = InlineKeyboardButton(text='Изменить статус', callback_data= f'item_{item_id}_changeStatus')
            ItemChange_perfom = InlineKeyboardButton(text='Изменить "исполнена"', callback_data= f'item_{item_id}_changePerfom')
            ItemDelete = InlineKeyboardButton(text='Удалить пункт', callback_data= f'item_{item_id}_delete')
            ItemChange_kb.add(ItemChange_status).add(ItemDelete)
            await callback.message.edit_reply_markup(reply_markup= ItemChange_kb)
        if callback.data.split('_')[2] == 'changeStatus':
            #Нажата кнопка "Изменить статус". Передает inline кнопки с вариациями изменения статуса.
            ItemChange_kb = InlineKeyboardMarkup()
            ItemChange_name = InlineKeyboardButton(text='Статус "В обработке"', callback_data=f'item_{item_id}_changeDbTreat')
            ItemChange_quan = InlineKeyboardButton(text='Статус "Заказано"', callback_data=f'item_{item_id}_changeDbOrder')
            ItemChange_status = InlineKeyboardButton(text='Статус "Выполнено"', callback_data=f'item_{item_id}_changeDbDone')
            ItemChange_kb.add(ItemChange_name).add(ItemChange_quan).add(ItemChange_status)
            await callback.message.edit_reply_markup(reply_markup=ItemChange_kb)
        if callback.data.split('_')[2] == 'changeDbTreat':
            #Статус пункта заявки меняется на "В обработке"
            db.itemStatusTreat(item_id)
            item  = db.findItem(item_id)
            itemAction = InlineKeyboardMarkup()
            itemChange = InlineKeyboardButton(text='Изменить заявку', callback_data=f"item_{item[0]}_change")
            itemAction.add(itemChange)
            await callback.message.edit_text(f"Название:    *{item[1]}*\n"
                                          f"Кол-во:          *{item[6]}*\n"
                                          f"Статус:           *{item[2]}*\n" , parse_mode="Markdown", reply_markup=itemAction )
        if callback.data.split('_')[2] == 'changeDbOrder':
            #Статус пункта заявки меняется на "Заказано"
            db.itemStatusOrder(item_id)
            item = db.findItem(item_id)
            itemAction = InlineKeyboardMarkup()
            itemChange = InlineKeyboardButton(text='Изменить заявку', callback_data=f"item_{item[0]}_change")
            itemAction.add(itemChange)
            await callback.message.edit_text(f"Название:    *{item[1]}*\n"
                                             f"Кол-во:          *{item[6]}*\n"
                                             f"Статус:           *{item[2]}*\n"
                                             , parse_mode="Markdown", reply_markup=itemAction)
            #f"Исполнена: *{item[4]}*"
        if callback.data.split('_')[2] == 'changeDbDone':
            #Статус пункта заявки меняется на "Выполнено"
            db.itemStatusDone(item_id)
            item = db.findItem(item_id)
            itemAction = InlineKeyboardMarkup()
            itemChange = InlineKeyboardButton(text='Изменить заявку', callback_data=f"item_{item[0]}_change")
            itemAction.add(itemChange)
            await callback.message.edit_text(f"Название:    *{item[1]}*\n"
                                             f"Кол-во:          *{item[6]}*\n"
                                             f"Статус:           *{item[2]}*\n" , parse_mode="Markdown", reply_markup=itemAction)
        if callback.data.split('_')[2] == 'delete':
            #Нажата кнопка "Удалить пункт". Удаляет пункт заявки
            db.ItemDelete(item_id)
            await callback.message.edit_text(f"Удалено")

async def inputAppId(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['app_id'] = message.text
            if data['app_id'].isdigit():
                await addItem.next()
                await message.reply("Введите то, что хотите заказать. Опишите подробно характеристики заказываемого товара.")
            else:
                await message.reply("Введите уникальный номер заявки корректно")
                await addItem.application_id.set()
    except:
        await message.reply("[ОШИБКА]. Проверьте корректность уникального номера заявки. Создайте заявку заново", reply_markup= await takeRoleKb(message.from_user.id))
        await state.reset_state()
        await state.finish()


async def inputTitle(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['title'] = message.text.capitalize()
        await addItem.next()
        await message.reply("Введите количество/объем")
    except:
        await message.reply(
            "[ОШИБКА]. Проверьте корректность названия заявки. Создайте заявку заново.", reply_markup= await takeRoleKb(message.from_user.id))
        await state.reset_state()
        await state.finish()


# @dp.message_handler(state=registerForm.second_name)
async def inputQuantity(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['quantity'] = message.text.capitalize()
            db.addItem(data['title'], data['quantity'], int(data['app_id']))
            db.updateLastItem(data['title'], int(data['app_id']))
        await state.finish()
        await message.reply("Пункт для вашей заявки создан!", reply_markup= await takeRoleKb(message.from_user.id))
    except:
        await message.reply(
            "[ОШИБКА]. Не получилось создать объект. Что-то введенно некорректно.", reply_markup= await takeRoleKb(message.from_user.id))
        await state.reset_state()
        await state.finish()


async def inputQuan(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await state.set_state()
        data['quan'] = message.text
        await message.answer(data['quan'])



def register_handerls_supplier(dp : dispatcher):
    dp.register_message_handler(inputAppId, state=addItem.application_id)
    dp.register_message_handler(inputTitle, state=addItem.title)
    dp.register_message_handler(inputQuantity, state=addItem.quantity)
    dp.register_message_handler(command_supplier, commands=['🙋Профиль','🏡Объекты','🏢Все_объекты','❗️Новые_заявки', '◀️Назад_снабжение' ])
